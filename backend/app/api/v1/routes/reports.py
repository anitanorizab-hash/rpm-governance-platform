"""Report API (A6 G13) — CP17. JWT; manage roles generate; HITL via CP9; no email/auto-issue."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.report import ReportGenerateIn, ReportOut, ReportPatchIn, SubmitForReviewOut
from app.services.report_service import ReportPermissionError, ReportService, ReportStateError

router = APIRouter(prefix="/reports", tags=["reports"])


def _svc(db):
    return ReportService(db)


def _guard(call):
    try:
        return call()
    except ReportPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ReportStateError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/generate", response_model=ReportOut, status_code=201)
def generate(body: ReportGenerateIn, request: Request,
             current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _guard(lambda: _svc(db).generate(current_user=current_user, period=body.period,
                                            type_=body.type, context=get_audit_context(request)))


@router.get("", response_model=list[ReportOut])
def list_reports(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _svc(db).list_reports(current_user)


@router.get("/{report_id}", response_model=ReportOut)
def get_report(report_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    r = _svc(db).get_report(current_user, report_id)
    if r is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return r


@router.patch("/{report_id}", response_model=ReportOut)
def patch_report(report_id: str, body: ReportPatchIn, request: Request,
                 current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    r = _guard(lambda: _svc(db).patch(current_user=current_user, report_id=report_id,
                                      fields=body.model_dump(exclude_none=True),
                                      context=get_audit_context(request)))
    if r is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return r


@router.post("/{report_id}/submit-for-review", response_model=SubmitForReviewOut)
def submit_for_review(report_id: str, request: Request,
                      current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = _guard(lambda: _svc(db).submit_for_review(current_user=current_user, report_id=report_id,
                                                    context=get_audit_context(request)))
    if res is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return res


@router.post("/{report_id}/archive", response_model=ReportOut)
def archive(report_id: str, request: Request,
            current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = _guard(lambda: _svc(db).archive(current_user=current_user, report_id=report_id,
                                          context=get_audit_context(request)))
    if res is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return res
