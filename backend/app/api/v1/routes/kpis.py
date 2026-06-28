"""KPI API (A6 G3) — CP7. JWT + RBAC. Amendment window enforced. Soft delete only."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.operational.finance import FinancialAllocation
from app.schemas.kpi import (
    CompletenessOut, CompletenessSummaryOut, KPICreateIn, KPIDetail, KPIListItem,
    KPIPatchIn, PICAssignIn,
)
from app.services import completeness_service
from app.services.kpi_service import AmendmentBlocked, KPIService

router = APIRouter(prefix="/kpis", tags=["kpis"])


def _list_item(kpi) -> KPIListItem:
    return KPIListItem(
        id=kpi.id, code=kpi.code, statement=kpi.statement,
        teras_number=(kpi.teras.number if kpi.teras else None),
        sector=kpi.sector, status=kpi.status,
        pic_email=(kpi.pic.email if kpi.pic else None),
        is_complete=completeness_service.is_complete(kpi),
    )


def _detail(kpi, db: Session) -> KPIDetail:
    total = db.scalar(
        select(func.coalesce(func.sum(FinancialAllocation.amount), 0.0))
        .where(FinancialAllocation.kpi_id == kpi.id)
    )
    missing = completeness_service.kpi_missing_fields(kpi)
    return KPIDetail(
        id=kpi.id, code=kpi.code, statement=kpi.statement,
        teras_number=(kpi.teras.number if kpi.teras else None),
        sector=kpi.sector, status=kpi.status,
        indicators=[i.indicator_text for i in kpi.indicators if i.indicator_text],
        targets=[t.target_value for t in kpi.targets if t.target_value],
        activities=[a.description for a in kpi.activities if a.description],
        pic_name=(kpi.pic.name if kpi.pic else None),
        pic_email=(kpi.pic.email if kpi.pic else None),
        financial_allocation_total=float(total or 0.0),
        is_complete=not missing, missing_fields=missing,
    )


# --- static paths first (before /{kpi_id}) ---
@router.get("", response_model=list[KPIListItem])
def list_kpis(
    teras: int | None = Query(default=None),
    sector: str | None = Query(default=None),
    pic: str | None = Query(default=None),
    status_: str | None = Query(default=None, alias="status"),
    completeness: str | None = Query(default=None, pattern="^(complete|incomplete)$"),
    limit: int = Query(default=100, le=500),
    offset: int = Query(default=0, ge=0),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items = KPIService(db).list_kpis(
        current_user=current_user, teras=teras, sector=sector, pic=pic, status=status_,
        completeness=completeness, limit=limit, offset=offset,
    )
    return [_list_item(k) for k in items]


@router.post("", response_model=KPIDetail, status_code=201)
def create_kpi(body: KPICreateIn, request: Request,
               current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = KPIService(db).create_kpi(current_user=current_user, data=body.model_dump(),
                                    context=get_audit_context(request))
    if res == "forbidden":
        raise HTTPException(status_code=403, detail="Not permitted to create KPIs")
    return _detail(res, db)


@router.get("/completeness/summary", response_model=CompletenessSummaryOut)
def completeness_summary(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return KPIService(db).completeness_summary()


# --- dynamic paths ---
@router.get("/{kpi_id}", response_model=KPIDetail)
def get_kpi(kpi_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    kpi = KPIService(db).get_kpi(kpi_id)
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    return _detail(kpi, db)


@router.get("/{kpi_id}/completeness", response_model=CompletenessOut)
def kpi_completeness(kpi_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = KPIService(db)
    kpi = svc.get_kpi(kpi_id)
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    return svc.completeness(kpi)


@router.patch("/{kpi_id}", response_model=KPIDetail)
def patch_kpi(kpi_id: str, body: KPIPatchIn, request: Request,
              override: bool = Query(default=False),
              current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = KPIService(db)
    try:
        res = svc.update_kpi(current_user=current_user, kpi_id=kpi_id,
                             patch=body.model_dump(exclude_none=True), override=override,
                             context=get_audit_context(request))
    except AmendmentBlocked as e:
        raise HTTPException(status_code=409, detail=str(e))
    if res is None:
        raise HTTPException(status_code=404, detail="KPI not found")
    if res == "forbidden":
        raise HTTPException(status_code=403, detail="Not permitted to manage this KPI")
    return _detail(res, db)


@router.post("/{kpi_id}/assign-pic", response_model=KPIDetail)
def assign_pic(kpi_id: str, body: PICAssignIn, request: Request,
               current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = KPIService(db).assign_pic(current_user=current_user, kpi_id=kpi_id, name=body.name,
                                    email=body.email, sector=body.sector,
                                    context=get_audit_context(request))
    if res is None:
        raise HTTPException(status_code=404, detail="KPI not found")
    if res == "forbidden":
        raise HTTPException(status_code=403, detail="Not permitted to manage this KPI")
    return _detail(res, db)


@router.delete("/{kpi_id}")
def delete_kpi(kpi_id: str, request: Request,
               current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = KPIService(db).soft_delete(current_user=current_user, kpi_id=kpi_id,
                                     context=get_audit_context(request))
    if res is None:
        raise HTTPException(status_code=404, detail="KPI not found")
    if res == "forbidden":
        raise HTTPException(status_code=403, detail="Not permitted to delete KPIs")
    return {"status": "soft_deleted", "kpi_id": kpi_id}
