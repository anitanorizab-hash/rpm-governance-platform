"""S6 OBB Analysis Skill (CP12) — deterministic value-for-money."""
from __future__ import annotations

from types import SimpleNamespace

from app.skills.base import Skill
from app.services import obb_service


class OBBAnalysisSkill(Skill):
    name = "obb_analysis"
    description = "Outcome-based budgeting value-for-money (deterministic)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        kpi = SimpleNamespace(keberhasilan=payload.get("expected_outcome"),
                              statement=payload.get("statement"))
        return obb_service.analyze(
            kpi=kpi, cost_total=payload.get("cost_total", 0.0),
            expenditure=payload.get("expenditure", 0.0),
            achievement=payload.get("achievement"), target=payload.get("target"),
            cost_level=payload.get("cost_level", "low"),
            impact_level=payload.get("impact_level", "low"),
        )
