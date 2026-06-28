"""Risk Assessment Agent (CP13) — composes the risk_scoring skill."""
from __future__ import annotations

from app.agents.base import Agent


class RiskAssessmentAgent(Agent):
    name = "risk_assessment"
    description = "Assess KPI risk level + reason."
    uses_skills = ["risk_scoring"]

    def run(self, context: dict) -> dict:
        out = self.skill("risk_scoring", {"achievement": context.get("achievement"),
                                          "target": context.get("target"),
                                          "status": context.get("status")})
        return self._wrap({"risk": out})
