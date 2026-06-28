"""Chatbot repository (CP15): chat sessions + conversation history."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai.ai_meta import AIConversation, ChatSession


def _uid() -> str:
    return str(uuid.uuid4())


class ChatbotRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_id: str) -> ChatSession:
        s = ChatSession(id=_uid(), user_id=user_id, started_at=datetime.now(timezone.utc))
        self.db.add(s); self.db.flush(); return s

    def get_session(self, session_id: str) -> ChatSession | None:
        return self.db.get(ChatSession, session_id)

    def list_sessions(self, user_id: str | None = None):
        stmt = select(ChatSession)
        if user_id:
            stmt = stmt.where(ChatSession.user_id == user_id)
        return list(self.db.scalars(stmt.order_by(ChatSession.started_at.desc())))

    def create_conversation(self, *, session_id, user_id, question, answer, grounded, fallback):
        c = AIConversation(id=_uid(), session_id=session_id, user_id=user_id,
                           question=question, answer_ref=answer, grounded=grounded, fallback=fallback)
        self.db.add(c); self.db.flush(); return c

    def list_conversations(self, session_id: str):
        return list(self.db.scalars(
            select(AIConversation).where(AIConversation.session_id == session_id)
            .order_by(AIConversation.created_at)
        ))
