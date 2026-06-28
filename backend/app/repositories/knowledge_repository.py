"""Knowledge repository (CP14): CRUD for knowledge plane entities."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.knowledge.knowledge import (
    Chunk, Citation, Document, EmbeddingMetadata, KnowledgeSource, LiveLink,
)


def _uid() -> str:
    return str(uuid.uuid4())


class KnowledgeRepository:
    def __init__(self, db: Session):
        self.db = db

    # sources
    def create_source(self, **kw) -> KnowledgeSource:
        s = KnowledgeSource(id=_uid(), **kw); self.db.add(s); self.db.flush(); return s

    def get_source(self, source_id: str) -> KnowledgeSource | None:
        return self.db.get(KnowledgeSource, source_id)

    def list_sources(self, limit=100, offset=0):
        return list(self.db.scalars(
            select(KnowledgeSource).order_by(KnowledgeSource.created_at.desc()).limit(limit).offset(offset)
        ))

    def set_status(self, source: KnowledgeSource, status: str, validated_by: str | None = None):
        source.status = status
        if validated_by:
            source.validated_by = validated_by
        self.db.flush()

    # documents
    def create_document(self, **kw) -> Document:
        d = Document(id=_uid(), **kw); self.db.add(d); self.db.flush(); return d

    def get_document_for_source(self, source_id: str) -> Document | None:
        return self.db.scalar(select(Document).where(Document.source_id == source_id))

    # chunks
    def create_chunk(self, *, source_id, document_id, text, position) -> Chunk:
        c = Chunk(id=_uid(), source_id=source_id, document_id=document_id, text=text, position=position)
        self.db.add(c); self.db.flush(); return c

    def get_chunk(self, chunk_id: str) -> Chunk | None:
        return self.db.get(Chunk, chunk_id)

    def delete_chunks_for_source(self, source_id: str):
        for c in self.db.scalars(select(Chunk).where(Chunk.source_id == source_id)):
            self.db.delete(c)
        self.db.flush()

    # embeddings
    def create_embedding_meta(self, *, chunk_id, model, dimensions, vector_ref) -> EmbeddingMetadata:
        e = EmbeddingMetadata(id=_uid(), chunk_id=chunk_id, model=model,
                              dimensions=dimensions, vector_ref=vector_ref)
        self.db.add(e); self.db.flush(); return e

    # live links
    def create_live_link(self, *, source_id, url, refresh_schedule=None) -> LiveLink:
        link = LiveLink(id=_uid(), source_id=source_id, url=url, refresh_schedule=refresh_schedule,
                        status="active", last_checked=datetime.now(timezone.utc))
        self.db.add(link); self.db.flush(); return link

    def get_live_link(self, link_id: str) -> LiveLink | None:
        return self.db.get(LiveLink, link_id)

    # citations
    def create_citation(self, *, chunk_id, source_id, conversation_id=None) -> Citation:
        c = Citation(id=_uid(), chunk_id=chunk_id, source_id=source_id, conversation_id=conversation_id)
        self.db.add(c); self.db.flush(); return c
