"""Monthly update repository (CP8)."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operational.kpi import KPIMonthlyUpdate, RiskAssessment


def _uid() -> str:
    return str(uuid.uuid4())


class MonthlyUpdateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, update_id: str) -> KPIMonthlyUpdate | None:
        return self.db.get(KPIMonthlyUpdate, update_id)

    def find_for_period(self, kpi_id: str, year: int, month: int) -> KPIMonthlyUpdate | None:
        return self.db.scalar(
            select(KPIMonthlyUpdate).where(
                KPIMonthlyUpdate.kpi_id == kpi_id,
                KPIMonthlyUpdate.reporting_year == year,
                KPIMonthlyUpdate.reporting_month == month,
            )
        )

    def list(self, *, kpi_id=None, year=None, month=None, limit=100, offset=0):
        stmt = select(KPIMonthlyUpdate)
        if kpi_id:
            stmt = stmt.where(KPIMonthlyUpdate.kpi_id == kpi_id)
        if year:
            stmt = stmt.where(KPIMonthlyUpdate.reporting_year == year)
        if month:
            stmt = stmt.where(KPIMonthlyUpdate.reporting_month == month)
        stmt = stmt.order_by(KPIMonthlyUpdate.reporting_year.desc(),
                             KPIMonthlyUpdate.reporting_month.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(stmt))

    def list_all(self):
        return list(self.db.scalars(select(KPIMonthlyUpdate)))

    def create(self, **kw) -> KPIMonthlyUpdate:
        upd = KPIMonthlyUpdate(id=_uid(), **kw)
        self.db.add(upd); self.db.flush()
        return upd

    def add_risk(self, *, kpi_id: str, period: str, risk_level: str) -> RiskAssessment:
        ra = RiskAssessment(id=_uid(), kpi_id=kpi_id, period=period,
                            risk_level=risk_level, method="rule-based")
        self.db.add(ra); self.db.flush()
        return ra
