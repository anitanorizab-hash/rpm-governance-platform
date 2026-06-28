"""Notification Agent (CP18) — composes notification_writing + ralph_loop_review + audit_logging.

Drafts only (subject/body); HITL; NEVER sends. Used by the notification service to build drafts.
"""
from __future__ import annotations

from app.agents.base import Agent


class NotificationAgent(Agent):
    name = "notification"
    description = "Draft reminders/alerts/escalations (subject+body); human approval required before send."
    uses_skills = ["notification_writing", "ralph_loop_review", "audit_logging"]
    human_review_required = True

    def run(self, context: dict) -> dict:
        ntype = context.get("type", "reminder")
        kpi = context.get("kpi", "your KPI")
        detail = context.get("detail", "")
        writing = self.skill("notification_writing", {"type": ntype, "kpi": kpi, "detail": detail})
        subject = context.get("subject") or f"{ntype.replace('_', ' ').title()} notification"
        ralph = self.skill("ralph_loop_review", {
            "text": writing["draft"], "citations": [], "advisory_only": True,
            "human_review_required": True, "actionable": True, "requires_citation": False,
        })
        audit = self.skill("audit_logging", {"entity_type": "notification", "action": "draft"})
        return self._wrap({"subject": subject, "body": writing["draft"], "type": ntype,
                           "source": writing["source"], "ralph_review": ralph,
                           "audit_entry": audit, "sent": False})
