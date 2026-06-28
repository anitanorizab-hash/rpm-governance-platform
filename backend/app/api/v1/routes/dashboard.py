"""Dashboard API (A6 G6) — CP10. Deterministic Teras 1–7 aggregation; JWT; role-scoped. No AI."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.dashboard import (
    BudgetSummaryOut, ExecutiveSummaryOut, HighRiskKPIItem, KPIMappingRow,
    OverviewOut, PPDComparisonOut, RiskSummaryOut, SubmissionSummaryOut, TerasSummaryItem,
)
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _svc(db):
    return DashboardService(db)


# V1.1: optional organisation_id scopes any view to a single org (JPN overall, or one PPD).
@router.get("/overview", response_model=OverviewOut)
def overview(organisation_id: str | None = Query(default=None),
             current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).overview(current_user, organisation_id=organisation_id)


@router.get("/teras-summary", response_model=list[TerasSummaryItem])
def teras_summary(organisation_id: str | None = Query(default=None),
                  current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).teras_summary(current_user, organisation_id=organisation_id)


@router.get("/risk-summary", response_model=RiskSummaryOut)
def risk_summary(organisation_id: str | None = Query(default=None),
                 current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).risk_summary(current_user, organisation_id=organisation_id)


@router.get("/budget-summary", response_model=BudgetSummaryOut)
def budget_summary(organisation_id: str | None = Query(default=None),
                   current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).budget_summary(current_user, organisation_id=organisation_id)


@router.get("/submission-summary", response_model=SubmissionSummaryOut)
def submission_summary(year: int | None = Query(default=None), month: int | None = Query(default=None),
                       organisation_id: str | None = Query(default=None),
                       current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).submission_summary(current_user, year=year, month=month,
                                       organisation_id=organisation_id)


@router.get("/high-risk-kpis", response_model=list[HighRiskKPIItem])
def high_risk_kpis(organisation_id: str | None = Query(default=None),
                   current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).high_risk_kpis(current_user, organisation_id=organisation_id)


@router.get("/kpi-mapping", response_model=list[KPIMappingRow])
def kpi_mapping(organisation_id: str | None = Query(default=None),
                current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).kpi_mapping(current_user, organisation_id=organisation_id)


@router.get("/executive-summary", response_model=ExecutiveSummaryOut)
def executive_summary(organisation_id: str | None = Query(default=None),
                      current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).executive_summary(current_user, organisation_id=organisation_id)


# V1.1: cross-PPD comparison (top/lowest performer, high-risk, budget & Teras by PPD).
@router.get("/ppd-comparison", response_model=PPDComparisonOut)
def ppd_comparison(parent_organisation_id: str | None = Query(default=None),
                   current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).ppd_comparison(current_user, parent_organisation_id=parent_organisation_id)
