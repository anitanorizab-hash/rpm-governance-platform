"""PIC Directory API (V1.1.1) — admin-managed PIC records, KPI assignment, Excel bulk import/export."""
from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, Response, UploadFile
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.pic import PICAssignKpisIn, PICCreateIn, PICImportOut, PICOut, PICPatchIn
from app.services.pic_service import PICPermissionError, PICService

router = APIRouter(prefix="/pics", tags=["pics"])

XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _guard(call):
    try:
        return call()
    except PICPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


def _out(svc, p, *, with_codes=False):
    codes = [k.code for k in svc.repo.assigned_kpis(p.id)] if with_codes else []
    return PICOut.from_model(p, assigned_count=svc.repo.assigned_count(p.id), assigned_codes=codes)


@router.get("", response_model=list[PICOut])
def list_pics(search: str | None = Query(default=None), organisation_id: str | None = Query(default=None),
              status: str | None = Query(default=None), department: str | None = Query(default=None),
              current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = PICService(db)
    pics = _guard(lambda: svc.list(current_user, search=search, organisation_id=organisation_id,
                                   status=status, department=department))
    return [_out(svc, p) for p in pics]


# --- static paths before /{pic_id} ---
@router.get("/export")
def export_pics(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    data = _guard(lambda: PICService(db).export_excel(current_user))
    return Response(content=data, media_type=XLSX,
                    headers={"Content-Disposition": "attachment; filename=pic_directory.xlsx"})


@router.post("/import", response_model=PICImportOut)
async def import_pics(request: Request, file: UploadFile = File(...),
                      current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    raw = await file.read()
    return _guard(lambda: PICService(db).import_excel(current_user=current_user, file_bytes=raw,
                                                      context=get_audit_context(request)))


@router.post("", response_model=PICOut, status_code=201)
def create_pic(body: PICCreateIn, request: Request,
               current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = PICService(db)
    p = _guard(lambda: svc.create(current_user=current_user, data=body.model_dump(),
                                  context=get_audit_context(request)))
    return _out(svc, p, with_codes=True)


@router.get("/{pic_id}", response_model=PICOut)
def get_pic(pic_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = PICService(db)
    p = _guard(lambda: svc.get(current_user, pic_id))
    if not p:
        raise HTTPException(status_code=404, detail="PIC not found")
    return _out(svc, p, with_codes=True)


@router.patch("/{pic_id}", response_model=PICOut)
def update_pic(pic_id: str, body: PICPatchIn, request: Request,
               current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = PICService(db)
    p = _guard(lambda: svc.update(current_user=current_user, pic_id=pic_id,
                                  fields=body.model_dump(exclude_none=True), context=get_audit_context(request)))
    if p is None:
        raise HTTPException(status_code=404, detail="PIC not found")
    return _out(svc, p, with_codes=True)


@router.delete("/{pic_id}")
def delete_pic(pic_id: str, request: Request,
               current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = _guard(lambda: PICService(db).delete(current_user=current_user, pic_id=pic_id,
                                               context=get_audit_context(request)))
    if res is None:
        raise HTTPException(status_code=404, detail="PIC not found")
    return {"status": "soft_deleted", "pic_id": pic_id}


@router.post("/{pic_id}/assign-kpis")
def assign_kpis(pic_id: str, body: PICAssignKpisIn, request: Request,
                current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = _guard(lambda: PICService(db).assign_kpis(current_user=current_user, pic_id=pic_id,
                                                    kpi_ids=body.kpi_ids, context=get_audit_context(request)))
    if res is None:
        raise HTTPException(status_code=404, detail="PIC not found")
    return res
