"""Monthly update service (CP8): in-system PIC updates + deterministic analysis/risk.

In-system only (BR-002). One update per KPI/year/month (override replaces). Permission-scoped.
Every save audited. Triggers deterministic KPI analysis + risk (RiskAssessment). Never touches
KPI statement/indicator/target. No reports/notifications/AI here.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.repositories.kpi_repository import KPIRepository
from app.repositories.monthly_update_repository import MonthlyUpdateRepository
from app.schemas.monthly_update import FINANCE_STATUSES
from app.services import kpi_analysis_service as analysis
from app.services import risk_service
from app.services.audit_service import AuditService

MANAGE_ALL_ROLES = {"super_admin", "jpn_admin"}
VIEW_ONLY_ROLES = {"executive", "read_only"}


class PermissionError_(Exception):
    pass


class DuplicateUpdate(Exception):
    pass


class ValidationError_(Exception):
    pass


class MonthlyUpdateService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = MonthlyUpdateRepository(db)
        self.kpis = KPIRepository(db)
        self.audit = AuditService(db)

    # ---------- permission ----------
    def _can_update_kpi(self, current_user, kpi) -> bool:
        roles = set(current_user.role_names)
        if roles & VIEW_ONLY_ROLES and not (roles & MANAGE_ALL_ROLES):
            return False
        if roles & MANAGE_ALL_ROLES:
            return True
        if "sector_admin" in roles and kpi.sector and kpi.sector == current_user.scope:
            return True
        if "kpi_pic" in roles and kpi.pic and kpi.pic.email == current_user.email:
            return True
        return False

    # ---------- create ----------
    def create(self, *, current_user, data: dict, override: bool = False,
               context: AuditContext | None = None):
        if data.get("finance_status") and data["finance_status"] not in FINANCE_STATUSES:
            raise ValidationError_(f"finance_status must be one of {sorted(FINANCE_STATUSES)}")
        month, year = data["reporting_month"], data["reporting_year"]
        if not (1 <= month <= 12):
            raise ValidationError_("reporting_month must be 1–12")

        kpi = self.kpis.get(data["kpi_id"])
        if not kpi:
            return None
        if not self._can_update_kpi(current_user, kpi):
            raise PermissionError_("Not permitted to update this KPI")

        existing = self.repo.find_for_period(kpi.id, year, month)
        if existing and not override:
            raise DuplicateUpdate(
                f"A monthly update for {year}-{month:02d} already exists. Use override=true (admin)."
            )

        # deterministic analysis + risk (placeholder; AI later)
        target = kpi.targets[0].target_value if kpi.targets else None
        ach = data.get("achievement_value")
        status = analysis.achievement_status(ach, target)
        risk = risk_service.assess(ach, target, status)
        period = f"{year}-{month:02d}"

        if existing and override:
            upd = existing
            upd.achievement_value = ach
            upd.achievement_status = status
            upd.finance_status = data.get("finance_status")
            upd.evidence_ref = data.get("evidence_ref")
            upd.remarks = data.get("remarks")
            upd.issue_description = data.get("issue_description")
            upd.proposed_action = data.get("proposed_action")
            action = "monthly_update_override"
        else:
            upd = self.repo.create(
                kpi_id=kpi.id, period=period, reporting_year=year, reporting_month=month,
                achievement_value=ach, achievement_status=status,
                finance_status=data.get("finance_status"), evidence_ref=data.get("evidence_ref"),
                remarks=data.get("remarks"), issue_description=data.get("issue_description"),
                proposed_action=data.get("proposed_action"), submitted_by=current_user.id,
            )
            action = "monthly_update_create"

        # persist risk + reflect on KPI (derived fields only — NOT statement/indicator/target)
        self.repo.add_risk(kpi_id=kpi.id, period=period, risk_level=risk["risk_level"])
        kpi.status = status
        kpi.risk_level = risk["risk_level"]

        self.audit.record(
            entity_type="kpi_monthly_update", entity_id=upd.id, action=action,
            actor_id=current_user.id,
            after={"kpi_id": kpi.id, "period": period, "achievement_status": status,
                   "risk_level": risk["risk_level"], "finance_status": data.get("finance_status")},
            context=context, commit=False,
        )
        self.db.commit()
        return {"update": self.repo.get(upd.id), "achievement_status": status, "risk": risk}

    # ---------- read ----------
    def list_updates(self, *, kpi_id=None, year=None, month=None, limit=100, offset=0):
        return self.repo.list(kpi_id=kpi_id, year=year, month=month, limit=limit, offset=offset)

    def get(self, update_id: str):
        return self.repo.get(update_id)

    def patch(self, *, current_user, update_id: str, patch: dict, context: AuditContext | None = None):
        upd = self.repo.get(update_id)
        if not upd:
            return None
        kpi = self.kpis.get(upd.kpi_id)
        if not self._can_update_kpi(current_user, kpi):
            raise PermissionError_("Not permitted to update this KPI")
        if patch.get("finance_status") and patch["finance_status"] not in FINANCE_STATUSES:
            raise ValidationError_(f"finance_status must be one of {sorted(FINANCE_STATUSES)}")
        for field in ("achievement_value", "finance_status", "evidence_ref", "remarks",
                      "issue_description", "proposed_action"):
            if patch.get(field) is not None:
                setattr(upd, field, patch[field])
        # recompute status/risk if achievement changed
        target = kpi.targets[0].target_value if kpi.targets else None
        upd.achievement_status = analysis.achievement_status(upd.achievement_value, target)
        risk = risk_service.assess(upd.achievement_value, target, upd.achievement_status)
        kpi.status = upd.achievement_status
        kpi.risk_level = risk["risk_level"]
        self.audit.record(entity_type="kpi_monthly_update", entity_id=upd.id,
                          action="monthly_update_patch", actor_id=current_user.id,
                          after={"achievement_status": upd.achievement_status}, context=context, commit=False)
        self.db.commit()
        return {"update": self.repo.get(upd.id), "achievement_status": upd.achievement_status, "risk": risk}

    def summary(self):
        items = self.repo.list_all()
        by_status, by_risk = {}, {}
        for u in items:
            if u.achievement_status:
                by_status[u.achievement_status] = by_status.get(u.achievement_status, 0) + 1
        # risk from KPI level (latest)
        for u in items:
            kpi = self.kpis.get(u.kpi_id, include_deleted=True)
            lvl = kpi.risk_level if kpi else None
            if lvl:
                by_risk[lvl] = by_risk.get(lvl, 0) + 1
        return {"total_updates": len(items), "by_status": by_status, "by_risk": by_risk}
