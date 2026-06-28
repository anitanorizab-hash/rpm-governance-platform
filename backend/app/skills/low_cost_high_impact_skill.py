"""S5 Low Cost High Impact Skill (CP12) — deterministic matrix."""
from __future__ import annotations

from app.skills.base import Skill
from app.services import low_cost_high_impact_service as lchi


class LowCostHighImpactSkill(Skill):
    name = "low_cost_high_impact"
    description = "Cost×impact matrix quadrant + alternatives (deterministic)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        return lchi.analyze(cost_total=payload.get("cost_total", 0.0),
                            achievement=payload.get("achievement"),
                            target=payload.get("target"))
