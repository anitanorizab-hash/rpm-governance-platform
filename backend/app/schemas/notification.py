"""Notification schemas (CP18)."""
from __future__ import annotations

from pydantic import BaseModel, Field

NOTIFICATION_TYPES = {
    "reminder", "missing_info", "approval", "report", "escalation", "fds_review",
}


class NotificationDraftIn(BaseModel):
    type: str = "reminder"
    recipient: str = Field(min_length=3)
    kpi: str | None = None
    detail: str | None = None
    subject: str | None = None
    related_entity_type: str | None = None
    related_entity_id: str | None = None


class NotificationPatchIn(BaseModel):
    recipient: str | None = None
    subject: str | None = None
    body: str | None = None


class NotificationOut(BaseModel):
    id: str
    type: str | None = None
    recipient: str | None = None
    subject: str | None = None
    body: str | None = None
    status: str
    related_entity_type: str | None = None
    related_entity_id: str | None = None
    approval_id: str | None = None
    failure_reason: str | None = None
    retry_count: int | None = None

    @classmethod
    def from_model(cls, m):
        return cls(id=m.id, type=m.type, recipient=m.recipient, subject=m.subject, body=m.body,
                   status=m.status, related_entity_type=m.related_entity_type,
                   related_entity_id=m.related_entity_id, approval_id=m.approval_id,
                   failure_reason=m.failure_reason, retry_count=m.retry_count)
