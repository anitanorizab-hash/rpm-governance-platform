"""Executive Copilot service (CP16): advisory leadership decision support.

Orchestrates Dashboard + specialist agents (via Executive Copilot agent) + RAG. Advisory only:
never approves/sends/amends/reports/notifies. Drafts recommendations; formal submission goes through
the CP9 approval engine. Every interaction logged + RALPH-reviewed.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.repositories.executive_copilot_repository import ExecutiveCopilotRepository
from app.services.agent_service import AgentService
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService
from app.services.dashboard_service import DashboardService
from app.services.fds_service import FDSService
from app.services.rag_service import RAGService
from app.skills import registry as skill_registry

COPILOT_ROLES = {"super_admin", "jpn_admin", "executive"}
MANAGE_ROLES = {"super_admin", "jpn_admin"}


class CopilotPermissionError(Exception):
    pass


class ExecutiveCopilotService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ExecutiveCopilotRepository(db)
        self.audit = AuditService(db)

    def _authorise(self, current_user):
        if not (set(current_user.role_names) & COPILOT_ROLES):
            raise CopilotPermissionError("Executive Copilot is limited to Super Admin / JPN Admin / Executive.")

    @staticmethod
    def _ralph(text, citations):
        return skill_registry.get_skill("ralph_loop_review").run({
            "text": text, "citations": citations, "advisory_only": True,
            "human_review_required": False, "action": "",
        })

    # ----- briefing -----
    def briefing(self, *, current_user, organisation_id: str | None = None,
                 context: AuditContext | None = None):
        self._authorise(current_user)
        ds = DashboardService(self.db)
        overview = ds.overview(current_user, organisation_id=organisation_id)
        high_risk = ds.high_risk_kpis(current_user, organisation_id=organisation_id)
        fds_summary = FDSService(self.db).summary(current_user, organisation_id=organisation_id)

        # orchestrate specialist agents (advisory) — agent injects RAG via skill
        agent_out = AgentService(self.db).execute("executive_copilot", {"overview": overview}).get("output", {})
        summary_text = agent_out.get("summary", {}).get("text", "")

        evidence_available = bool(agent_out.get("citations"))  # RAG citations if any
        key_risks = [{"code": k["code"], "risk": k["risk_level"], "teras": k["teras_number"]}
                     for k in high_risk]
        suggested = []
        # use FDS specialist output if present
        fds_spec = agent_out.get("specialist_outputs", {}).get("financial_decision_support", {})
        rec = fds_spec.get("strategic_recommendation") if isinstance(fds_spec, dict) else None
        if rec and rec.get("recommended_action"):
            suggested.append(rec["recommended_action"])

        briefing = {
            "executive_summary": summary_text or
                f"{overview['total_kpis']} KPIs tracked; {len(key_risks)} high-risk; "
                f"{overview['missing_information']} incomplete.",
            "kpi_highlights": {"total_kpis": overview["total_kpis"], "by_teras": overview["by_teras"],
                               "achievement": overview["achievement"]},
            "key_risks": key_risks,
            "budget_fds_insights": fds_summary,
            "suggested_strategic_actions": suggested,
            "citations": agent_out.get("citations", []),
            "evidence_available": evidence_available,
            "evidence_note": None if evidence_available else
                "No knowledge-source citations available for this briefing.",
            "advisory_only": True,
            "human_review_required": True,
        }
        briefing["ralph_review"] = self._ralph(briefing["executive_summary"], briefing["citations"])
        self.repo.log(user_id=current_user.id, kind="briefing", question="(system briefing)",
                      answer=briefing["executive_summary"])
        self.audit.record(entity_type="executive_copilot", action="copilot_briefing",
                          actor_id=current_user.id, after={"organisation_id": organisation_id},
                          context=context, commit=False)
        self.db.commit()
        return briefing

    # ----- ask -----
    def ask(self, *, current_user, question: str, organisation_id: str | None = None,
            context: AuditContext | None = None):
        self._authorise(current_user)
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")
        rag = RAGService(self.db).query(query=question, actor_id=current_user.id)
        overview = DashboardService(self.db).overview(current_user, organisation_id=organisation_id)
        answer = rag["answer"]
        resp = {
            "question": question,
            "answer": answer,
            "citations": rag["citations"],
            "grounded": rag["grounded"],
            "fallback_used": rag["fallback"],
            "evidence_available": rag["grounded"],
            "evidence_note": None if rag["grounded"] else
                "No supporting evidence found in knowledge sources.",
            "context_highlights": {"total_kpis": overview["total_kpis"], "risk": overview["risk"]},
            "advisory_only": True,
            "human_review_required": False,
        }
        resp["ralph_review"] = self._ralph(answer, rag["citations"])
        self.repo.log(user_id=current_user.id, kind="ask", question=question, answer=answer,
                      grounded=rag["grounded"], fallback=rag["fallback"])
        self.audit.record(entity_type="executive_copilot", action="copilot_ask",
                          actor_id=current_user.id, after={"grounded": rag["grounded"]},
                          context=context, commit=False)
        self.db.commit()
        return resp

    # ----- recommendations (advisory draft) -----
    def create_recommendation(self, *, current_user, data: dict, context: AuditContext | None = None):
        self._authorise(current_user)
        rec = self.repo.create_recommendation(
            kpi_id=data["kpi_id"], content=data["content"],
            rationale=data.get("rationale"), priority=data.get("priority", 2),
        )
        self.audit.record(entity_type="strategic_recommendation", entity_id=rec.id,
                          action="copilot_recommendation_draft", actor_id=current_user.id,
                          context=context, commit=False)
        self.db.commit()
        return rec

    def submit_for_approval(self, *, current_user, rec_id, context: AuditContext | None = None):
        self._authorise(current_user)
        rec = self.repo.get_recommendation(rec_id)
        if not rec:
            return None
        approval = ApprovalService(self.db).create_request(
            item_type="copilot_recommendation", item_id=rec.id, requested_by=current_user.id,
            submit=True, context=context,
        )
        rec.status = "pending_approval"
        self.audit.record(entity_type="strategic_recommendation", entity_id=rec.id,
                          action="copilot_submit_for_approval", actor_id=current_user.id,
                          after={"approval_id": approval.id, "state": approval.state},
                          context=context, commit=False)
        self.db.commit()
        return {"recommendation_id": rec.id, "approval_id": approval.id,
                "approval_state": approval.state, "recommendation_status": rec.status}

    # ----- history -----
    def history(self, current_user):
        self._authorise(current_user)
        user_filter = None if (set(current_user.role_names) & MANAGE_ROLES) else current_user.id
        return self.repo.list_interactions(user_id=user_filter)
