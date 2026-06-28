"""AI metadata models (CP3) — AI plane (logging / observability).

AgentExecution, SkillExecution, ChatSession, AIConversation, AIRecommendation, AICostLog, ProviderUsage.
These log advisory AI activity; they are NOT the operational system of record.
"""
from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin, fk_uuid, uuid_pk


class AgentExecution(Base, TimestampMixin):
    __tablename__ = "agent_execution"
    id = uuid_pk()
    agent_name = Column(String(64), nullable=False)
    trigger = Column(String(64))
    inputs_ref = Column(Text)
    outputs_ref = Column(Text)
    status = Column(String(16))
    started_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))
    skills = relationship("SkillExecution", back_populates="agent_execution")
    costs = relationship("AICostLog", back_populates="agent_execution")


class SkillExecution(Base, TimestampMixin):
    __tablename__ = "skill_execution"
    id = uuid_pk()
    skill_name = Column(String(64), nullable=False)
    version = Column(String(32))
    agent_execution_id = fk_uuid("agent_execution.id")
    inputs_ref = Column(Text)
    outputs_ref = Column(Text)
    agent_execution = relationship("AgentExecution", back_populates="skills")


class ChatSession(Base, TimestampMixin):
    __tablename__ = "chat_session"
    id = uuid_pk()
    user_id = fk_uuid("user.id")
    started_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))
    conversations = relationship("AIConversation", back_populates="session")


class AIConversation(Base, TimestampMixin):
    __tablename__ = "ai_conversation"
    id = uuid_pk()
    session_id = fk_uuid("chat_session.id")
    user_id = fk_uuid("user.id")
    question = Column(Text)
    answer_ref = Column(Text)
    grounded = Column(Boolean, default=False)
    fallback = Column(Boolean, default=False)
    session = relationship("ChatSession", back_populates="conversations")


class AIRecommendation(Base, TimestampMixin):
    """Raw, advisory AI output (log). Operational record = StrategicRecommendation (linked)."""
    __tablename__ = "ai_recommendation"
    id = uuid_pk()
    type = Column(String(32))
    content = Column(Text)
    rationale = Column(Text)
    linked_entity = Column(String(128))
    provider = Column(String(32))
    model = Column(String(64))
    status = Column(String(16), default="draft")


class AICostLog(Base, TimestampMixin):
    __tablename__ = "ai_cost_log"
    id = uuid_pk()
    agent_execution_id = fk_uuid("agent_execution.id")
    provider = Column(String(32))
    model = Column(String(64))
    tokens_in = Column(Integer)
    tokens_out = Column(Integer)
    cost = Column(Float)
    latency_ms = Column(Integer)
    agent_execution = relationship("AgentExecution", back_populates="costs")


class ProviderUsage(Base, TimestampMixin):
    __tablename__ = "provider_usage"
    id = uuid_pk()
    provider = Column(String(32))
    mode = Column(String(16))      # dev | prod
    period = Column(String(7))
    calls = Column(Integer, default=0)
    tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
