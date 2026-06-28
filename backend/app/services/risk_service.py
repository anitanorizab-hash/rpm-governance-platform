"""Risk service (CP8) — deterministic placeholder (AI-enhanced later).

Maps achievement status / ratio → risk level + reason. Pure functions, independently testable.
"""
from __future__ import annotations

from app.services import kpi_analysis_service as analysis

LOW, MEDIUM, HIGH = "low", "medium", "high"


def assess(achievement, target, status: str | None = None) -> dict:
    status = status or analysis.achievement_status(achievement, target)
    r = analysis.ratio(achievement, target)
    if status == analysis.ACHIEVED:
        return {"risk_level": LOW, "risk_reason": "Target achieved."}
    if status == analysis.ON_TRACK:
        return {"risk_level": LOW, "risk_reason": "On track toward target."}
    if status == analysis.AT_RISK:
        return {"risk_level": MEDIUM,
                "risk_reason": f"Achievement below 80% of target (ratio={round(r, 2) if r else 'n/a'})."}
    if status == analysis.OFF_TRACK:
        return {"risk_level": HIGH,
                "risk_reason": f"Achievement below 50% of target (ratio={round(r, 2) if r else 'n/a'})."}
    # not_updated
    return {"risk_level": MEDIUM, "risk_reason": "No achievement reported for the period."}
