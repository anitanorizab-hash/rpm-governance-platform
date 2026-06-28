"""Agent base (CP13). Agents compose CP12 skills and return structured ADVISORY output.

Agents NEVER approve/reject/send/delete/amend official outputs and NEVER access the DB directly —
they operate on the context passed in (services fetch data) and call skills via the registry.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from app.skills import registry as skill_registry


class Agent(ABC):
    name: str = "base"
    description: str = ""
    uses_skills: list[str] = []
    human_review_required: bool = False
    version: str = "1.0"

    # convenience: run a registered skill (no DB access)
    @staticmethod
    def skill(name: str, payload: dict) -> dict:
        s = skill_registry.get_skill(name)
        if not s:
            return {"error": f"skill '{name}' not found"}
        return s.run(payload or {})

    @abstractmethod
    def run(self, context: dict) -> dict:
        """Return structured advisory output (must include advisory_only=True)."""

    def metadata(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "uses_skills": self.uses_skills,
            "human_review_required": self.human_review_required,
            "version": self.version,
        }

    def _wrap(self, payload: dict) -> dict:
        """Standard advisory envelope."""
        return {
            "agent": self.name,
            "advisory_only": True,
            "human_review_required": self.human_review_required,
            **payload,
        }
