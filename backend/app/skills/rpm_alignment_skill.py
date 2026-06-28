"""S8 RPM Alignment Skill (CP12) — deterministic placeholder until RAG (CP14)."""
from __future__ import annotations

import re

from app.skills.base import Skill


class RPMAlignmentSkill(Skill):
    name = "rpm_alignment"
    description = "KPI↔RPM alignment (deterministic placeholder; RAG-enhanced in CP14)."
    deterministic = True

    def run(self, payload: dict) -> dict:
        statement = (payload.get("kpi_statement") or "").lower()
        # Placeholder heuristic: alignment strength from keyword overlap with RPM themes.
        rpm_terms = ("murid", "guru", "pendidikan", "sekolah", "literasi", "numerasi", "kpi", "teras")
        hits = sum(1 for t in rpm_terms if re.search(rf"\b{t}", statement))
        strength = round(min(1.0, hits / 3.0), 2) if statement else 0.0
        return {
            "mapped": bool(statement),
            "alignment_strength": strength,
            "rpm_reference": "RPM 2026-2035",
            "note": "Deterministic placeholder; semantic alignment via RAG in CP14.",
            "source": "placeholder",
        }
