"""Approval repository (CP9)."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operational.governance import Approval


class ApprovalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, approval_id: str) -> Approval | None:
        return self.db.get(Approval, approval_id)

    def create(self, *, item_type: str, item_id: str, requested_by: str, state: str) -> Approval:
        ap = Approval(id=str(uuid.uuid4()), item_type=item_type, item_id=item_id,
                      requested_by=requested_by, state=state)
        self.db.add(ap); self.db.flush()
        return ap

    def list(self, *, state=None, item_type=None, limit=100, offset=0):
        stmt = select(Approval)
        if state:
            stmt = stmt.where(Approval.state == state)
        if item_type:
            stmt = stmt.where(Approval.item_type == item_type)
        stmt = stmt.order_by(Approval.created_at.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(stmt))

    def latest_for_item(self, item_type: str, item_id: str) -> Approval | None:
        return self.db.scalar(
            select(Approval).where(Approval.item_type == item_type, Approval.item_id == item_id)
            .order_by(Approval.created_at.desc())
        )
