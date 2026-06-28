"""Audit schemas (CP5)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AuditLogOut(BaseModel):
    id: str
    entity_type: str
    entity_id: str | None = None
    action: str
    actor_id: str | None = None
    before: str | None = None        # already masked at write time
    after: str | None = None
    reason: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    request_id: str | None = None
    created_at: datetime

    @classmethod
    def from_model(cls, m) -> "AuditLogOut":
        return cls(
            id=m.id, entity_type=m.entity_type, entity_id=m.entity_id, action=m.action,
            actor_id=m.actor_id, before=m.before, after=m.after, reason=m.reason,
            ip_address=m.ip_address, user_agent=m.user_agent, request_id=m.request_id,
            created_at=m.created_at,
        )
