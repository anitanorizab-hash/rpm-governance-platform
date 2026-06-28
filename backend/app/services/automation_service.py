"""Automation service (V1.1.1) — administrator-triggered, HITL-SAFE draft generation.

Generates DRAFTS only (monthly report + PIC/missing-info/overdue notification drafts) by reusing the
existing ReportService / NotificationService. Drafts must still be submitted for approval; nothing is
queued or sent here. A notification draft is skipped when its KPI's PIC has no valid email (a valid
recipient + approval + configured SMTP remain required before any real send). Every draft is audited
by the underlying services.
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.services.dashboard_service import DashboardService
from app.services.notification_service import NotificationService
from app.services.report_service import ReportService

AUTOMATION_ROLES = {"super_admin", "jpn_admin"}
ALL_TYPES = ("monthly_report", "pic_reminders", "missing_info", "overdue_escalations")


class AutomationPermissionError(Exception):
    pass


def _this_period() -> str:
    now = datetime.now(timezone.utc)
    return f"{now.year}-{now.month:02d}"


def _valid_email(email: str | None) -> bool:
    return bool(email and "@" in email and not email.endswith((".local", ".unassigned")))


class AutomationService:
    def __init__(self, db: Session):
        self.db = db

    def _authorise(self, current_user):
        if not (set(current_user.role_names) & AUTOMATION_ROLES):
            raise AutomationPermissionError("Automation is limited to Super Admin / JPN Admin.")

    def run(self, *, current_user, types=None, period: str | None = None, limit: int = 10,
            context: AuditContext | None = None) -> dict:
        self._authorise(current_user)
        types = [t for t in (types or ALL_TYPES) if t in ALL_TYPES]
        generated: dict[str, int] = {}
        skipped: dict[str, int] = {}

        if "monthly_report" in types:
            ReportService(self.db).generate(
                current_user=current_user, period=(period or _this_period()), context=context)
            generated["monthly_report"] = 1

        if any(t in types for t in ("pic_reminders", "missing_info", "overdue_escalations")):
            notif = NotificationService(self.db)
            rows = DashboardService(self.db)._build(current_user)

            def draft(kpi, ntype, detail) -> bool:
                email = kpi.pic.email if kpi.pic else None
                if not _valid_email(email):
                    return False
                notif.draft(current_user=current_user,
                            data={"type": ntype, "recipient": email, "kpi": kpi.code, "detail": detail},
                            context=context)
                return True

            if "pic_reminders" in types:
                g = s = 0
                for r in rows:
                    if g >= limit:
                        break
                    ok = draft(r["kpi"], "reminder",
                               f"Monthly KPI update reminder for {r['kpi'].code}.")
                    g, s = g + int(ok), s + int(not ok)
                generated["pic_reminders"], skipped["pic_reminders_no_email"] = g, s

            if "missing_info" in types:
                g = s = 0
                for r in (x for x in rows if x["missing"]):
                    if g >= limit:
                        break
                    ok = draft(r["kpi"], "missing_info",
                               f"Missing information for {r['kpi'].code}: {', '.join(r['missing'])}.")
                    g, s = g + int(ok), s + int(not ok)
                generated["missing_info"], skipped["missing_info_no_email"] = g, s

            if "overdue_escalations" in types:
                g = s = 0
                for r in (x for x in rows if x["status"] == "not_updated"):
                    if g >= limit:
                        break
                    ok = draft(r["kpi"], "escalation",
                               f"Overdue KPI update escalation for {r['kpi'].code}.")
                    g, s = g + int(ok), s + int(not ok)
                generated["overdue_escalations"], skipped["overdue_no_email"] = g, s

        return {
            "generated": generated,
            "skipped_no_valid_email": skipped,
            "note": "Drafts only — submit for approval; send requires approval + valid email + SMTP config.",
        }
