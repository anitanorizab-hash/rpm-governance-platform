"""Approval engine (CP9): a generic, reusable Human-in-the-Loop state machine.

States: draft → pending_review → (approved | rejected); cancel from draft/pending → cancelled.
Final states (approved/rejected/cancelled) are IMMUTABLE. Every transition is audited.
No AI agent may approve/reject (decisions require an authenticated human with an approver role).
A requester cannot approve their own request unless a Super Admin override is used.

Reusable for: reports, notifications, FDS recommendations, Executive Copilot recommendations, future.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.repositories.approval_repository import ApprovalRepository
from app.services.audit_service import AuditService

# States
DRAFT, PENDING, APPROVED, REJECTED, CANCELLED = (
    "draft", "pending_review", "approved", "rejected", "cancelled",
)
FINAL_STATES = {APPROVED, REJECTED, CANCELLED}

# Allowed transitions
TRANSITIONS = {
    DRAFT: {PENDING, CANCELLED},
    PENDING: {APPROVED, REJECTED, CANCELLED},
    APPROVED: set(), REJECTED: set(), CANCELLED: set(),
}

APPROVER_ROLES = {"super_admin", "jpn_admin", "sector_admin", "executive"}


class ApprovalError(Exception):
    """Invalid transition / immutable final state."""


class ApprovalPermissionError(Exception):
    """Actor not permitted (role, own-request, or non-human)."""


class ApprovalService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ApprovalRepository(db)
        self.audit = AuditService(db)

    # ---------- creation ----------
    def create_request(self, *, item_type: str, item_id: str, requested_by: str,
                        submit: bool = False, context: AuditContext | None = None):
        """Create an approval request. Reusable entry point for any module."""
        state = PENDING if submit else DRAFT
        ap = self.repo.create(item_type=item_type, item_id=item_id,
                              requested_by=requested_by, state=state)
        self.audit.record(entity_type="approval", entity_id=ap.id,
                          action=f"approval_create_{state}", actor_id=requested_by,
                          after={"item_type": item_type, "item_id": item_id, "state": state},
                          context=context, commit=False)
        self.db.commit()
        return ap

    # ---------- transitions ----------
    def _transition(self, ap, target, *, actor, action, decision=None, comment=None, context=None):
        if ap.state in FINAL_STATES:
            raise ApprovalError(f"Approval is in final state '{ap.state}' and cannot be changed.")
        if target not in TRANSITIONS.get(ap.state, set()):
            raise ApprovalError(f"Cannot transition from '{ap.state}' to '{target}'.")
        before = ap.state
        ap.state = target
        if decision:
            ap.decision = decision
        if actor is not None:
            ap.actor_id = getattr(actor, "id", None)
        if comment is not None:
            ap.comment = comment
        self.audit.record(entity_type="approval", entity_id=ap.id, action=action,
                          actor_id=getattr(actor, "id", None), before={"state": before},
                          after={"state": target, "decision": decision}, context=context, commit=False)
        self.db.commit()
        return ap

    def submit(self, *, approval_id, actor, context=None):
        ap = self.repo.get(approval_id)
        if not ap:
            return None
        # requester or an admin may submit
        if actor.id != ap.requested_by and not (set(actor.role_names) & {"super_admin", "jpn_admin"}):
            raise ApprovalPermissionError("Only the requester or an admin may submit this request.")
        return self._transition(ap, PENDING, actor=actor, action="approval_submit", context=context)

    def approve(self, *, approval_id, actor, override: bool = False, comment=None, context=None):
        ap = self.repo.get(approval_id)
        if not ap:
            return None
        self._guard_decider(ap, actor, override)
        return self._transition(ap, APPROVED, actor=actor, action="approval_approve",
                                decision="approve", comment=comment, context=context)

    def reject(self, *, approval_id, actor, comment=None, context=None):
        ap = self.repo.get(approval_id)
        if not ap:
            return None
        self._guard_decider(ap, actor, override=False)
        return self._transition(ap, REJECTED, actor=actor, action="approval_reject",
                                decision="reject", comment=comment, context=context)

    def cancel(self, *, approval_id, actor, context=None):
        ap = self.repo.get(approval_id)
        if not ap:
            return None
        if actor.id != ap.requested_by and not (set(actor.role_names) & {"super_admin", "jpn_admin"}):
            raise ApprovalPermissionError("Only the requester or an admin may cancel this request.")
        return self._transition(ap, CANCELLED, actor=actor, action="approval_cancel", context=context)

    def _guard_decider(self, ap, actor, override: bool) -> None:
        roles = set(actor.role_names)
        # No AI agent may decide: actor is always an authenticated human user here; also require an approver role.
        if not (roles & APPROVER_ROLES):
            raise ApprovalPermissionError(
                f"Approval decisions require one of roles: {sorted(APPROVER_ROLES)}."
            )
        # Requester cannot approve/reject own request unless Super Admin override.
        if actor.id == ap.requested_by and not (override and "super_admin" in roles):
            raise ApprovalPermissionError(
                "Requester cannot decide on their own request (Super Admin override required)."
            )

    # ---------- reads / integration helper ----------
    def get(self, approval_id):
        return self.repo.get(approval_id)

    def list(self, *, state=None, item_type=None):
        return self.repo.list(state=state, item_type=item_type)

    def is_approved(self, item_type: str, item_id: str) -> bool:
        """Reusable gate: other modules call this before executing a formal action."""
        ap = self.repo.latest_for_item(item_type, item_id)
        return bool(ap and ap.state == APPROVED)
