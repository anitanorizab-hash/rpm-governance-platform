"""Reference seed data (CP3) — roles, Teras 1–7, budget statuses, amendment windows.

Idempotent: safe to run repeatedly. NO real KPI data is seeded.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operational.access import BudgetStatus, Role, Teras
from app.models.operational.governance import AmendmentWindow

ROLES = [
    ("super_admin", "Platform governance"),
    ("jpn_admin", "State-level administrator"),
    ("sector_admin", "Sector/Bahagian administrator"),
    ("ppd_admin", "District administrator"),
    ("kpi_pic", "KPI Person-in-Charge"),
    ("finance_officer", "Finance/budget officer"),
    ("executive", "Executive management"),
    ("read_only", "Read-only user"),
    ("internal_audit", "Internal audit / oversight"),
]

TERAS = [
    (1, "Teras 1"), (2, "Teras 2"), (3, "Teras 3"), (4, "Teras 4"),
    (5, "Teras 5"), (6, "Teras 6"), (7, "Teras 7"),
]

BUDGET_STATUSES = [
    ("received", "Received"),
    ("will_be_received", "Will be received"),
    ("pending", "Pending"),
    ("not_received", "Not received"),
    ("not_required", "Not required"),
    ("insufficient", "Insufficient"),
]

# Amendment windows: July (7) and October (10). Seed for the RPM start year.
AMENDMENT_WINDOWS = [(2026, 7), (2026, 10)]


def _uid() -> str:
    return str(uuid.uuid4())


def _now():
    return datetime.now(timezone.utc)


def seed_reference_data(session: Session) -> dict:
    """Insert reference rows if missing. Returns counts inserted."""
    counts = {"roles": 0, "teras": 0, "budget_status": 0, "amendment_windows": 0}

    for name, desc in ROLES:
        if not session.scalar(select(Role).where(Role.name == name)):
            session.add(Role(id=_uid(), name=name, description=desc,
                             created_at=_now(), updated_at=_now()))
            counts["roles"] += 1

    for number, name in TERAS:
        if not session.scalar(select(Teras).where(Teras.number == number)):
            session.add(Teras(id=_uid(), number=number, name=name,
                              created_at=_now(), updated_at=_now()))
            counts["teras"] += 1

    for code, label in BUDGET_STATUSES:
        if not session.scalar(select(BudgetStatus).where(BudgetStatus.code == code)):
            session.add(BudgetStatus(id=_uid(), code=code, label=label,
                                     created_at=_now(), updated_at=_now()))
            counts["budget_status"] += 1

    for year, month in AMENDMENT_WINDOWS:
        exists = session.scalar(
            select(AmendmentWindow).where(
                AmendmentWindow.year == year, AmendmentWindow.month == month
            )
        )
        if not exists:
            session.add(AmendmentWindow(id=_uid(), year=year, month=month, is_open=False,
                                        created_at=_now(), updated_at=_now()))
            counts["amendment_windows"] += 1

    session.commit()
    return counts
