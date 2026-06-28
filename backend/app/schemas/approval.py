"""Approval schemas (CP9)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ApprovalCreateIn(BaseModel):
    item_type: str          # report | notification | recommendation | copilot_recommendation | ...
    item_id: str
    submit: bool = False    # create straight into pending_review


class ApprovalDecisionIn(BaseModel):
    comment: str | None = None


class ApprovalOut(BaseModel):
    id: str
    item_type: str
    item_id: str
    state: str
    requested_by: str | None = None
    decision: str | None = None
    actor_id: str | None = None
    comment: str | None = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, m) -> "ApprovalOut":
        return cls(
            id=m.id, item_type=m.item_type, item_id=m.item_id, state=m.state,
            requested_by=m.requested_by, decision=m.decision, actor_id=m.actor_id,
            comment=m.comment, created_at=m.created_at, updated_at=m.updated_at,
        )
