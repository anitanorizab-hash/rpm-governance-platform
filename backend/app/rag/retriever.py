"""Retriever (CP14) — vector search when embeddings exist, else keyword fallback (V1)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.rag import keyword_search
from app.rag.vector_store import VECTOR_STORE


def retrieve(db: Session, query: str, top_k: int = 5) -> dict:
    """Return {mode, results[]}. Tries vector (if embeddings available), else keyword."""
    # Vector path (only if vectors exist AND an embedding provider is usable)
    if VECTOR_STORE.size() > 0:
        try:
            from app.providers.provider_factory import get_embedding_provider
            qvec = get_embedding_provider().embed([query])[0]
            vres = VECTOR_STORE.search(qvec, top_k=top_k)
            if vres:
                return {"mode": "vector", "results": vres}
        except Exception:
            pass  # fall through to keyword
    # Keyword fallback (always available)
    return {"mode": "keyword", "results": keyword_search.search(db, query, top_k=top_k)}
