"""Validation Agent (CP13) — composes the validation skill."""
from __future__ import annotations

from app.agents.base import Agent


class ValidationAgent(Agent):
    name = "validation"
    description = "Detect missing mandatory KPI fields."
    uses_skills = ["validation"]

    def run(self, context: dict) -> dict:
        out = self.skill("validation", {"fields": context.get("fields", context)})
        return self._wrap({"validation": out})
