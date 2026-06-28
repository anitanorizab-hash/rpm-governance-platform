"""S12 Notification Writing Skill (CP12) — AI-assisted with deterministic fallback. Draft only (no send)."""
from __future__ import annotations

from app.skills.base import Skill, safe_chat

TEMPLATES = {
    "reminder": "Reminder: please submit your monthly KPI update for {kpi}.",
    "missing_info": "Action needed: KPI {kpi} has missing information: {detail}.",
    "escalation": "Escalation: KPI {kpi} update is overdue. Please act.",
    "approval": "An item requires your approval: {detail}.",
}


class NotificationWritingSkill(Skill):
    name = "notification_writing"
    description = "Draft reminder/alert/escalation text (AI via adapter; template fallback). Never sends."
    deterministic = False
    uses_provider = True

    def run(self, payload: dict) -> dict:
        ntype = payload.get("type", "reminder")
        kpi = payload.get("kpi", "your KPI")
        detail = payload.get("detail", "")
        template = TEMPLATES.get(ntype, TEMPLATES["reminder"]).format(kpi=kpi, detail=detail)
        result = safe_chat(
            [{"role": "user", "content": f"Draft a short {ntype} notification: kpi={kpi}, detail={detail}"}],
            fallback=template,
        )
        return {"draft": result["text"], "type": ntype, "source": result["source"], "sent": False}
