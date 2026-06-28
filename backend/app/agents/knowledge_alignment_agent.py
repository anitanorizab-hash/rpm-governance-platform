"""Knowledge Alignment Agent (CP14) — RPM alignment + RAG context (real retrieval when db present)."""
from __future__ import annotations

from app.agents.base import Agent


class KnowledgeAlignmentAgent(Agent):
    name = "knowledge_alignment"
    description = "Map KPI to RPM 2026-2035 + alignment strength, grounded by RAG context."
    uses_skills = ["rpm_alignment", "rag_retrieval"]

    def run(self, context: dict) -> dict:
        statement = context.get("kpi_statement") or context.get("statement") or ""
        db = context.get("_db")
        align = self.skill("rpm_alignment", {"kpi_statement": statement})
        rpm_context = []
        if db is not None and statement:
            rpm_context = self.skill("rag_retrieval", {"query": statement, "db": db}).get("results", [])
        return self._wrap({"alignment": align, "rpm_context_count": len(rpm_context),
                           "rpm_citations": [{"title": r.get("title"), "source_id": r.get("source_id")}
                                             for r in rpm_context]})
