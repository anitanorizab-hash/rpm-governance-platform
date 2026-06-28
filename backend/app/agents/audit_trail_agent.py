"""Audit Trail Agent (CP13) — composes audit_logging skill (structured entry; logging only)."""
from __future__ import annotations

from app.agents.base import Agent


class AuditTrailAgent(Agent):
    name = "audit_trail"
    description = "Produce a masked, structured audit entry (append-only logging)."
    uses_skills = ["audit_logging"]

    def run(self, context: dict) -> dict:
        out = self.skill("audit_logging", context)
        return self._wrap({"audit_entry": out})
