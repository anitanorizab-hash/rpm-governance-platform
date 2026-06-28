"""S4 Financial Decision Support Skill (CP12) — deterministic budget intelligence."""
from __future__ import annotations

from app.skills.base import Skill
from app.services.fds_service import FDSService


class FDSSkill(Skill):
    name = "fds"
    description = "Budget Intelligence: finance status → risk + funding-gap (deterministic)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        return FDSService.budget_intelligence(payload.get("finance_status"))
