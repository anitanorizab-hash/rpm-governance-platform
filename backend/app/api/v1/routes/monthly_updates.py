"""Monthly Update API (A6 G5) — CP8. In-system only; JWT + permission-scoped; audited."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.monthly_update import (
    MonthlyUpdateIn, MonthlyUpdateOut, MonthlyUpdatePatch, MonthlyUpdateSummaryOut,
)
from app.services.monthly_update_service import (
    DuplicateUpdate, MonthlyUpdateService, PermissionError_, ValidationError_,
)

router = APIRouter(prefix="/monthly-updates", tags=["monthly-updates"])
# KPI-scoped listing lives under /kpis to match the API spec.
kpi_scoped_router = APIRouter(prefix="/kpis", tags=["monthly-updates"])


def _svc(db):
    return MonthlyUpdateService(db)


@router.post("", response_model=MonthlyUpdateOut, status_code=201)
def create_update(body: MonthlyUpdateIn, request: Request,
                  override: bool = Query(default=False),
                  current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        res = _svc(db).create(current_user=current_user, data=body.model_dump(),
                              override=override, context=get_audit_context(request))
    except ValidationError_ as e:
        raise HTTPException(status_code=422, detail=str(e))
    except PermissionError_ as e:
        raise HTTPException(status_code=403, detail=str(e))
    except DuplicateUpdate as e:
        raise HTTPException(status_code=409, detail=str(e))
    if res is None:
        raise HTTPException(status_code=404, detail="KPI not found")
    return MonthlyUpdateOut.from_model(res["update"])


@router.get("", response_model=list[MonthlyUpdateOut])
def list_updates(kpi_id: str | None = Query(default=None),
                 year: int | None = Query(default=None),
                 month: int | None = Query(default=None),
                 current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return [MonthlyUpdateOut.from_model(u) for u in
            _svc(db).list_updates(kpi_id=kpi_id, year=year, month=month)]


@router.get("/summary", response_model=MonthlyUpdateSummaryOut)
def summary(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).summary()


@router.get("/{update_id}", response_model=MonthlyUpdateOut)
def get_update(update_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    upd = _svc(db).get(update_id)
    if not upd:
        raise HTTPException(status_code=404, detail="Monthly update not found")
    return MonthlyUpdateOut.from_model(upd)


@router.patch("/{update_id}", response_model=MonthlyUpdateOut)
def patch_update(update_id: str, body: MonthlyUpdatePatch, request: Request,
                 current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        res = _svc(db).patch(current_user=current_user, update_id=update_id,
                             patch=body.model_dump(exclude_none=True), context=get_audit_context(request))
    except ValidationError_ as e:
        raise HTTPException(status_code=422, detail=str(e))
    except PermissionError_ as e:
        raise HTTPException(status_code=403, detail=str(e))
    if res is None:
        raise HTTPException(status_code=404, detail="Monthly update not found")
    return MonthlyUpdateOut.from_model(res["update"])


@kpi_scoped_router.get("/{kpi_id}/monthly-updates", response_model=list[MonthlyUpdateOut])
def list_for_kpi(kpi_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return [MonthlyUpdateOut.from_model(u) for u in _svc(db).list_updates(kpi_id=kpi_id)]
