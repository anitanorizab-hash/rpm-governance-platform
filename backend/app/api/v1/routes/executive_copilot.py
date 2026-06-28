"""Executive Copilot API (A6 G12) — CP16. JWT; admin/executive only; advisory; HITL; logged."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.executive_copilot import (
    AskIn, HistoryItem, RecommendationIn, RecommendationOut, SubmitForApprovalOut,
)
from app.services.executive_copilot_service import CopilotPermissionError, ExecutiveCopilotService

router = APIRouter(prefix="/executive-copilot", tags=["executive-copilot"])


def _svc(db):
    return ExecutiveCopilotService(db)


def _guard(call):
    try:
        return call()
    except CopilotPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/briefing")
def briefing(request: Request, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _guard(lambda: _svc(db).briefing(current_user=current_user, context=get_audit_context(request)))


@router.post("/ask")
def ask(body: AskIn, request: Request, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return _guard(lambda: _svc(db).ask(current_user=current_user, question=body.question,
                                       context=get_audit_context(request)))


@router.post("/recommendations", response_model=RecommendationOut, status_code=201)
def create_recommendation(body: RecommendationIn, request: Request,
                          current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    rec = _guard(lambda: _svc(db).create_recommendation(current_user=current_user, data=body.model_dump(),
                                                        context=get_audit_context(request)))
    return RecommendationOut.from_model(rec)


@router.post("/recommendations/{recommendation_id}/submit-for-approval", response_model=SubmitForApprovalOut)
def submit_for_approval(recommendation_id: str, request: Request,
                        current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = _guard(lambda: _svc(db).submit_for_approval(current_user=current_user, rec_id=recommendation_id,
                                                      context=get_audit_context(request)))
    if res is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return res


@router.get("/history", response_model=list[HistoryItem])
def history(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    items = _guard(lambda: _svc(db).history(current_user))
    return [HistoryItem.from_model(i) for i in items]
