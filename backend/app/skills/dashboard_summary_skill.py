"""S14 Dashboard Summary Skill (CP12) — deterministic Teras roll-up summary text."""
from __future__ import annotations

from app.skills.base import Skill


class DashboardSummarySkill(Skill):
    name = "dashboard_summary"
    description = "Deterministic summary text from dashboard overview (AI-enhanced later)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        ov = payload.get("overview", payload)
        total = ov.get("total_kpis", 0)
        high = (ov.get("risk", {}) or {}).get("high", 0)
        missing = ov.get("missing_information", 0)
        by_teras = ov.get("by_teras", {}) or {}
        top = max(by_teras.items(), key=lambda kv: kv[1]) if by_teras else None
        text = (
            f"{total} KPIs tracked across Teras 1-7. {high} high-risk; {missing} incomplete."
            + (f" Teras {top[0]} has the most KPIs ({top[1]})." if top else "")
        )
        return {"generated_by": "deterministic", "text": text}
