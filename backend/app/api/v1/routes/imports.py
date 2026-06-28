"""Import API (A6 G4) — CP6. JWT + admin-only (super_admin/jpn_admin). Excel = initial input only."""
from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import require_roles
from app.db.session import get_db
from app.schemas.import_schema import ImportBatchOut, ImportExecuteOut, ImportPreviewOut
from app.services.import_service import ImportService

router = APIRouter(prefix="/imports", tags=["imports"])

IMPORT_ROLES = ("super_admin", "jpn_admin")
# Repo-root Data folder (…/backend/app/api/v1/routes/imports.py → parents[5] == repo root).
DATA_DIR = str(Path(__file__).resolve().parents[5] / "Data")


@router.post("/preview", response_model=ImportPreviewOut)
async def preview(
    file: UploadFile = File(...),
    plan_type: str = Form("jpn"),
    _admin=Depends(require_roles(*IMPORT_ROLES)),
    db: Session = Depends(get_db),
):
    data = await file.read()
    return ImportService(db).preview(file_bytes=data, plan_type=plan_type, filename=file.filename or "")


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


@router.post("/data-folder")
def import_data_folder(
    request: Request,
    override: bool = Form(False),
    admin=Depends(require_roles(*IMPORT_ROLES)),
    db: Session = Depends(get_db),
):
    """V1.1.1: batch-import the JPN plan + all PPD plans from the server's Data folder."""
    return ImportService(db).import_data_folder(
        data_dir=DATA_DIR, actor_id=admin.id, override=override, context=get_audit_context(request),
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
