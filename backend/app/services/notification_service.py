"""Notification service (CP18): draft → submit-for-review (CP9) → queue (approved only) → dry-run send.

No notification is sent without human approval. Queue changes audited. Role-scoped.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.repositories.approval_repository import ApprovalRepository
from app.repositories.notification_repository import NotificationRepository
from app.services import email_queue_service
from app.services.agent_service import AgentService
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService

MANAGE_ROLES = {"super_admin", "jpn_admin"}
DRAFT_ROLES = {"super_admin", "jpn_admin", "sector_admin"}
VIEW_ALL_ROLES = {"super_admin", "jpn_admin", "executive"}


class NotificationPermissionError(Exception):
    pass


class NotificationStateError(Exception):
    pass


class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = NotificationRepository(db)
        self.approvals = ApprovalRepository(db)
        self.audit = AuditService(db)

    # ----- draft -----
    def draft(self, *, current_user, data: dict, context: AuditContext | None = None):
        if not (set(current_user.role_names) & DRAFT_ROLES):
            raise NotificationPermissionError("Not permitted to draft notifications")
        agent_out = AgentService(self.db).execute("notification", {
            "type": data.get("type", "reminder"), "kpi": data.get("kpi", ""),
            "detail": data.get("detail", ""), "subject": data.get("subject"),
        }).get("output", {})
        n = self.repo.create(
            type=data.get("type", "reminder"), recipient=data.get("recipient"),
            subject=agent_out.get("subject"), body=agent_out.get("body"),
            related_entity_type=data.get("related_entity_type"),
            related_entity_id=data.get("related_entity_id"),
            status="draft", created_by=current_user.id,
        )
        self.audit.record(entity_type="notification", entity_id=n.id, action="notification_draft",
                          actor_id=current_user.id, after={"type": n.type, "recipient": n.recipient},
                          context=context, commit=False)
        self.db.commit()
        return n

    # ----- status sync from CP9 -----
    def _sync(self, n):
        if n.approval_id and n.status == "pending_review":
            ap = self.approvals.get(n.approval_id)
            if ap and ap.state == "approved":
                n.status = "approved"; n.approved_by = ap.actor_id; self.db.commit()
            elif ap and ap.state == "rejected":
                n.status = "cancelled"; n.failure_reason = ap.comment or "rejected"; self.db.commit()
        return n

    # ----- reads (role-scoped) -----
    def list_notifications(self, current_user):
        roles = set(current_user.role_names)
        if roles & VIEW_ALL_ROLES:
            items = self.repo.list()
        elif "kpi_pic" in roles:
            items = self.repo.list(recipient=current_user.email)
        else:
            items = self.repo.list()
        return [self._sync(n) for n in items]

    def get(self, current_user, notification_id):
        n = self.repo.get(notification_id)
        return self._sync(n) if n else None

    def patch(self, *, current_user, notification_id, fields, context=None):
        if not (set(current_user.role_names) & DRAFT_ROLES):
            raise NotificationPermissionError("Not permitted")
        n = self.repo.get(notification_id)
        if not n:
            return None
        if n.status != "draft":
            raise NotificationStateError("Only draft notifications can be edited.")
        for f in ("recipient", "subject", "body"):
            if fields.get(f) is not None:
                setattr(n, f, fields[f])
        self.db.commit()
        return n

    # ----- submit for review -----
    def submit_for_review(self, *, current_user, notification_id, context: AuditContext | None = None):
        if not (set(current_user.role_names) & DRAFT_ROLES):
            raise NotificationPermissionError("Not permitted")
        n = self.repo.get(notification_id)
        if not n:
            return None
        if n.status != "draft":
            raise NotificationStateError(f"Notification is '{n.status}'; only drafts can be submitted.")
        approval = ApprovalService(self.db).create_request(
            item_type="notification", item_id=n.id, requested_by=current_user.id, submit=True, context=context)
        n.status = "pending_review"; n.approval_id = approval.id
        self.audit.record(entity_type="notification", entity_id=n.id, action="notification_submit_for_review",
                          actor_id=current_user.id, after={"approval_id": approval.id}, context=context, commit=False)
        self.db.commit()
        return {"notification_id": n.id, "approval_id": approval.id, "approval_state": approval.state,
                "notification_status": n.status}

    # ----- queue (approved only) → dry-run send -----
    def queue(self, *, current_user, notification_id, context: AuditContext | None = None):
        if not (set(current_user.role_names) & MANAGE_ROLES):
            raise NotificationPermissionError("Not permitted to queue notifications")
        n = self.repo.get(notification_id)
        if not n:
            return None
        self._sync(n)
        if n.status != "approved":
            raise NotificationStateError(f"Only approved notifications can be queued (current: {n.status}).")
        n.status = "queued"
        result = email_queue_service.attempt_send(n)
        n.status = result["status"]
        n.failure_reason = result["failure_reason"]
        self.audit.record(entity_type="notification", entity_id=n.id, action="notification_queue",
                          actor_id=current_user.id, after={"status": n.status, "mode": result["mode"]},
                          context=context, commit=False)
        self.db.commit()
        return {"notification_id": n.id, "status": n.status, "mode": result["mode"],
                "retry_count": n.retry_count}

    def cancel(self, *, current_user, notification_id, context=None):
        if not (set(current_user.role_names) & DRAFT_ROLES):
            raise NotificationPermissionError("Not permitted")
        n = self.repo.get(notification_id)
        if not n:
            return None
        if n.status in ("sent",):
            raise NotificationStateError("Sent notifications cannot be cancelled.")
        n.status = "cancelled"
        self.audit.record(entity_type="notification", entity_id=n.id, action="notification_cancel",
                          actor_id=current_user.id, context=context, commit=False)
        self.db.commit()
        return {"notification_id": n.id, "status": n.status}

    # ----- email queue -----
    def email_queue(self, current_user):
        if not (set(current_user.role_names) & (MANAGE_ROLES | {"executive"})):
            raise NotificationPermissionError("Not permitted to view the email queue")
        return self.repo.email_queue()

    def retry(self, *, current_user, notification_id, context=None):
        if not (set(current_user.role_names) & MANAGE_ROLES):
            raise NotificationPermissionError("Not permitted to retry")
        n = self.repo.get(notification_id)
        if not n:
            return None
        if n.status not in ("failed", "queued"):
            raise NotificationStateError(f"Only failed/queued items can be retried (current: {n.status}).")
        n.retry_count = (n.retry_count or 0) + 1
        result = email_queue_service.attempt_send(n)
        n.status = result["status"]; n.failure_reason = result["failure_reason"]
        self.audit.record(entity_type="notification", entity_id=n.id, action="notification_retry",
                          actor_id=current_user.id, after={"status": n.status, "retry_count": n.retry_count},
                          context=context, commit=False)
        self.db.commit()
        return {"notification_id": n.id, "status": n.status, "retry_count": n.retry_count, "mode": result["mode"]}
