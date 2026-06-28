"""S1 KPI Analysis Skill (CP12) — deterministic. Wraps kpi_analysis_service."""
from __future__ import annotations

from app.skills.base import Skill
from app.services import kpi_analysis_service as svc


class KPIAnalysisSkill(Skill):
    name = "kpi_analysis"
    description = "Classify achievement status vs target (deterministic)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        achievement = payload.get("achievement")
        target = payload.get("target")
        return {
            "achievement_status": svc.achievement_status(achievement, target),
            "ratio": svc.ratio(achievement, target),
        }
