"""Chatbot schemas (CP15)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SessionOut(BaseModel):
    id: str
    user_id: str | None = None
    started_at: datetime | None = None

    @classmethod
    def from_model(cls, m):
        return cls(id=m.id, user_id=m.user_id, started_at=m.started_at)


class MessageIn(BaseModel):
    message: str = Field(min_length=1)
    achievement: str | None = None       # optional numeric context for KPI analysis
    target: str | None = None


class MessageOut(BaseModel):
    session_id: str
    question: str
    answer: str
    citations: list[dict] = []
    grounded: bool
    fallback_used: bool
    human_review_required: bool
    ralph_review: dict | None = None
    operational_context: list[dict] = []
    operational_summary: dict | None = None   # role-scoped KPI aggregates for data-intent questions


class ConversationOut(BaseModel):
    id: str
    question: str | None = None
    answer: str | None = None
    grounded: bool | None = None
    fallback: bool | None = None
    created_at: datetime

    @classmethod
    def from_model(cls, m):
        return cls(id=m.id, question=m.question, answer=m.answer_ref,
                   grounded=m.grounded, fallback=m.fallback, created_at=m.created_at)
