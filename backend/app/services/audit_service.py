"""Audit service (CP5): reusable record() + role-scoped read access.

- record(): the single entry point future modules call to write audit entries (masked, append-only).
- list_logs()/get_log(): admin/oversight see all; other users see only their own actions.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.audit import AuditContext, write_audit
from app.repositories.audit_repository import AuditRepository

# Roles allowed to view ALL audit logs (admin + oversight).
AUDIT_VIEW_ALL_ROLES = {"super_admin", "jpn_admin", "internal_audit"}


class AuditService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AuditRepository(db)

    # --- write (reusable by all modules) ---
    def record(self, *, entity_type: str, action: str, entity_id: str | None = None,
               actor_id: str | None = None, before=None, after=None,
               reason: str | None = None, context: AuditContext | None = None,
               commit: bool = True):
        entry = write_audit(
            self.db, entity_type=entity_type, action=action, entity_id=entity_id,
            actor_id=actor_id, before=before, after=after, reason=reason, context=context,
        )
        if commit:
            self.db.commit()
        return entry

    # --- read (role-scoped) ---
    @staticmethod
    def _can_view_all(user) -> bool:
        return bool(set(user.role_names) & AUDIT_VIEW_ALL_ROLES)

    def list_logs(self, *, current_user, entity_type=None, action=None, limit=100, offset=0):
        actor_filter = None if self._can_view_all(current_user) else current_user.id
        return self.repo.list(actor_id=actor_filter, entity_type=entity_type,
                              action=action, limit=limit, offset=offset)

    def get_log(self, *, current_user, audit_id: str):
        log = self.repo.get(audit_id)
        if not log:
            return None
        if self._can_view_all(current_user) or log.actor_id == current_user.id:
            return log
        return "forbidden"   # caller maps to 403 (distinguish from not-found)
