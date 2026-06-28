"""Audit API (A6 G16) — CP5. Read-only; JWT-protected; role-scoped. No update/delete endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.audit import AuditLogOut
from app.services.audit_service import AuditService

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs", response_model=list[AuditLogOut])
def list_logs(
    entity_type: str | None = Query(default=None),
    action: str | None = Query(default=None),
    limit: int = Query(default=100, le=500),
    offset: int = Query(default=0, ge=0),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Admin/oversight see all logs; other authenticated users see only their own actions."""
    logs = AuditService(db).list_logs(
        current_user=current_user, entity_type=entity_type, action=action,
        limit=limit, offset=offset,
    )
    return [AuditLogOut.from_model(x) for x in logs]


@router.get("/logs/{audit_id}", response_model=AuditLogOut)
def get_log(
    audit_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = AuditService(db).get_log(current_user=current_user, audit_id=audit_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit log not found")
    if result == "forbidden":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not permitted to view this log")
    return AuditLogOut.from_model(result)
