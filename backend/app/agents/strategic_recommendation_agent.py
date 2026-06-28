"""Strategic Recommendation Agent (CP13) — composes the strategic_recommendation skill. Advisory + HITL."""
from __future__ import annotations

from app.agents.base import Agent


class StrategicRecommendationAgent(Agent):
    name = "strategic_recommendation"
    description = "Draft an advisory intervention recommendation (human review required)."
    uses_skills = ["strategic_recommendation"]
    human_review_required = True

    def run(self, context: dict) -> dict:
        out = self.skill("strategic_recommendation", {
            "finance_risk": context.get("finance_risk", "medium"),
            "funding_gap": context.get("funding_gap", False),
            "quadrant": context.get("quadrant", "Optional / Quick Win"),
            "vfm": context.get("vfm", "moderate"),
        })
        return self._wrap({"recommendation": out})
