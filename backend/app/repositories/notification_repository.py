"""Notification repository (CP18). The notification IS the email-queue item (status queued/sent/failed)."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operational.governance import Notification

QUEUE_STATES = ("queued", "sent", "failed")


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kw) -> Notification:
        n = Notification(id=str(uuid.uuid4()), retry_count=0, **kw); self.db.add(n); self.db.flush(); return n

    def get(self, notification_id: str) -> Notification | None:
        return self.db.get(Notification, notification_id)

    def list(self, *, recipient=None, status=None, limit=100, offset=0):
        stmt = select(Notification)
        if recipient:
            stmt = stmt.where(Notification.recipient == recipient)
        if status:
            stmt = stmt.where(Notification.status == status)
        return list(self.db.scalars(stmt.order_by(Notification.created_at.desc()).limit(limit).offset(offset)))

    def email_queue(self, limit=100):
        return list(self.db.scalars(
            select(Notification).where(Notification.status.in_(QUEUE_STATES))
            .order_by(Notification.created_at.desc()).limit(limit)
        ))
