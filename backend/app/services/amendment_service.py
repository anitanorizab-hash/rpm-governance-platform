"""Amendment-window service (CP7): KPI statement/indicator/target editable only in July & October (BR-008).

Outside the window, changes are blocked unless an explicit Super Admin override is provided.
`_current_month()` is isolated so tests can monkeypatch it deterministically.
"""
from __future__ import annotations

from datetime import datetime, timezone

# Fields under amendment control (BR-008).
AMENDABLE_FIELDS = {"statement", "indicator", "target"}
AMENDMENT_MONTHS = {7, 10}   # July, October


def _current_month() -> int:
    return datetime.now(timezone.utc).month


def is_window_open(month: int | None = None) -> bool:
    return (month if month is not None else _current_month()) in AMENDMENT_MONTHS


def changed_amendable_fields(patch: dict) -> list[str]:
    return [f for f in patch if f in AMENDABLE_FIELDS and patch[f] is not None]


def amendment_allowed(patch: dict, *, is_super_admin: bool, override: bool) -> tuple[bool, str | None]:
    """Return (allowed, reason_if_blocked) for the amendable fields in a patch."""
    amendable = changed_amendable_fields(patch)
    if not amendable:
        return True, None
    if is_window_open():
        return True, None
    if override and is_super_admin:
        return True, None
    return False, (
        f"Amendment of {amendable} is only allowed in July and October "
        f"(BR-008). Super Admin override required outside the window."
    )
