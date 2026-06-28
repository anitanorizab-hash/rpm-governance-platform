"""PIC repository (V1.1.1 PIC Directory): CRUD, filters, KPI assignment, soft delete."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.operational.access import PIC
from app.models.operational.kpi import KPI


def _uid() -> str:
    return str(uuid.uuid4())


class PICRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, *, search=None, organisation_id=None, status=None, department=None,
             include_deleted=False) -> list[PIC]:
        stmt = select(PIC).options(selectinload(PIC.organisation))
        if not include_deleted:
            stmt = stmt.where(PIC.is_deleted.is_(False))
        if organisation_id:
            stmt = stmt.where(PIC.organisation_id == organisation_id)
        if status == "active":
            stmt = stmt.where(PIC.active.is_(True))
        elif status == "inactive":
            stmt = stmt.where(PIC.active.is_(False))
        if department:
            stmt = stmt.where(PIC.sector == department)
        if search:
            like = f"%{search.lower()}%"
            stmt = stmt.where(or_(func.lower(PIC.name).like(like),
                                  func.lower(func.coalesce(PIC.email, "")).like(like)))
        return list(self.db.scalars(stmt.order_by(PIC.name)))

    def get(self, pic_id: str, include_deleted: bool = False) -> PIC | None:
        p = self.db.get(PIC, pic_id)
        if p and p.is_deleted and not include_deleted:
            return None
        return p

    def get_by_email(self, email: str) -> PIC | None:
        return self.db.scalar(select(PIC).where(PIC.email == email, PIC.is_deleted.is_(False)))

    def create(self, **kw) -> PIC:
        p = PIC(id=_uid(), active=kw.pop("active", True), is_deleted=False, **kw)
        self.db.add(p); self.db.flush()
        return p

    def assigned_kpis(self, pic_id: str) -> list[KPI]:
        return list(self.db.scalars(
            select(KPI).where(KPI.pic_id == pic_id, KPI.is_deleted.is_(False)).order_by(KPI.code)))

    def assigned_count(self, pic_id: str) -> int:
        return self.db.scalar(
            select(func.count()).select_from(KPI)
            .where(KPI.pic_id == pic_id, KPI.is_deleted.is_(False))) or 0

    def assign_kpis(self, pic_id: str, kpi_ids: list[str]) -> int:
        n = 0
        for kid in kpi_ids:
            k = self.db.get(KPI, kid)
            if k and not k.is_deleted:
                k.pic_id = pic_id; n += 1
        self.db.flush()
        return n

    def soft_delete(self, pic: PIC) -> None:
        pic.is_deleted = True
        pic.active = False
        pic.deleted_at = datetime.now(timezone.utc)
        self.db.flush()
