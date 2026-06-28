"""Automation API (V1.1.1) — administrator-triggered, HITL-safe draft generation.

Generates report/notification DRAFTS only; nothing is approved, queued or sent here.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.services.automation_service import AutomationPermissionError, AutomationService

router = APIRouter(prefix="/automation", tags=["automation"])


class AutomationRunIn(BaseModel):
    types: list[str] | None = None       # subset of monthly_report/pic_reminders/missing_info/overdue_escalations
    period: str | None = None            # YYYY-MM for the monthly report
    limit: int = 10                      # cap drafts per notification type


@router.post("/run")
def run(body: AutomationRunIn, request: Request,
        current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return AutomationService(db).run(
            current_user=current_user, types=body.types, period=body.period,
            limit=body.limit, context=get_audit_context(request))
    except AutomationPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
