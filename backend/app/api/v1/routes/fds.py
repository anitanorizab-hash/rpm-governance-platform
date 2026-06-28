"""Financial Decision Support API (A6 G7) — CP11. Deterministic, advisory; JWT + role-scoped. No AI."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.fds import (
    FDSAnalysisOut, FDSSummaryOut, RecommendationOut, SubmitForApprovalOut,
)
from app.services.fds_service import FDSPermissionError, FDSService

router = APIRouter(prefix="/fds", tags=["fds"])


def _svc(db):
    return FDSService(db)


@router.get("/kpis/{kpi_id}/analysis", response_model=FDSAnalysisOut)
def analysis(kpi_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        res = _svc(db).analyze_kpi(current_user=current_user, kpi_id=kpi_id)
    except FDSPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    if res is None:
        raise HTTPException(status_code=404, detail="KPI not found")
    return res


@router.post("/kpis/{kpi_id}/generate", response_model=FDSAnalysisOut, status_code=201)
def generate(kpi_id: str, request: Request,
             current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        res = _svc(db).generate(current_user=current_user, kpi_id=kpi_id,
                                context=get_audit_context(request))
    except FDSPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    if res is None:
        raise HTTPException(status_code=404, detail="KPI not found")
    return res


@router.get("/recommendations", response_model=list[RecommendationOut])
def list_recommendations(kpi_id: str | None = None,
                         current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return [RecommendationOut.from_model(r) for r in _svc(db).list_recommendations(kpi_id=kpi_id)]


@router.get("/summary", response_model=FDSSummaryOut)
def summary(organisation_id: str | None = Query(default=None),
            current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).summary(current_user, organisation_id=organisation_id)


@router.get("/recommendations/{recommendation_id}", response_model=RecommendationOut)
def get_recommendation(recommendation_id: str,
                       current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    rec = _svc(db).get_recommendation(recommendation_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return RecommendationOut.from_model(rec)


@router.post("/recommendations/{recommendation_id}/submit-for-approval", response_model=SubmitForApprovalOut)
def submit_for_approval(recommendation_id: str, request: Request,
                        current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        res = _svc(db).submit_for_approval(current_user=current_user, rec_id=recommendation_id,
                                           context=get_audit_context(request))
    except FDSPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    if res is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return res
