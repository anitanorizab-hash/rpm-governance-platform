"""Executive Copilot repository (CP16): interaction history + advisory recommendation drafts.

History reuses AIConversation with session_id = NULL (distinguishes copilot from chatbot sessions).
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai.ai_meta import AIConversation
from app.repositories.fds_repository import FDSRepository

import uuid


class ExecutiveCopilotRepository:
    def __init__(self, db: Session):
        self.db = db
        self.fds = FDSRepository(db)

    def log(self, *, user_id, kind, question, answer, grounded=False, fallback=False):
        c = AIConversation(id=str(uuid.uuid4()), session_id=None, user_id=user_id,
                           question=f"[{kind}] {question}", answer_ref=str(answer)[:2000],
                           grounded=grounded, fallback=fallback)
        self.db.add(c); self.db.flush(); return c

    def list_interactions(self, user_id: str | None = None, limit=100):
        stmt = select(AIConversation).where(AIConversation.session_id.is_(None))
        if user_id:
            stmt = stmt.where(AIConversation.user_id == user_id)
        return list(self.db.scalars(stmt.order_by(AIConversation.created_at.desc()).limit(limit)))

    def create_recommendation(self, *, kpi_id, content, rationale, priority=2):
        return self.fds.create_recommendation(kpi_id=kpi_id, type="Copilot", content=content,
                                               rationale=rationale, priority=priority,
                                               status="draft", reviewed_by=None)

    def get_recommendation(self, rec_id):
        return self.fds.get_recommendation(rec_id)
