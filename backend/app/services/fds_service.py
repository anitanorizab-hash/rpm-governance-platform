"""Financial Decision Support orchestrator (CP11) — deterministic, advisory only. No AI provider.

Composes Budget Intelligence + Low Cost High Impact + OBB + Strategic Recommendation. Outputs are
advisory; FDS never approves/executes. Recommendations route to the CP9 approval engine only on
explicit request. Role-scoped + audited.
"""
from __future__ import annotations

from collections import Counter

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.repositories.fds_repository import FDSRepository
from app.services import low_cost_high_impact_service as lchi
from app.services import obb_service
from app.services import strategic_recommendation_service as strat
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService

FINANCE_RISK = {
    "received": "low",
    "not_required": "low",
    "will_be_received": "medium",
    "pending": "medium",
    "insufficient": "high",
    "not_received": "high",
}
FUNDING_GAP_STATUSES = {"pending", "not_received", "insufficient"}

FDS_MANAGE_ROLES = {"super_admin", "jpn_admin", "sector_admin", "finance_officer"}


class FDSPermissionError(Exception):
    pass


class FDSService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = FDSRepository(db)
        self.audit = AuditService(db)

    # ---------- scoping ----------
    @staticmethod
    def _can_view(current_user, kpi) -> bool:
        roles = set(current_user.role_names)
        if roles & {"super_admin", "jpn_admin", "executive", "read_only", "finance_officer", "ppd_admin"}:
            return True
        if "sector_admin" in roles:
            return kpi.sector and kpi.sector == current_user.scope
        if "kpi_pic" in roles:
            return kpi.pic and kpi.pic.email == current_user.email
        return False

    @staticmethod
    def _can_manage(current_user) -> bool:
        return bool(set(current_user.role_names) & FDS_MANAGE_ROLES)

    # ---------- budget intelligence ----------
    @staticmethod
    def budget_intelligence(finance_status: str | None) -> dict:
        status = finance_status or "not_reported"
        risk = FINANCE_RISK.get(status, "medium")
        gap = status in FUNDING_GAP_STATUSES
        summary = (
            f"Finance status '{status}' → financial risk {risk}."
            + (" Funding gap detected." if gap else "")
        )
        return {"finance_status": status, "financial_risk": risk, "funding_gap": gap, "summary": summary}

    # ---------- analysis (no persistence) ----------
    def analyze_kpi(self, *, current_user, kpi_id: str):
        kpi = self.repo.get_kpi(kpi_id)
        if not kpi:
            return None
        if not self._can_view(current_user, kpi):
            raise FDSPermissionError("Not permitted to view FDS for this KPI")

        cost_total, expenditure = self.repo.allocation_totals(kpi_id)
        upd = self.repo.latest_update(kpi_id)
        finance_status = upd.finance_status if upd else None
        achievement = upd.achievement_value if upd else None
        target = kpi.targets[0].target_value if kpi.targets else None

        bi = self.budget_intelligence(finance_status)
        m = lchi.analyze(cost_total=cost_total, achievement=achievement, target=target)
        obb = obb_service.analyze(kpi=kpi, cost_total=cost_total, expenditure=expenditure,
                                  achievement=achievement, target=target,
                                  cost_level=m["cost_level"], impact_level=m["impact_level"])
        rec = strat.build(finance_risk=bi["financial_risk"], funding_gap=bi["funding_gap"],
                          quadrant=m["quadrant"], vfm=obb["value_for_money"])
        return {
            "kpi_id": kpi.id, "code": kpi.code,
            "advisory_only": True,
            "budget_intelligence": bi,
            "low_cost_high_impact": m,
            "obb_analysis": obb,
            "strategic_recommendation": rec,
        }

    # ---------- generate (persist recommendation + OBB + LCHI; audited) ----------
    def generate(self, *, current_user, kpi_id: str, context: AuditContext | None = None):
        if not self._can_manage(current_user):
            raise FDSPermissionError("Not permitted to generate FDS recommendations")
        analysis = self.analyze_kpi(current_user=current_user, kpi_id=kpi_id)
        if analysis is None:
            return None

        m, obb, rec = (analysis["low_cost_high_impact"], analysis["obb_analysis"],
                       analysis["strategic_recommendation"])
        self.repo.create_lchi(kpi_id=kpi_id, cost=m["cost_total"], impact=None, quadrant=m["quadrant"])
        self.repo.create_obb(kpi_id=kpi_id, vfm_indicator=obb["value_for_money"], rationale=obb["resource_use"])
        recommendation = self.repo.create_recommendation(
            kpi_id=kpi_id, type="FDS", content=rec["recommended_action"],
            rationale=rec["rationale"], priority=rec["priority"], status="draft",
            reviewed_by=None,
        )
        self.audit.record(entity_type="strategic_recommendation", entity_id=recommendation.id,
                          action="fds_generate", actor_id=current_user.id,
                          after={"kpi_id": kpi_id, "quadrant": m["quadrant"],
                                 "financial_risk": analysis["budget_intelligence"]["financial_risk"],
                                 "priority": rec["priority"]},
                          context=context, commit=False)
        self.db.commit()
        analysis["recommendation_id"] = recommendation.id
        return analysis

    # ---------- recommendations ----------
    def list_recommendations(self, kpi_id=None):
        return self.repo.list_recommendations(kpi_id=kpi_id)

    def get_recommendation(self, rec_id: str):
        return self.repo.get_recommendation(rec_id)

    def submit_for_approval(self, *, current_user, rec_id: str, context: AuditContext | None = None):
        if not self._can_manage(current_user):
            raise FDSPermissionError("Not permitted to submit FDS recommendations")
        rec = self.repo.get_recommendation(rec_id)
        if not rec:
            return None
        # Route to the CP9 approval engine (creates a pending request; does NOT approve).
        approval = ApprovalService(self.db).create_request(
            item_type="recommendation", item_id=rec.id, requested_by=current_user.id,
            submit=True, context=context,
        )
        rec.status = "pending_approval"
        self.audit.record(entity_type="strategic_recommendation", entity_id=rec.id,
                          action="fds_submit_for_approval", actor_id=current_user.id,
                          after={"approval_id": approval.id, "approval_state": approval.state},
                          context=context, commit=False)
        self.db.commit()
        return {"recommendation_id": rec.id, "approval_id": approval.id,
                "approval_state": approval.state, "recommendation_status": rec.status}

    # ---------- summary ----------
    def summary(self, current_user):
        recs = self.repo.list_recommendations()
        kpis = self.repo.all_kpis_active()
        # finance risk distribution from latest updates
        risk_dist = Counter()
        for k in kpis:
            upd = self.repo.latest_update(k.id)
            risk_dist[self.budget_intelligence(upd.finance_status if upd else None)["financial_risk"]] += 1
        return {
            "total_recommendations": len(recs),
            "by_status": dict(Counter(r.status for r in recs)),
            "by_priority": dict(Counter(r.priority for r in recs)),
            "financial_risk_distribution": dict(risk_dist),
        }
