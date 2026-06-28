"""Import repository (CP6): entity lookup/create for the import pipeline + batch persistence."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operational.access import Department, PIC, Teras
from app.models.operational.imports import ImportBatch
from app.models.operational.kpi import KPI, Activity, KPIIndicator, KPITarget


def _uid() -> str:
    return str(uuid.uuid4())


class ImportRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- lookups / creates ---
    def get_teras_by_number(self, number: int) -> Teras | None:
        return self.db.scalar(select(Teras).where(Teras.number == number))

    def get_or_create_department(self, name: str) -> Department:
        dept = self.db.scalar(select(Department).where(Department.name == name))
        if not dept:
            dept = Department(id=_uid(), name=name)
            self.db.add(dept); self.db.flush()
        return dept

    def get_or_create_pic(self, *, name: str, email: str, sector: str | None, dept_id: str | None) -> PIC:
        pic = self.db.scalar(select(PIC).where(PIC.email == email))
        if not pic:
            pic = PIC(id=_uid(), name=name, email=email, sector=sector, department_id=dept_id)
            self.db.add(pic); self.db.flush()
        return pic

    def get_kpi_by_code(self, code: str) -> KPI | None:
        return self.db.scalar(select(KPI).where(KPI.code == code))

    def create_kpi(self, **kw) -> KPI:
        kpi = KPI(id=_uid(), **kw)
        self.db.add(kpi); self.db.flush()
        return kpi

    def add_indicator(self, kpi_id: str, indicator_text: str) -> None:
        self.db.add(KPIIndicator(id=_uid(), kpi_id=kpi_id, indicator_text=indicator_text)); self.db.flush()

    def add_target(self, kpi_id: str, target_value: str, tov: str | None) -> None:
        self.db.add(KPITarget(id=_uid(), kpi_id=kpi_id, target_value=target_value, tov=tov)); self.db.flush()

    def add_activity(self, kpi_id: str, description: str) -> None:
        self.db.add(Activity(id=_uid(), kpi_id=kpi_id, type="utama", description=description)); self.db.flush()

    # --- batch / import-once ---
    def find_completed_batch_by_hash(self, file_hash: str) -> ImportBatch | None:
        return self.db.scalar(
            select(ImportBatch).where(
                ImportBatch.file_hash == file_hash, ImportBatch.status == "completed"
            )
        )

    def create_batch(self, **kw) -> ImportBatch:
        batch = ImportBatch(id=_uid(), **kw)
        self.db.add(batch); self.db.flush()
        return batch

    def list_batches(self, limit: int = 100, offset: int = 0) -> list[ImportBatch]:
        return list(self.db.scalars(
            select(ImportBatch).order_by(ImportBatch.created_at.desc()).limit(limit).offset(offset)
        ))

    def get_batch(self, batch_id: str) -> ImportBatch | None:
        return self.db.get(ImportBatch, batch_id)
