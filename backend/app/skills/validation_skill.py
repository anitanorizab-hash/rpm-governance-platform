"""S2 Validation Skill (CP12) — deterministic completeness check on a field dict."""
from __future__ import annotations

from app.skills.base import Skill

MANDATORY = ("statement", "indicator", "target", "pic_name", "pic_email", "department", "teras")


class ValidationSkill(Skill):
    name = "validation"
    description = "Detect missing mandatory KPI fields (deterministic)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        fields = payload.get("fields", payload)
        missing = [f for f in MANDATORY if not fields.get(f)]
        return {"is_complete": not missing, "missing_fields": missing}
