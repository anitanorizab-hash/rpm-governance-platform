"""Custom Agent Orchestrator (CP13) — V1, no external orchestration framework (TRD §17.5).

Registers agents, runs one or a sequence, passes structured context between steps, returns combined
output, and stops safely if an agent fails (safe fallback — no external side effects).
"""
from __future__ import annotations

from app.agents import registry


class AgentOrchestrator:
    def __init__(self):
        self.registry = registry

    def run_agent(self, name: str, context: dict) -> dict:
        agent = self.registry.get_agent(name)
        if not agent:
            return {"agent": name, "status": "error", "error": "agent not found",
                    "fallback": True, "advisory_only": True, "human_review_required": True}
        try:
            out = agent.run(context or {})
            return {"agent": name, "status": "ok", "output": out}
        except Exception as exc:  # safe fallback — never crash the request
            return {"agent": name, "status": "error", "error": str(exc),
                    "fallback": True, "advisory_only": True, "human_review_required": True,
                    "message": f"Agent '{name}' failed safely; human review required."}

    def run_sequence(self, steps: list, context: dict | None = None) -> dict:
        """steps: list of agent names or {agent, context}. Stops safely on first failure."""
        ctx = dict(context or {})
        results = []
        stopped = False
        for step in steps:
            name = step if isinstance(step, str) else step.get("agent")
            step_ctx = {**ctx, **(step.get("context", {}) if isinstance(step, dict) else {})}
            res = self.run_agent(name, step_ctx)
            results.append(res)
            if res["status"] == "error":
                stopped = True
                break
            # pass structured output forward
            ctx["previous"] = res.get("output")
        return {"status": "stopped" if stopped else "completed",
                "steps": results, "advisory_only": True}
