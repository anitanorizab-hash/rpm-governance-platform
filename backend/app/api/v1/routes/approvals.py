"""Approval API (A6 G15) — CP9. Human-in-the-loop state machine. JWT-protected; audited."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.approval import ApprovalCreateIn, ApprovalDecisionIn, ApprovalOut
from app.services.approval_service import (
    ApprovalError, ApprovalPermissionError, ApprovalService,
)

router = APIRouter(prefix="/approvals", tags=["approvals"])


def _svc(db):
    return ApprovalService(db)


def _handle(fn):
    try:
        res = fn()
    except ApprovalPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ApprovalError as e:
        raise HTTPException(status_code=409, detail=str(e))
    if res is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    return ApprovalOut.from_model(res)


@router.post("", response_model=ApprovalOut, status_code=201)
def create_request(body: ApprovalCreateIn, request: Request,
                   current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    ap = _svc(db).create_request(item_type=body.item_type, item_id=body.item_id,
                                 requested_by=current_user.id, submit=body.submit,
                                 context=get_audit_context(request))
    return ApprovalOut.from_model(ap)


@router.get("", response_model=list[ApprovalOut])
def list_approvals(state: str | None = Query(default=None),
                   item_type: str | None = Query(default=None),
                   current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return [ApprovalOut.from_model(a) for a in _svc(db).list(state=state, item_type=item_type)]


@router.get("/pending", response_model=list[ApprovalOut])
def pending(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return [ApprovalOut.from_model(a) for a in _svc(db).list(state="pending_review")]


@router.get("/{approval_id}", response_model=ApprovalOut)
def get_approval(approval_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    ap = _svc(db).get(approval_id)
    if not ap:
        raise HTTPException(status_code=404, detail="Approval not found")
    return ApprovalOut.from_model(ap)


@router.post("/{approval_id}/submit", response_model=ApprovalOut)
def submit(approval_id: str, request: Request,
           current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = _svc(db)
    return _handle(lambda: svc.submit(approval_id=approval_id, actor=current_user,
                                      context=get_audit_context(request)))


@router.post("/{approval_id}/approve", response_model=ApprovalOut)
def approve(approval_id: str, request: Request, body: ApprovalDecisionIn | None = None,
            override: bool = Query(default=False),
            current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = _svc(db)
    comment = body.comment if body else None
    return _handle(lambda: svc.approve(approval_id=approval_id, actor=current_user,
                                       override=override, comment=comment,
                                       context=get_audit_context(request)))


@router.post("/{approval_id}/reject", response_model=ApprovalOut)
def reject(approval_id: str, request: Request, body: ApprovalDecisionIn | None = None,
           current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = _svc(db)
    comment = body.comment if body else None
    return _handle(lambda: svc.reject(approval_id=approval_id, actor=current_user,
                                      comment=comment, context=get_audit_context(request)))


@router.post("/{approval_id}/cancel", response_model=ApprovalOut)
def cancel(approval_id: str, request: Request,
           current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    svc = _svc(db)
    return _handle(lambda: svc.cancel(approval_id=approval_id, actor=current_user,
                                      context=get_audit_context(request)))
