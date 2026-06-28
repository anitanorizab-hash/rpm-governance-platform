"""Agent API (A6 G8) — CP13. JWT; manual execution admin/internal-only; logged. Advisory only."""
from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user, require_roles
from app.db.session import get_db
from app.services.agent_service import AgentNotFound, AgentService
from app.services.audit_service import AuditService

router = APIRouter(prefix="/agents", tags=["agents"])

AGENT_EXEC_ROLES = ("super_admin", "jpn_admin")


@router.get("")
def list_agents(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return AgentService(db).list()


@router.get("/{agent_name}")
def get_agent(agent_name: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return AgentService(db).get(agent_name)
    except AgentNotFound:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/{agent_name}/execute")
def execute_agent(agent_name: str, request: Request, payload: dict | None = Body(default=None),
                  _admin=Depends(require_roles(*AGENT_EXEC_ROLES)),
                  current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        res = AgentService(db).execute(agent_name, payload or {})
    except AgentNotFound:
        raise HTTPException(status_code=404, detail="Agent not found")
    AuditService(db).record(entity_type="agent", entity_id=agent_name, action="agent_execute",
                            actor_id=current_user.id, context=get_audit_context(request))
    return res


@router.post("/orchestrate")
def orchestrate(request: Request, body: dict = Body(...),
                _admin=Depends(require_roles(*AGENT_EXEC_ROLES)),
                current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    steps = body.get("steps", [])
    context = body.get("context", {})
    res = AgentService(db).orchestrate(steps, context)
    AuditService(db).record(entity_type="agent", entity_id="orchestrate", action="agent_orchestrate",
                            actor_id=current_user.id, context=get_audit_context(request))
    return res
