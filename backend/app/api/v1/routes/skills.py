"""Skills API (A6 G9) — CP12. JWT; manual execution admin/internal-only; logged. No official actions."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.audit import get_audit_context
from app.core.dependencies import get_current_user, require_roles
from app.db.session import get_db
from app.services.audit_service import AuditService
from app.services.skill_service import SkillNotFound, SkillService

router = APIRouter(prefix="/skills", tags=["skills"])

SKILL_EXEC_ROLES = ("super_admin", "jpn_admin")


@router.get("")
def list_skills(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return SkillService(db).list()


@router.get("/{skill_name}")
def get_skill(skill_name: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return SkillService(db).get(skill_name)
    except SkillNotFound:
        raise HTTPException(status_code=404, detail="Skill not found")


@router.post("/{skill_name}/execute")
def execute_skill(skill_name: str, request: Request, payload: dict | None = None,
                  _admin=Depends(require_roles(*SKILL_EXEC_ROLES)),
                  current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        res = SkillService(db).execute(skill_name, payload or {}, actor_id=current_user.id)
    except SkillNotFound:
        raise HTTPException(status_code=404, detail="Skill not found")
    AuditService(db).record(entity_type="skill", entity_id=skill_name, action="skill_execute",
                            actor_id=current_user.id, context=get_audit_context(request))
    return res
