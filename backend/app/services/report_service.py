"""Report service (CP17): generate draft → submit-for-review (CP9) → status syncs → archive.

No auto-issue, no email, no auto-publish. Generation uses dashboard/KPI/risk/FDS + Report Generation
Agent (which composes report_writing/dashboard_summary/citation_grounding/RALPH). Audited.
"""
from __future__ import annotations

import json

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.repositories.approval_repository import ApprovalRepository
from app.repositories.report_repository import ReportRepository
from app.services.agent_service import AgentService
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService
from app.services.dashboard_service import DashboardService
from app.services.fds_service import FDSService

MANAGE_ROLES = {"super_admin", "jpn_admin", "executive"}


class ReportPermissionError(Exception):
    pass


class ReportStateError(Exception):
    pass


class ReportService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReportRepository(db)
        self.approvals = ApprovalRepository(db)
        self.audit = AuditService(db)

    def _can_manage(self, current_user) -> bool:
        return bool(set(current_user.role_names) & MANAGE_ROLES)

    # ----- generate -----
    def generate(self, *, current_user, period: str, type_: str = "monthly",
                 context: AuditContext | None = None):
        if not self._can_manage(current_user):
            raise ReportPermissionError("Not permitted to generate reports")
        ds = DashboardService(self.db)
        overview = ds.overview(current_user)
        high_risk = ds.high_risk_kpis(current_user)
        fds_summary = FDSService(self.db).summary(current_user)

        stats = {"total_kpis": overview["total_kpis"], "high_risk": len(high_risk),
                 "missing_information": overview["missing_information"]}
        agent_out = AgentService(self.db).execute(
            "report_generation", {"period": period, "stats": stats, "overview": overview}
        ).get("output", {})

        sections = {
            "title": f"KPI Report — {period}",
            "reporting_period": period,
            "summary": agent_out.get("summary"),
            "narrative": agent_out.get("narrative"),
            "kpi_achievement_overview": overview["achievement"],
            "by_teras": overview["by_teras"],
            "risk_summary": overview["risk"],
            "budget_fds_summary": fds_summary,
            "missing_information_summary": overview["missing_information"],
            "recommendations": agent_out.get("ralph_review", {}).get("verdict"),
            "citations": agent_out.get("citations", []),
            "advisory_only": True,
            "human_review_required": True,
            "ralph_review": agent_out.get("ralph_review"),
        }
        report = self.repo.create(
            title=sections["title"], period=period, type=type_, status="draft",
            content=json.dumps(sections, default=str), summary=agent_out.get("summary"),
            generated_by=current_user.id,
        )
        self.audit.record(entity_type="report", entity_id=report.id, action="report_generate",
                          actor_id=current_user.id, after={"period": period}, context=context, commit=False)
        self.db.commit()
        return self._view(report)

    # ----- status sync from CP9 approval -----
    def _sync(self, report):
        if report.approval_id and report.status == "pending_review":
            ap = self.approvals.get(report.approval_id)
            if ap and ap.state == "approved":
                report.status = "approved"; report.approved_by = ap.actor_id
            elif ap and ap.state == "rejected":
                report.status = "rejected"; report.reject_reason = ap.comment or "rejected"
            if ap and ap.state in ("approved", "rejected"):
                self.db.commit()
        return report

    def _view(self, report) -> dict:
        try:
            content = json.loads(report.content) if report.content else {}
        except Exception:
            content = {}
        return {"id": report.id, "title": report.title, "period": report.period, "type": report.type,
                "status": report.status, "summary": report.summary, "reject_reason": report.reject_reason,
                "approval_id": report.approval_id, "generated_by": report.generated_by,
                "content": content}

    # ----- reads -----
    def list_reports(self, current_user):
        return [self._view(self._sync(r)) for r in self.repo.list()]

    def get_report(self, current_user, report_id):
        r = self.repo.get(report_id)
        if not r:
            return None
        return self._view(self._sync(r))

    def patch(self, *, current_user, report_id, fields: dict, context=None):
        if not self._can_manage(current_user):
            raise ReportPermissionError("Not permitted to edit reports")
        r = self.repo.get(report_id)
        if not r:
            return None
        if r.status != "draft":
            raise ReportStateError("Only draft reports can be edited.")
        if fields.get("title"):
            r.title = fields["title"]
        if fields.get("summary"):
            r.summary = fields["summary"]
        self.audit.record(entity_type="report", entity_id=r.id, action="report_patch",
                          actor_id=current_user.id, context=context, commit=False)
        self.db.commit()
        return self._view(r)

    # ----- submit for review (CP9) -----
    def submit_for_review(self, *, current_user, report_id, context: AuditContext | None = None):
        if not self._can_manage(current_user):
            raise ReportPermissionError("Not permitted to submit reports")
        r = self.repo.get(report_id)
        if not r:
            return None
        if r.status != "draft":
            raise ReportStateError(f"Report is '{r.status}'; only drafts can be submitted.")
        approval = ApprovalService(self.db).create_request(
            item_type="report", item_id=r.id, requested_by=current_user.id, submit=True, context=context)
        r.status = "pending_review"; r.approval_id = approval.id
        self.audit.record(entity_type="report", entity_id=r.id, action="report_submit_for_review",
                          actor_id=current_user.id, after={"approval_id": approval.id}, context=context, commit=False)
        self.db.commit()
        return {"report_id": r.id, "approval_id": approval.id, "approval_state": approval.state,
                "report_status": r.status}

    # ----- archive -----
    def archive(self, *, current_user, report_id, context: AuditContext | None = None):
        if not self._can_manage(current_user):
            raise ReportPermissionError("Not permitted to archive reports")
        r = self.repo.get(report_id)
        if not r:
            return None
        self._sync(r)
        if r.status != "approved":
            raise ReportStateError(f"Only approved reports can be archived (current: {r.status}).")
        r.status = "archived"; r.archive_ref = f"archive/{r.id}"
        self.audit.record(entity_type="report", entity_id=r.id, action="report_archive",
                          actor_id=current_user.id, context=context, commit=False)
        self.db.commit()
        return self._view(r)
