"""Import API (A6 G4) — CP6. JWT + admin-only (super_admin/jpn_admin). Excel = initial input only."""
from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import require_roles
from app.db.session import get_db
from app.schemas.import_schema import ImportBatchOut, ImportExecuteOut, ImportPreviewOut
from app.services.import_service import ImportService

router = APIRouter(prefix="/imports", tags=["imports"])

IMPORT_ROLES = ("super_admin", "jpn_admin")


@router.post("/preview", response_model=ImportPreviewOut)
async def preview(
    file: UploadFile = File(...),
    plan_type: str = Form("jpn"),
    _admin=Depends(require_roles(*IMPORT_ROLES)),
    db: Session = Depends(get_db),
):
    data = await file.read()
    return ImportService(db).preview(file_bytes=data, plan_type=plan_type)


@router.post("/execute", response_model=ImportExecuteOut)
async def execute(
    request: Request,
    file: UploadFile = File(...),
    plan_type: str = Form("jpn"),
    override: bool = Form(False),
    admin=Depends(require_roles(*IMPORT_ROLES)),
    db: Session = Depends(get_db),
):
    data = await file.read()
    ctx = get_audit_context(request)
    return ImportService(db).execute(
        file_bytes=data, filename=file.filename or "upload.xlsx", plan_type=plan_type,
        actor_id=admin.id, override=override, context=ctx,
    )


@router.get("/history", response_model=list[ImportBatchOut])
def history(
    _admin=Depends(require_roles(*IMPORT_ROLES)),
    db: Session = Depends(get_db),
):
    from app.repositories.import_repository import ImportRepository
    return [ImportBatchOut.from_model(b) for b in ImportRepository(db).list_batches()]


@router.get("/{batch_id}", response_model=ImportBatchOut)
def get_batch(
    batch_id: str,
    _admin=Depends(require_roles(*IMPORT_ROLES)),
    db: Session = Depends(get_db),
):
    from fastapi import HTTPException, status
    from app.repositories.import_repository import ImportRepository
    batch = ImportRepository(db).get_batch(batch_id)
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Import batch not found")
    return ImportBatchOut.from_model(batch)
