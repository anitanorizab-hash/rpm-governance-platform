"""KPI Analysis Agent (CP13) — composes the kpi_analysis skill."""
from __future__ import annotations

from app.agents.base import Agent


class KPIAnalysisAgent(Agent):
    name = "kpi_analysis"
    description = "Classify KPI achievement status vs target."
    uses_skills = ["kpi_analysis"]

    def run(self, context: dict) -> dict:
        out = self.skill("kpi_analysis", {"achievement": context.get("achievement"),
                                          "target": context.get("target")})
        return self._wrap({"analysis": out})
