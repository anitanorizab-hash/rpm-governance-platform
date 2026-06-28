"""S13 Audit Logging Skill (CP12) — structured audit entry (logging, not an official action)."""
from __future__ import annotations

from app.skills.base import Skill
from app.core.audit import mask_payload


class AuditLoggingSkill(Skill):
    name = "audit_logging"
    description = "Produce a masked, structured audit entry (append-only logging)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        return {
            "entity_type": payload.get("entity_type"),
            "action": payload.get("action"),
            "entity_id": payload.get("entity_id"),
            "actor_id": payload.get("actor_id"),
            "before": mask_payload(payload.get("before")),
            "after": mask_payload(payload.get("after")),
            "reason": payload.get("reason"),
        }
