"""RAG service (CP14): retrieval + grounded answer with citations + fixed fallback.

Knowledge plane only — never modifies operational data. Logs retrievals and failed retrievals.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.rag import retriever
from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.audit_service import AuditService

FALLBACK = "I cannot find this information in the available KPI data or knowledge sources."


class RAGService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = KnowledgeRepository(db)
        self.audit = AuditService(db)

    def retrieve(self, query: str, top_k: int = 5) -> dict:
        """Return {mode, results[]} — read-only on the knowledge plane."""
        return retriever.retrieve(self.db, query, top_k=top_k)

    def query(self, *, query: str, actor_id=None, top_k: int = 5,
              context: AuditContext | None = None) -> dict:
        r = self.retrieve(query, top_k=top_k)
        results = r["results"]
        if not results:
            self.audit.record(entity_type="knowledge_query", action="retrieval_failed",
                              actor_id=actor_id, after={"query": query, "mode": r["mode"]},
                              context=context, commit=True)
            return {"query": query, "grounded": False, "fallback": True,
                    "answer": FALLBACK, "citations": [], "mode": r["mode"]}

        top = results[0]
        snippet = (top["text"] or "")[:500]
        citations = [{"title": x.get("title"), "source_id": x.get("source_id"),
                      "chunk_id": x.get("chunk_id")} for x in results]
        # record citations + a successful retrieval
        for c in citations:
            if c.get("chunk_id") and c.get("source_id"):
                self.repo.create_citation(chunk_id=c["chunk_id"], source_id=c["source_id"])
        self.audit.record(entity_type="knowledge_query", action="retrieval",
                          actor_id=actor_id,
                          after={"query": query, "mode": r["mode"], "hits": len(results)},
                          context=context, commit=True)
        return {"query": query, "grounded": True, "fallback": False,
                "answer": snippet, "citations": citations, "mode": r["mode"]}
