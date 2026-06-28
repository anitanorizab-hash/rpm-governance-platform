"""Agent service (CP13): list/get/execute/orchestrate + AgentExecution logging."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.agents import registry
from app.agents.orchestrator import AgentOrchestrator
from app.models.ai.ai_meta import AgentExecution


class AgentNotFound(Exception):
    pass


class AgentService:
    def __init__(self, db: Session | None = None):
        self.db = db
        self.orchestrator = AgentOrchestrator()

    def list(self):
        return registry.list_agents()

    def get(self, name: str):
        agent = registry.get_agent(name)
        if not agent:
            raise AgentNotFound(name)
        return agent.metadata()

    def _log(self, *, agent_name, trigger, inputs, output, status, started):
        if self.db is None:
            return
        self.db.add(AgentExecution(
            id=str(uuid.uuid4()), agent_name=agent_name, trigger=trigger,
            inputs_ref=json.dumps(inputs, default=str)[:2000],
            outputs_ref=json.dumps(output, default=str)[:2000],
            status=status, started_at=started, ended_at=datetime.now(timezone.utc),
        ))
        self.db.commit()

    def _run_ctx(self, context: dict | None) -> dict:
        """Inject the db session so RAG-using agents can call rag_service (via the RAG skill)."""
        ctx = dict(context or {})
        if self.db is not None:
            ctx["_db"] = self.db
        return ctx

    def execute(self, name: str, context: dict, *, trigger="manual"):
        if not registry.get_agent(name):
            raise AgentNotFound(name)
        started = datetime.now(timezone.utc)
        res = self.orchestrator.run_agent(name, self._run_ctx(context))
        self._log(agent_name=name, trigger=trigger, inputs=context or {},  # log original (no _db)
                  output=res, status=res.get("status", "ok"), started=started)
        return res

    def orchestrate(self, steps: list, context: dict | None = None, *, trigger="orchestrate"):
        started = datetime.now(timezone.utc)
        res = self.orchestrator.run_sequence(steps, self._run_ctx(context))
        # log each step + an orchestration summary
        for step in res["steps"]:
            self._log(agent_name=step.get("agent"), trigger=trigger, inputs=context or {},
                      output=step, status=step.get("status", "ok"), started=started)
        return res
