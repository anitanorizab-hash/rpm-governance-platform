"""S7 Strategic Recommendation Skill (CP12) — deterministic advisory draft."""
from __future__ import annotations

from app.skills.base import Skill
from app.services import strategic_recommendation_service as strat


class StrategicRecommendationSkill(Skill):
    name = "strategic_recommendation"
    description = "Draft advisory recommendation (action/rationale/priority; human-review required)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        return strat.build(
            finance_risk=payload.get("finance_risk", "medium"),
            funding_gap=payload.get("funding_gap", False),
            quadrant=payload.get("quadrant", "Optional / Quick Win"),
            vfm=payload.get("vfm", "moderate"),
        )
