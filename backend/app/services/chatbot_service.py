"""Chatbot service (CP15): sessions, role-scoped grounded answers via the KPI Chatbot Agent.

Role-scopes operational KPI context, runs the agent (RAG + citation + RALPH LOOP), logs the
conversation, and returns an advisory, cited answer. Never executes official actions.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.chatbot_repository import ChatbotRepository
from app.repositories.organisation_repository import OrganisationRepository
from app.services.agent_service import AgentService
from app.services.dashboard_service import DashboardService

ADMIN_BROAD = {"super_admin", "jpn_admin", "executive"}


class ChatbotError(Exception):
    pass


class ChatbotPermissionError(Exception):
    pass


class ChatbotService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ChatbotRepository(db)

    # ----- sessions -----
    def create_session(self, current_user):
        # Persist immediately: each API request uses a fresh DB session (get_db does not
        # commit on exit), so a flush-only create would be rolled back and 404 on the next call.
        s = self.repo.create_session(current_user.id)
        self.db.commit()
        return s

    def list_sessions(self, current_user):
        if set(current_user.role_names) & ADMIN_BROAD:
            return self.repo.list_sessions()
        return self.repo.list_sessions(user_id=current_user.id)

    def _accessible(self, current_user, session) -> bool:
        return (session.user_id == current_user.id) or bool(set(current_user.role_names) & ADMIN_BROAD)

    def get_session(self, current_user, session_id):
        s = self.repo.get_session(session_id)
        if not s:
            return None
        if not self._accessible(current_user, s):
            return "forbidden"
        return s

    def list_conversations(self, current_user, session_id):
        s = self.get_session(current_user, session_id)
        if s is None:
            return None
        if s == "forbidden":
            return "forbidden"
        return self.repo.list_conversations(session_id)

    # ----- role-scoped operational context -----
    def _operational_context(self, current_user, message: str, organisation_id=None) -> list[dict]:
        """Return KPI summaries the user MAY see and whose code is referenced in the message."""
        scoped = DashboardService(self.db)._scoped_kpis(current_user, organisation_id=organisation_id)
        msg = (message or "").lower()
        out = []
        for k in scoped:
            if k.code and k.code.lower() in msg:
                out.append({"code": k.code, "status": k.status,
                            "teras": (k.teras.number if k.teras else None),
                            "risk": k.risk_level})
        return out

    # Aggregate / data-intent triggers — questions answered from KPI figures, not specific codes.
    _AGG_TRIGGERS = (
        "how many", "how much", "number of", "count", "total", "overall", "summary",
        "overview", "breakdown", "high risk", "high-risk", "at risk", "medium risk",
        "low risk", "incomplete", "missing", "not updated", "on track", "on-track",
        "achieved", "status", "performance", "by teras", "which kpis", "list",
    )

    def _operational_summary(self, current_user, message: str, organisation_id=None,
                             force: bool = False, scope_label: str = "role-scoped") -> dict | None:
        """Role-scoped KPI aggregate stats for data-intent questions (BR-027 KPI-data grounding).

        Reuses DashboardService (role-scoping + completeness logic shared, not duplicated — BR-042).
        Returns None when the question shows no aggregate/data/organisation intent (unless forced).
        """
        msg = (message or "").lower()
        if not force and not any(t in msg for t in self._AGG_TRIGGERS):
            return None
        ds = DashboardService(self.db)
        ov = ds.overview(current_user, organisation_id=organisation_id)
        high = ds.high_risk_kpis(current_user, levels=("high",), organisation_id=organisation_id)
        return {
            "scope": scope_label,
            "total_kpis": ov["total_kpis"],
            "high_risk": ov["risk"].get("high", 0),
            "medium_risk": ov["risk"].get("medium", 0),
            "low_risk": ov["risk"].get("low", 0),
            "missing_information": ov["missing_information"],
            "by_risk": ov["risk"],
            "by_status": ov["achievement"],
            "by_completion": ov["completion"],
            "by_teras": ov["by_teras"],
            "high_risk_kpis": [
                {"code": h["code"], "teras": h["teras_number"], "pic": h["pic_email"]}
                for h in high[:10]
            ],
        }

    # ----- organisation-aware detection (V1.1) -----
    _COMPARE_TRIGGERS = (
        "compare", "comparison", "versus", " vs ", "banding", "bandingkan",
        "top performing", "best performing", "lowest", "worst", "highest risk ppd",
        "which ppd", "which district", "each ppd", "every ppd", "setiap ppd",
        "by ppd", "across ppd", "rank",
    )

    def _is_comparison(self, message: str) -> bool:
        msg = (message or "").lower()
        return any(t in msg for t in self._COMPARE_TRIGGERS)

    def _referenced_orgs(self, message: str) -> list:
        """Organisations whose name/code is mentioned in the message (V1.1)."""
        msg = (message or "").lower()
        matched = []
        for org in OrganisationRepository(self.db).list():
            candidates = {
                org.name.lower(),
                org.name.lower().replace("ppd ", "").replace("jpn ", ""),
                org.code.lower(),
                org.code.lower().replace("ppd-", "").replace("jpn-", "").replace("-", " "),
            }
            if any(len(c) > 2 and c in msg for c in candidates):
                matched.append(org)
        return matched

    @staticmethod
    def _compact_comparison(comp: dict) -> dict:
        def _name(item):
            return item["name"] if item else None
        return {
            "ppds": [{"name": p["name"], "total_kpis": p["total_kpis"], "achieved": p["achieved"],
                      "achievement_rate": p["achievement_rate"], "high_risk": p["high_risk"]}
                     for p in comp.get("ppds", [])],
            "top_performer": _name(comp.get("top_performer")),
            "lowest_performer": _name(comp.get("lowest_performer")),
            "highest_risk": _name(comp.get("highest_risk")),
        }

    # ----- messaging -----
    def send_message(self, *, current_user, session_id, message: str, achievement=None, target=None):
        if not message or not message.strip():
            raise ChatbotError("Message cannot be empty.")
        s = self.get_session(current_user, session_id)
        if s is None:
            return None
        if s == "forbidden":
            raise ChatbotPermissionError("Not permitted to use this session.")

        # V1.1: organisation-aware context. Detect referenced PPD(s) / comparison intent.
        referenced = self._referenced_orgs(message)
        comparison = self._is_comparison(message) or len(referenced) >= 2
        scope_org = referenced[0] if (referenced and not comparison) else None
        scope_label = f"{scope_org.type}: {scope_org.name}" if scope_org else "role-scoped"
        org_id = scope_org.id if scope_org else None

        op_context = self._operational_context(current_user, message, organisation_id=org_id)
        op_summary = self._operational_summary(current_user, message, organisation_id=org_id,
                                               force=bool(scope_org) or comparison,
                                               scope_label=scope_label)
        if comparison:
            comp = DashboardService(self.db).ppd_comparison(current_user)
            if op_summary is None:
                op_summary = {"scope": "ppd-comparison"}
            op_summary["ppd_comparison"] = self._compact_comparison(comp)

        agent_ctx = {"query": message, "operational_context": op_context,
                     "operational_summary": op_summary,
                     "achievement": achievement, "target": target}
        # AgentService injects the db session for RAG; logs AgentExecution.
        res = AgentService(self.db).execute("kpi_chatbot", agent_ctx)
        out = res.get("output", {})

        answer = out.get("answer", "")
        grounded = bool(out.get("grounded"))
        fallback_used = bool(out.get("fallback_used"))

        # log conversation (question + answer)
        self.repo.create_conversation(session_id=session_id, user_id=current_user.id,
                                       question=message, answer=answer,
                                       grounded=grounded, fallback=fallback_used)
        self.db.commit()

        return {
            "session_id": session_id,
            "question": message,
            "answer": answer,
            "citations": out.get("citations", []),
            "grounded": grounded,
            "fallback_used": fallback_used,
            "human_review_required": bool(out.get("human_review_required", False)),
            "ralph_review": out.get("ralph_review"),
            "operational_context": op_context,
            "operational_summary": op_summary,
        }
