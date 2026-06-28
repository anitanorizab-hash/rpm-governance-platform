"""Report Generation Agent (CP17) — composes report_writing + dashboard_summary + citation_grounding
+ ralph_loop_review. Produces an advisory DRAFT only (never issues/distributes)."""
from __future__ import annotations

from app.agents.base import Agent


class ReportGenerationAgent(Agent):
    name = "report_generation"
    description = "Draft a monthly report (human review + CP9 approval required before issue)."
    uses_skills = ["report_writing", "dashboard_summary", "citation_grounding", "ralph_loop_review"]
    human_review_required = True

    def run(self, context: dict) -> dict:
        period = context.get("period", "the period")
        stats = context.get("stats", {})
        overview = context.get("overview", {})
        sources = context.get("sources", [])

        summary = self.skill("dashboard_summary", {"overview": overview})
        writing = self.skill("report_writing", {"period": period, "stats": stats})
        grounded = self.skill("citation_grounding", {"answer": writing["draft"], "sources": sources})
        ralph = self.skill("ralph_loop_review", {
            "text": writing["draft"], "citations": grounded["citations"],
            "advisory_only": True, "human_review_required": True, "actionable": False,
            "requires_citation": False,   # aggregate report; citations optional
        })
        return self._wrap({
            "narrative": writing["draft"],
            "summary": summary["text"],
            "citations": grounded["citations"],
            "ralph_review": ralph,
            "issued": False,           # never auto-issued
        })
