"""OBB Analysis (CP11) — deterministic outcome-based budgeting value-for-money. No AI."""
from __future__ import annotations

from app.services import kpi_analysis_service as analysis


def analyze(*, kpi, cost_total: float, expenditure: float, achievement, target,
            cost_level: str, impact_level: str) -> dict:
    """Outcome achieved vs resource used → value-for-money + outcome risk."""
    r = analysis.ratio(achievement, target)

    # value for money + outcome risk from cost vs impact
    if cost_level == "high" and impact_level == "low":
        vfm, outcome_risk = "low", "high"
    elif cost_level == "low" and impact_level == "high":
        vfm, outcome_risk = "high", "low"
    else:
        vfm, outcome_risk = "moderate", "medium"

    expected_outcome = kpi.keberhasilan or kpi.statement or "Outcome per KPI definition"
    resource_use = (
        f"Allocation RM{cost_total:,.0f}; expenditure RM{expenditure:,.0f}."
        if cost_total or expenditure else "No allocation recorded."
    )
    return {
        "expected_outcome": expected_outcome,
        "resource_use": resource_use,
        "achievement_ratio": (round(r, 2) if r is not None else None),
        "value_for_money": vfm,
        "outcome_risk": outcome_risk,
        "optimisation_opportunity": (cost_level == "low" and impact_level == "high"),
    }
