"""S11 Report Writing Skill (CP12) — AI-assisted with deterministic fallback. Draft only."""
from __future__ import annotations

from app.skills.base import Skill, safe_chat


class ReportWritingSkill(Skill):
    name = "report_writing"
    description = "Draft monthly report narrative (AI via adapter; template fallback)."
    deterministic = False
    uses_provider = True

    def run(self, payload: dict) -> dict:
        period = payload.get("period", "the period")
        stats = payload.get("stats", {})
        template = (
            f"Monthly KPI Report — {period}. "
            f"Total KPIs: {stats.get('total_kpis', 'n/a')}; "
            f"high-risk: {stats.get('high_risk', 'n/a')}; "
            f"incomplete: {stats.get('missing_information', 'n/a')}. (Draft — human review required.)"
        )
        result = safe_chat(
            [{"role": "user", "content": f"Write a concise monthly KPI report for {period}: {stats}"}],
            fallback=template,
        )
        return {"draft": result["text"], "source": result["source"], "human_review_required": True}
