"""S10 Citation & Source Grounding Skill (CP12) — deterministic; enforces BR-025/027."""
from __future__ import annotations

from app.skills.base import Skill

FALLBACK = "I cannot find this information in the available KPI data or knowledge sources."


class CitationGroundingSkill(Skill):
    name = "citation_grounding"
    description = "Attach source citations; emit fixed fallback when ungrounded (deterministic)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        answer = payload.get("answer")
        sources = payload.get("sources") or []
        if not answer or not sources:
            return {"grounded": False, "answer": FALLBACK, "citations": [], "fallback": True}
        citations = [{"title": s.get("title"), "source_id": s.get("source_id"),
                      "chunk_id": s.get("chunk_id"), "ref": s.get("ref")} for s in sources]
        return {"grounded": True, "answer": answer, "citations": citations, "fallback": False}
