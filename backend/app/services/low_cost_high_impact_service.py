"""Low Cost High Impact Analysis (CP11) — deterministic Matrix (BR-011/046). No AI."""
from __future__ import annotations

from app.services import kpi_analysis_service as analysis

COST_HIGH_THRESHOLD = 50_000.0   # RM; configurable later

QUADRANTS = {
    ("low", "high"): "Priority Action",
    ("low", "low"): "Optional / Quick Win",
    ("high", "high"): "Strategic Investment",
    ("high", "low"): "Avoid / Redesign",
}

_ALTERNATIVES = {
    "Priority Action": ["Proceed; protect funding", "Scale via existing channels"],
    "Optional / Quick Win": ["Deliver digitally / low-cost", "Bundle with related activities"],
    "Strategic Investment": ["Phase delivery to spread cost", "Seek collaboration / shared resources"],
    "Avoid / Redesign": ["Redesign to lower cost", "Consolidate with overlapping programmes",
                          "Consider digital alternatives or discontinue"],
}

_OPTIMISATION = {
    "Priority Action": "Maintain; monitor cost efficiency.",
    "Optional / Quick Win": "Use shared resources and digital delivery to keep cost minimal.",
    "Strategic Investment": "Optimise via programme consolidation, shared venues/trainers, phasing.",
    "Avoid / Redesign": "High cost for low impact — redesign, collaborate, or reallocate budget.",
}


def cost_level(cost_total: float) -> str:
    return "high" if (cost_total or 0) >= COST_HIGH_THRESHOLD else "low"


def impact_level(achievement, target) -> str:
    r = analysis.ratio(achievement, target)
    if r is None:
        # no comparable data → conservative low impact (flag for review)
        return "low"
    return "high" if r >= 0.5 else "low"


def analyze(*, cost_total: float, achievement, target) -> dict:
    c = cost_level(cost_total)
    i = impact_level(achievement, target)
    quadrant = QUADRANTS[(c, i)]
    return {
        "cost_level": c,
        "impact_level": i,
        "quadrant": quadrant,
        "cost_total": float(cost_total or 0),
        "low_cost_alternatives": _ALTERNATIVES[quadrant],
        "resource_optimisation_notes": _OPTIMISATION[quadrant],
    }
