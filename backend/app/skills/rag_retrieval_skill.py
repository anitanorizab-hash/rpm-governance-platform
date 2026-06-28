"""S9 RAG Retrieval Skill (CP14) — calls rag_service when a db session is supplied; placeholder otherwise."""
from __future__ import annotations

from app.skills.base import Skill


class RAGRetrievalSkill(Skill):
    name = "rag_retrieval"
    description = "Retrieve grounding chunks via rag_service (vector/keyword); placeholder without db."
    deterministic = False
    uses_provider = True   # vector path uses embedding(); keyword fallback otherwise

    def run(self, payload: dict) -> dict:
        query = payload.get("query", "")
        db = payload.get("db") or payload.get("_db")
        if db is None:
            return {"query": query, "results": [], "mode": "placeholder",
                    "note": "No db/corpus supplied; RAG retrieval requires a session."}
        from app.services.rag_service import RAGService
        r = RAGService(db).retrieve(query)
        return {"query": query, "results": r["results"], "mode": r["mode"]}
