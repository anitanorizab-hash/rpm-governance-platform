"""Executive Copilot Agent (CP13) — ORCHESTRATES specialist agents (does not replace them).

Consumes KPI Analysis, Risk, FDS and Knowledge Alignment agent outputs + dashboard_summary skill
to synthesise an advisory executive insight. Human review required before acting (ASM-11).
"""
from __future__ import annotations

from app.agents.base import Agent


class ExecutiveCopilotAgent(Agent):
    name = "executive_copilot"
    description = "Synthesise specialist-agent outputs into advisory executive insight (orchestrator)."
    uses_skills = ["dashboard_summary"]
    human_review_required = True

    def run(self, context: dict) -> dict:
        # Lazy import to avoid circular import (registry includes this agent).
        from app.agents import registry as agent_registry

        def _run(name):
            agent = agent_registry.get_agent(name)
            return agent.run(context) if agent else {"error": f"agent '{name}' missing"}

        sub = {
            "kpi_analysis": _run("kpi_analysis"),
            "risk_assessment": _run("risk_assessment"),
            "financial_decision_support": _run("financial_decision_support"),
            "knowledge_alignment": _run("knowledge_alignment"),
        }
        summary = self.skill("dashboard_summary", {"overview": context.get("overview", {})})
        insight = (
            "Executive insight (advisory): "
            + summary.get("text", "")
            + " Specialist findings attached; human decision required."
        )
        return self._wrap({
            "insight": insight,
            "summary": summary,
            "specialist_outputs": sub,   # orchestrates specialists, not replaces them
        })
