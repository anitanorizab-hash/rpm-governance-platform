"""S3 Risk Scoring Skill (CP12) — deterministic. Wraps risk_service."""
from __future__ import annotations

from app.skills.base import Skill
from app.services import risk_service


class RiskScoringSkill(Skill):
    name = "risk_scoring"
    description = "Compute risk level + reason from achievement vs target (deterministic)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        return risk_service.assess(payload.get("achievement"), payload.get("target"),
                                   payload.get("status"))
