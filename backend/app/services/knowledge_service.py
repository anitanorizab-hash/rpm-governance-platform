"""Knowledge service (CP14): create/process/list knowledge sources. Admin-gated at the route.

Operational/knowledge plane separation enforced — Pelan Taktikal is NEVER a knowledge source.
Embedding is best-effort; keyword search always works (BR-024/AD-006).
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.rag import chunker
from app.rag.vector_store import VECTOR_STORE
from app.repositories.knowledge_repository import KnowledgeRepository
from app.services import document_processing_service as dps
from app.services.audit_service import AuditService


class KnowledgeService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = KnowledgeRepository(db)
        self.audit = AuditService(db)

    def create_source(self, *, actor_id, data: dict, context: AuditContext | None = None):
        source = self.repo.create_source(
            type=data.get("type", "static"), title=data.get("title"),
            category=data.get("category"), reliability=data.get("reliability", "trusted"),
            status="active",
        )
        # store description on title note if provided (model has no description col → keep in title only)
        if data.get("content") is not None:
            text, err = dps.extract_text(fmt=data.get("format", "txt"), content=data["content"])
            self.repo.create_document(
                source_id=source.id, filename=data.get("filename", "upload"),
                format=data.get("format", "txt"), size=(len(text) if text else 0),
                content=text, extract_error=err, uploaded_by=actor_id,
            )
        self.audit.record(entity_type="knowledge_source", entity_id=source.id, action="knowledge_upload",
                          actor_id=actor_id, after={"title": data.get("title"), "type": source.type},
                          context=context, commit=False)
        self.db.commit()
        return self.repo.get_source(source.id)

    def list_sources(self):
        return self.repo.list_sources()

    def get_source(self, source_id):
        return self.repo.get_source(source_id)

    def process_source(self, *, actor_id, source_id, context: AuditContext | None = None):
        source = self.repo.get_source(source_id)
        if not source:
            return None
        doc = self.repo.get_document_for_source(source_id)
        if not doc or not doc.content:
            return {"error": doc.extract_error if doc else "No document/content to process",
                    "chunks": 0, "embedded": False}

        # rebuild chunks
        self.repo.delete_chunks_for_source(source_id)
        VECTOR_STORE.remove_source(source_id)
        pieces = chunker.chunk_text(doc.content)
        chunk_rows = [self.repo.create_chunk(source_id=source_id, document_id=doc.id,
                                             text=p, position=i) for i, p in enumerate(pieces)]

        # best-effort embedding (keyword search works regardless)
        embedded = False
        try:
            from app.providers.provider_factory import get_embedding_provider
            provider = get_embedding_provider()
            vectors = provider.embed([c.text for c in chunk_rows])
            for c, vec in zip(chunk_rows, vectors):
                VECTOR_STORE.add(c.id, vec, {"source_id": source_id, "title": source.title, "text": c.text})
                self.repo.create_embedding_meta(chunk_id=c.id, model=getattr(provider, "model", "unknown"),
                                                dimensions=len(vec), vector_ref=c.id)
            embedded = True
        except Exception:
            embedded = False  # embedding unavailable → keyword fallback only (do not fail)

        self.audit.record(entity_type="knowledge_source", entity_id=source_id, action="knowledge_process",
                          actor_id=actor_id, after={"chunks": len(chunk_rows), "embedded": embedded},
                          context=context, commit=False)
        self.db.commit()
        return {"source_id": source_id, "chunks": len(chunk_rows), "embedded": embedded,
                "mode": "vector" if embedded else "keyword"}
