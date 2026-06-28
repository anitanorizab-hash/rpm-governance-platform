"""Executive Copilot schemas (CP16)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class AskIn(BaseModel):
    question: str = Field(min_length=1)


class RecommendationIn(BaseModel):
    kpi_id: str
    content: str = Field(min_length=1)
    rationale: str | None = None
    priority: int = 2


class RecommendationOut(BaseModel):
    id: str
    kpi_id: str
    type: str | None = None
    content: str | None = None
    rationale: str | None = None
    priority: int | None = None
    status: str | None = None

    @classmethod
    def from_model(cls, m):
        return cls(id=m.id, kpi_id=m.kpi_id, type=m.type, content=m.content,
                   rationale=m.rationale, priority=m.priority, status=m.status)


class SubmitForApprovalOut(BaseModel):
    recommendation_id: str
    approval_id: str
    approval_state: str
    recommendation_status: str


class HistoryItem(BaseModel):
    id: str
    question: str | None = None
    answer: str | None = None
    created_at: datetime

    @classmethod
    def from_model(cls, m):
        return cls(id=m.id, question=m.question, answer=m.answer_ref, created_at=m.created_at)
