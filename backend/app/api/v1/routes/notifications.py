"""Notification API (A6 G14) — CP18. JWT; HITL via CP9; dry-run email; nothing sends without approval."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.notification import NotificationDraftIn, NotificationOut, NotificationPatchIn
from app.services.notification_service import (
    NotificationPermissionError, NotificationService, NotificationStateError,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


def _svc(db):
    return NotificationService(db)


def _guard(call):
    try:
        return call()
    except NotificationPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except NotificationStateError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/draft", response_model=NotificationOut, status_code=201)
def draft(body: NotificationDraftIn, request: Request,
          current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    n = _guard(lambda: _svc(db).draft(current_user=current_user, data=body.model_dump(),
                                      context=get_audit_context(request)))
    return NotificationOut.from_model(n)


@router.get("", response_model=list[NotificationOut])
def list_notifications(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return [NotificationOut.from_model(n) for n in _svc(db).list_notifications(current_user)]


# static path before /{notification_id}
@router.get("/email-queue")
def email_queue(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    items = _guard(lambda: _svc(db).email_queue(current_user))
    return [NotificationOut.from_model(n) for n in items]


@router.post("/email-queue/{queue_id}/retry")
def retry(queue_id: str, request: Request,
          current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = _guard(lambda: _svc(db).retry(current_user=current_user, notification_id=queue_id,
                                        context=get_audit_context(request)))
    if res is None:
        raise HTTPException(status_code=404, detail="Queue item not found")
    return res


@router.get("/{notification_id}", response_model=NotificationOut)
def get_notification(notification_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    n = _svc(db).get(current_user, notification_id)
    if not n:
        raise HTTPException(status_code=404, detail="Notification not found")
    return NotificationOut.from_model(n)


@router.patch("/{notification_id}", response_model=NotificationOut)
def patch_notification(notification_id: str, body: NotificationPatchIn, request: Request,
                       current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    n = _guard(lambda: _svc(db).patch(current_user=current_user, notification_id=notification_id,
                                      fields=body.model_dump(exclude_none=True),
                                      context=get_audit_context(request)))
    if n is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return NotificationOut.from_model(n)


@router.post("/{notification_id}/submit-for-review")
def submit_for_review(notification_id: str, request: Request,
                      current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = _guard(lambda: _svc(db).submit_for_review(current_user=current_user, notification_id=notification_id,
                                                    context=get_audit_context(request)))
    if res is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return res


@router.post("/{notification_id}/queue")
def queue(notification_id: str, request: Request,
          current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = _guard(lambda: _svc(db).queue(current_user=current_user, notification_id=notification_id,
                                        context=get_audit_context(request)))
    if res is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return res


@router.post("/{notification_id}/cancel")
def cancel(notification_id: str, request: Request,
           current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = _guard(lambda: _svc(db).cancel(current_user=current_user, notification_id=notification_id,
                                         context=get_audit_context(request)))
    if res is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return res
