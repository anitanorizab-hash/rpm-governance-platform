"""FDS repository (CP11): financial reads + recommendation persistence."""
from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.operational.finance import (
    FinancialAllocation, LowCostHighImpactAnalysis, OBBAnalysis, StrategicRecommendation,
)
from app.models.operational.kpi import KPI, KPIMonthlyUpdate


def _uid() -> str:
    return str(uuid.uuid4())


class FDSRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_kpi(self, kpi_id: str) -> KPI | None:
        kpi = self.db.scalar(
            select(KPI).options(selectinload(KPI.targets), selectinload(KPI.pic),
                                selectinload(KPI.teras), selectinload(KPI.activities)).where(KPI.id == kpi_id)
        )
        return kpi if (kpi and not kpi.is_deleted) else None

    def allocation_totals(self, kpi_id: str) -> tuple[float, float]:
        amount = self.db.scalar(
            select(func.coalesce(func.sum(FinancialAllocation.amount), 0.0))
            .where(FinancialAllocation.kpi_id == kpi_id)
        ) or 0.0
        expenditure = self.db.scalar(
            select(func.coalesce(func.sum(FinancialAllocation.expenditure), 0.0))
            .where(FinancialAllocation.kpi_id == kpi_id)
        ) or 0.0
        return float(amount), float(expenditure)

    def latest_update(self, kpi_id: str) -> KPIMonthlyUpdate | None:
        rows = self.db.scalars(select(KPIMonthlyUpdate).where(KPIMonthlyUpdate.kpi_id == kpi_id))
        latest = None
        for u in rows:
            key = (u.reporting_year or 0, u.reporting_month or 0, u.created_at)
            if latest is None or key > (latest.reporting_year or 0, latest.reporting_month or 0, latest.created_at):
                latest = u
        return latest

    def create_recommendation(self, **kw) -> StrategicRecommendation:
        rec = StrategicRecommendation(id=_uid(), **kw)
        self.db.add(rec); self.db.flush()
        return rec

    def get_recommendation(self, rec_id: str) -> StrategicRecommendation | None:
        return self.db.get(StrategicRecommendation, rec_id)

    def list_recommendations(self, *, kpi_id=None, limit=100, offset=0):
        stmt = select(StrategicRecommendation)
        if kpi_id:
            stmt = stmt.where(StrategicRecommendation.kpi_id == kpi_id)
        stmt = stmt.order_by(StrategicRecommendation.created_at.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(stmt))

    def create_obb(self, **kw) -> OBBAnalysis:
        row = OBBAnalysis(id=_uid(), **kw); self.db.add(row); self.db.flush(); return row

    def create_lchi(self, **kw) -> LowCostHighImpactAnalysis:
        row = LowCostHighImpactAnalysis(id=_uid(), **kw); self.db.add(row); self.db.flush(); return row

    def all_kpis_active(self):
        return list(self.db.scalars(select(KPI).where(KPI.is_deleted.is_(False))))
