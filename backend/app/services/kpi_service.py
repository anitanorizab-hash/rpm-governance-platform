"""KPI service (CP7): CRUD, PIC assignment, completeness, amendment-window control, soft delete.

All mutations audited. Amendable fields (statement/indicator/target) gated to Jul/Oct unless Super
Admin override (BR-008). No monthly updates created here.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.models.operational.governance import KPIAmendment
from app.repositories.kpi_repository import KPIRepository
from app.services import amendment_service, completeness_service
from app.services.audit_service import AuditService

MANAGE_ALL_ROLES = {"super_admin", "jpn_admin"}


class AmendmentBlocked(Exception):
    pass


class KPIService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = KPIRepository(db)
        self.audit = AuditService(db)

    # ---------- read (scoped) ----------
    def list_kpis(self, *, current_user, teras=None, sector=None, pic=None, status=None,
                  completeness=None, organisation_id=None, include_removed=False, limit=100, offset=0):
        # kpi_pic sees only their assigned KPIs (by their email)
        roles = set(current_user.role_names)
        pic_filter = pic
        if "kpi_pic" in roles and not (roles & MANAGE_ALL_ROLES):
            pic_filter = current_user.email
        # only admins may include removed (inactive) KPIs
        include_removed = include_removed and bool(roles & MANAGE_ALL_ROLES)
        items = self.repo.list(teras_number=teras, sector=sector, pic_email=pic_filter,
                               status=status, organisation_id=organisation_id,
                               include_deleted=include_removed, limit=limit, offset=offset)
        if completeness == "incomplete":
            items = [k for k in items if not completeness_service.is_complete(k)]
        elif completeness == "complete":
            items = [k for k in items if completeness_service.is_complete(k)]
        return items

    def get_kpi(self, kpi_id: str):
        return self.repo.get(kpi_id)

    # ---------- completeness ----------
    def completeness(self, kpi):
        missing = completeness_service.kpi_missing_fields(kpi)
        return {"kpi_id": kpi.id, "code": kpi.code, "is_complete": not missing, "missing_fields": missing}

    def completeness_summary(self):
        items = self.repo.all_active()
        total = len(items)
        incomplete = [k for k in items if not completeness_service.is_complete(k)]
        # missing counts by field
        field_counts: dict[str, int] = {}
        for k in incomplete:
            for f in completeness_service.kpi_missing_fields(k):
                field_counts[f] = field_counts.get(f, 0) + 1
        return {
            "total_kpis": total,
            "complete": total - len(incomplete),
            "incomplete": len(incomplete),
            "missing_field_counts": field_counts,
        }

    # ---------- RBAC for management ----------
    @staticmethod
    def _can_manage(current_user, kpi=None) -> bool:
        roles = set(current_user.role_names)
        if roles & MANAGE_ALL_ROLES:
            return True
        if "sector_admin" in roles and kpi is not None and kpi.sector and kpi.sector == current_user.scope:
            return True
        return False

    # ---------- create ----------
    def create_kpi(self, *, current_user, data: dict, context: AuditContext | None = None):
        if not (set(current_user.role_names) & MANAGE_ALL_ROLES):
            return "forbidden"
        kpi = self.repo.create(
            code=data["code"], teras_id=data.get("teras_id"),
            statement=data.get("statement"), sector=data.get("department"),
        )
        if data.get("indicator"):
            self.repo.set_indicator(kpi, data["indicator"])
        if data.get("target"):
            self.repo.set_target(kpi, data["target"])
        self.audit.record(entity_type="kpi", entity_id=kpi.id, action="kpi_create",
                          actor_id=current_user.id, after={"code": kpi.code}, context=context, commit=False)
        self.db.commit()
        return self.repo.get(kpi.id)

    # ---------- update / amendment ----------
    def update_kpi(self, *, current_user, kpi_id: str, patch: dict, override: bool = False,
                   context: AuditContext | None = None):
        kpi = self.repo.get(kpi_id)
        if not kpi:
            return None
        if not self._can_manage(current_user, kpi):
            return "forbidden"

        is_super = "super_admin" in set(current_user.role_names)
        allowed, reason = amendment_service.amendment_allowed(patch, is_super_admin=is_super, override=override)
        if not allowed:
            raise AmendmentBlocked(reason)

        changes = {}
        # amendable fields (audited as KPIAmendment)
        if patch.get("statement") is not None:
            old, kpi.statement = kpi.statement, patch["statement"]
            self._record_amendment(kpi, "statement", old, patch["statement"], current_user, override)
            changes["statement"] = patch["statement"]
        if patch.get("indicator") is not None:
            old, new = self.repo.set_indicator(kpi, patch["indicator"])
            self._record_amendment(kpi, "indicator", old, new, current_user, override)
            changes["indicator"] = new
        if patch.get("target") is not None:
            old, new = self.repo.set_target(kpi, patch["target"])
            self._record_amendment(kpi, "target", old, new, current_user, override)
            changes["target"] = new
        # non-amendable fields (editable anytime)
        if patch.get("status") is not None:
            kpi.status = patch["status"]; changes["status"] = patch["status"]
        if patch.get("department") is not None:
            kpi.sector = patch["department"]; changes["department"] = patch["department"]

        self.audit.record(entity_type="kpi", entity_id=kpi.id, action="kpi_update",
                          actor_id=current_user.id, after=changes, context=context, commit=False)
        self.db.commit()
        return self.repo.get(kpi.id)

    def _record_amendment(self, kpi, field, old, new, current_user, override):
        self.db.add(KPIAmendment(
            id=str(uuid.uuid4()), kpi_id=kpi.id, field=field,
            old_value=(str(old) if old is not None else None), new_value=str(new),
            actor_id=current_user.id,
            reason=("super_admin override" if override else "amendment window"),
        ))
        self.db.flush()

    # ---------- PIC assignment ----------
    def assign_pic(self, *, current_user, kpi_id: str, name: str, email: str, sector: str | None,
                   context: AuditContext | None = None):
        kpi = self.repo.get(kpi_id)
        if not kpi:
            return None
        if not self._can_manage(current_user, kpi):
            return "forbidden"
        pic = self.repo.get_or_create_pic(name=name, email=email, sector=sector)
        old_pic = kpi.pic_id
        kpi.pic_id = pic.id
        if sector:
            kpi.sector = sector
        self.audit.record(entity_type="kpi", entity_id=kpi.id, action="assign_pic",
                          actor_id=current_user.id, before={"pic_id": old_pic},
                          after={"pic_email": email}, context=context, commit=False)
        self.db.commit()
        return self.repo.get(kpi.id)

    # ---------- activity progress (operational; NOT amendment-gated) ----------
    def _can_update_activity(self, current_user, kpi) -> bool:
        if self._can_manage(current_user, kpi):
            return True
        roles = set(current_user.role_names)
        # the KPI's assigned PIC may update activity progress
        return ("kpi_pic" in roles and kpi.pic is not None
                and kpi.pic.email and kpi.pic.email == current_user.email)

    def update_activity(self, *, current_user, kpi_id: str, activity_id: str, fields: dict,
                        context: AuditContext | None = None):
        kpi = self.repo.get(kpi_id)
        if not kpi:
            return None
        act = self.repo.get_activity(activity_id)
        if not act or act.kpi_id != kpi_id:
            return None
        if not self._can_update_activity(current_user, kpi):
            return "forbidden"
        changes = {}
        for f in ("description", "milestone", "status", "remarks"):
            if fields.get(f) is not None:
                setattr(act, f, fields[f]); changes[f] = fields[f]
        self.db.flush()
        self.audit.record(entity_type="activity", entity_id=act.id, action="activity_update",
                          actor_id=current_user.id, after={"kpi_id": kpi_id, **changes},
                          context=context, commit=False)
        self.db.commit()
        return self.repo.get(kpi_id)

    # ---------- soft delete / removal (V1.1.3: reason + org context, audited) ----------
    def soft_delete(self, *, current_user, kpi_id: str, reason: str | None = None,
                    context: AuditContext | None = None):
        kpi = self.repo.get(kpi_id)
        if not kpi:
            return None
        if not (set(current_user.role_names) & MANAGE_ALL_ROLES):
            return "forbidden"
        removed_at = datetime.now(timezone.utc)
        org = kpi.organisation
        kpi.is_deleted = True
        kpi.deleted_at = removed_at
        kpi.status = kpi.status  # unchanged; remains for history
        self.audit.record(
            entity_type="kpi", entity_id=kpi.id, action="kpi_remove",
            actor_id=current_user.id, reason=reason,
            after={
                "kpi_id": kpi.id, "kpi_code": kpi.code, "kpi_statement": kpi.statement,
                "organisation_level": (org.type if org else None),
                "organisation_name": (org.name if org else None),
                "removed_by": current_user.id, "removed_at": removed_at.isoformat(),
                "reason": reason,
            },
            context=context, commit=False)
        self.db.commit()
        return True
