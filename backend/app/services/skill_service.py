"""Skill service (CP12): list/get/execute skills + SkillExecution logging.

Skills are advisory compute units; they never execute official actions. Manual execution is
admin/internal-only and logged.
"""
from __future__ import annotations

import json
import uuid

from sqlalchemy.orm import Session

from app.models.ai.ai_meta import SkillExecution
from app.skills import registry


class SkillNotFound(Exception):
    pass


class SkillService:
    def __init__(self, db: Session | None = None):
        self.db = db

    def list(self):
        return registry.list_skills()

    def get(self, name: str):
        skill = registry.get_skill(name)
        if not skill:
            raise SkillNotFound(name)
        return skill.metadata()

    def execute(self, name: str, payload: dict, *, actor_id: str | None = None, log: bool = True):
        skill = registry.get_skill(name)
        if not skill:
            raise SkillNotFound(name)
        result = skill.run(payload or {})
        if log and self.db is not None:
            self.db.add(SkillExecution(
                id=str(uuid.uuid4()), skill_name=name, version=skill.version,
                inputs_ref=json.dumps(payload or {}, default=str)[:2000],
                outputs_ref=json.dumps(result, default=str)[:2000],
            ))
            self.db.commit()
        return {"skill": name, "result": result}
