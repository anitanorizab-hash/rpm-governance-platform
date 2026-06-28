"""KPI analysis service (CP8) — deterministic placeholder (AI-enhanced later).

Compares achievement vs target → achievement_status. Pure functions, independently testable.
"""
from __future__ import annotations

import re

ACHIEVED, ON_TRACK, AT_RISK, OFF_TRACK, NOT_UPDATED = (
    "achieved", "on_track", "at_risk", "off_track", "not_updated",
)


def parse_numeric(value) -> float | None:
    """Parse '85%', '1,200', '3' → float. Percentages become a 0–1 fraction."""
    if value is None:
        return None
    s = str(value).strip().replace(",", "")
    if not s:
        return None
    is_pct = "%" in s
    m = re.search(r"-?\d+(\.\d+)?", s)
    if not m:
        return None
    num = float(m.group())
    return num / 100.0 if is_pct else num


def ratio(achievement, target) -> float | None:
    a, t = parse_numeric(achievement), parse_numeric(target)
    if a is None or t in (None, 0):
        return None
    return a / t


def achievement_status(achievement, target) -> str:
    if achievement in (None, ""):
        return NOT_UPDATED
    r = ratio(achievement, target)
    if r is None:
        # have a value but no comparable target → treat as on_track (reported)
        return ON_TRACK
    if r >= 1.0:
        return ACHIEVED
    if r >= 0.8:
        return ON_TRACK
    if r >= 0.5:
        return AT_RISK
    return OFF_TRACK
