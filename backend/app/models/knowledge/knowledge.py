"""Knowledge metadata models (CP3) — KNOWLEDGE plane (separate from operational).

KnowledgeSource, Document, LiveLink, Chunk, EmbeddingMetadata, Citation, RefreshHistory.
Vectors live in the vector store (Chroma/pgvector); only metadata is modelled here.
Pelan Taktikal is NEVER a knowledge source (operational only).
"""
from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin, fk_uuid, uuid_pk


class KnowledgeSource(Base, TimestampMixin):
    __tablename__ = "knowledge_source"
    id = uuid_pk()
    type = Column(String(16), nullable=False)    # static | live
    title = Column(String(512))
    category = Column(String(64))                # rpm | guideline | circular | note | policy
    reliability = Column(String(32))             # official | trusted | unverified
    status = Column(String(16), default="active")
    validated_by = fk_uuid("user.id")
    documents = relationship("Document", back_populates="source")
    links = relationship("LiveLink", back_populates="source")
    chunks = relationship("Chunk", back_populates="source")


class Document(Base, TimestampMixin):
    __tablename__ = "document"
    id = uuid_pk()
    source_id = fk_uuid("knowledge_source.id", nullable=False)
    filename = Column(String(512))
    format = Column(String(16))                  # PDF | DOCX | TXT | MD
    size = Column(Integer)
    content = Column(Text)                       # extracted text (CP14)
    extract_error = Column(String(512))          # set if extraction failed
    uploaded_by = fk_uuid("user.id")
    source = relationship("KnowledgeSource", back_populates="documents")


class LiveLink(Base, TimestampMixin):
    __tablename__ = "live_link"
    id = uuid_pk()
    source_id = fk_uuid("knowledge_source.id", nullable=False)
    url = Column(String(1024), nullable=False)
    last_checked = Column(DateTime(timezone=True))
    refresh_schedule = Column(String(32))
    status = Column(String(16), default="active")  # active | unreachable
    source = relationship("KnowledgeSource", back_populates="links")
    refresh_history = relationship("RefreshHistory", back_populates="link")


class Chunk(Base, TimestampMixin):
    __tablename__ = "chunk"
    id = uuid_pk()
    source_id = fk_uuid("knowledge_source.id", nullable=False)
    document_id = fk_uuid("document.id")
    text = Column(Text)
    position = Column(Integer)
    chunk_metadata = Column(Text)                # JSON metadata
    source = relationship("KnowledgeSource", back_populates="chunks")
    embedding = relationship("EmbeddingMetadata", back_populates="chunk", uselist=False)


class EmbeddingMetadata(Base, TimestampMixin):
    __tablename__ = "embedding_metadata"
    id = uuid_pk()
    chunk_id = fk_uuid("chunk.id", nullable=False)
    model = Column(String(128))
    dimensions = Column(Integer)
    vector_ref = Column(String(128))             # id/ref in the vector store
    chunk = relationship("Chunk", back_populates="embedding")


class Citation(Base, TimestampMixin):
    __tablename__ = "citation"
    id = uuid_pk()
    conversation_id = fk_uuid("ai_conversation.id")
    chunk_id = fk_uuid("chunk.id")
    source_id = fk_uuid("knowledge_source.id")


class RefreshHistory(Base, TimestampMixin):
    __tablename__ = "refresh_history"
    id = uuid_pk()
    link_id = fk_uuid("live_link.id", nullable=False)
    checked_at = Column(DateTime(timezone=True))
    status = Column(String(16))
    changed = Column(Boolean, default=False)
    link = relationship("LiveLink", back_populates="refresh_history")
