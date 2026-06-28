"""Dashboard repository (CP10): bulk reads for deterministic aggregation (no N+1)."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.operational.access import Teras
from app.models.operational.kpi import KPI, KPIMonthlyUpdate, RiskAssessment


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def teras_list(self) -> list[Teras]:
        return list(self.db.scalars(select(Teras).order_by(Teras.number)))

    def active_kpis(self) -> list[KPI]:
        return list(self.db.scalars(
            select(KPI).options(
                selectinload(KPI.indicators), selectinload(KPI.targets),
                selectinload(KPI.pic), selectinload(KPI.teras),
            ).where(KPI.is_deleted.is_(False))
        ))

    def latest_updates_by_kpi(self, kpi_ids: list[str]) -> dict[str, KPIMonthlyUpdate]:
        """Return the latest monthly update per KPI (by year, month, created_at)."""
        if not kpi_ids:
            return {}
        rows = self.db.scalars(
            select(KPIMonthlyUpdate).where(KPIMonthlyUpdate.kpi_id.in_(kpi_ids))
        )
        latest: dict[str, KPIMonthlyUpdate] = {}
        for u in rows:
            cur = latest.get(u.kpi_id)
            key = (u.reporting_year or 0, u.reporting_month or 0, u.created_at)
            if cur is None or key > (cur.reporting_year or 0, cur.reporting_month or 0, cur.created_at):
                latest[u.kpi_id] = u
        return latest

    def updates_for_period(self, kpi_ids: list[str], year: int, month: int) -> set[str]:
        """KPI ids that have a monthly update for the given period."""
        if not kpi_ids:
            return set()
        rows = self.db.scalars(
            select(KPIMonthlyUpdate.kpi_id).where(
                KPIMonthlyUpdate.kpi_id.in_(kpi_ids),
                KPIMonthlyUpdate.reporting_year == year,
                KPIMonthlyUpdate.reporting_month == month,
            )
        )
        return set(rows)

    def has_any_update(self, kpi_ids: list[str]) -> set[str]:
        if not kpi_ids:
            return set()
        return set(self.db.scalars(
            select(KPIMonthlyUpdate.kpi_id).where(KPIMonthlyUpdate.kpi_id.in_(kpi_ids))
        ))
