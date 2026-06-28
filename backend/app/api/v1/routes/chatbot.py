"""KPI Chatbot API (A6 G11) — CP15. JWT; role-scoped; advisory; cited; logged. No official actions."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.chatbot import ConversationOut, MessageIn, MessageOut, SessionOut
from app.services.chatbot_service import ChatbotError, ChatbotPermissionError, ChatbotService

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


def _svc(db):
    return ChatbotService(db)


@router.post("/sessions", response_model=SessionOut, status_code=201)
def create_session(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return SessionOut.from_model(_svc(db).create_session(current_user))


@router.get("/sessions", response_model=list[SessionOut])
def list_sessions(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return [SessionOut.from_model(s) for s in _svc(db).list_sessions(current_user)]


@router.get("/sessions/{session_id}", response_model=SessionOut)
def get_session(session_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    s = _svc(db).get_session(current_user, session_id)
    if s is None:
        raise HTTPException(status_code=404, detail="Session not found")
    if s == "forbidden":
        raise HTTPException(status_code=403, detail="Not permitted to view this session")
    return SessionOut.from_model(s)


@router.post("/sessions/{session_id}/messages", response_model=MessageOut)
def send_message(session_id: str, body: MessageIn,
                 current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        res = _svc(db).send_message(current_user=current_user, session_id=session_id,
                                    message=body.message, achievement=body.achievement, target=body.target)
    except ChatbotError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ChatbotPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    if res is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return res


@router.get("/sessions/{session_id}/messages", response_model=list[ConversationOut])
def list_messages(session_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    res = _svc(db).list_conversations(current_user, session_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Session not found")
    if res == "forbidden":
        raise HTTPException(status_code=403, detail="Not permitted to view this session")
    return [ConversationOut.from_model(c) for c in res]
