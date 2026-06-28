"""KPI repository (CP7): queries/mutations for KPI management. Soft-delete aware."""
from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.operational.access import PIC, Teras
from app.models.operational.kpi import KPI, KPIIndicator, KPITarget


def _uid() -> str:
    return str(uuid.uuid4())


class KPIRepository:
    def __init__(self, db: Session):
        self.db = db

    def _detail_opts(self):
        return (
            selectinload(KPI.indicators), selectinload(KPI.targets),
            selectinload(KPI.activities), selectinload(KPI.pic), selectinload(KPI.teras),
        )

    def get(self, kpi_id: str, include_deleted: bool = False) -> KPI | None:
        kpi = self.db.scalar(select(KPI).options(*self._detail_opts()).where(KPI.id == kpi_id))
        if kpi and kpi.is_deleted and not include_deleted:
            return None
        return kpi

    def list(self, *, teras_number=None, sector=None, pic_email=None, status=None,
             limit=100, offset=0) -> list[KPI]:
        stmt = select(KPI).options(*self._detail_opts()).where(KPI.is_deleted.is_(False))
        if teras_number is not None:
            t = self.db.scalar(select(Teras).where(Teras.number == teras_number))
            stmt = stmt.where(KPI.teras_id == (t.id if t else "__none__"))
        if sector:
            stmt = stmt.where(KPI.sector == sector)
        if pic_email:
            pic_ids = [p.id for p in self.db.scalars(select(PIC).where(PIC.email == pic_email))]
            stmt = stmt.where(KPI.pic_id.in_(pic_ids or ["__none__"]))
        if status:
            stmt = stmt.where(KPI.status == status)
        stmt = stmt.order_by(KPI.code).limit(limit).offset(offset)
        return list(self.db.scalars(stmt))

    def all_active(self) -> list[KPI]:
        return list(self.db.scalars(
            select(KPI).options(*self._detail_opts()).where(KPI.is_deleted.is_(False))
        ))

    def create(self, **kw) -> KPI:
        kpi = KPI(id=_uid(), is_deleted=False, **kw)
        self.db.add(kpi); self.db.flush()
        return kpi

    def get_or_create_pic(self, *, name, email, sector) -> PIC:
        pic = self.db.scalar(select(PIC).where(PIC.email == email)) if email else None
        if not pic:
            pic = PIC(id=_uid(), name=name, email=email, sector=sector)
            self.db.add(pic); self.db.flush()
        else:
            if name:
                pic.name = name
            if sector:
                pic.sector = sector
            self.db.flush()
        return pic

    def set_indicator(self, kpi: KPI, text: str) -> tuple[str | None, str]:
        if kpi.indicators:
            ind = kpi.indicators[0]; old = ind.indicator_text; ind.indicator_text = text
        else:
            old = None
            self.db.add(KPIIndicator(id=_uid(), kpi_id=kpi.id, indicator_text=text))
        self.db.flush()
        return old, text

    def set_target(self, kpi: KPI, value: str) -> tuple[str | None, str]:
        if kpi.targets:
            tg = kpi.targets[0]; old = tg.target_value; tg.target_value = value
        else:
            old = None
            self.db.add(KPITarget(id=_uid(), kpi_id=kpi.id, target_value=value))
        self.db.flush()
        return old, value
