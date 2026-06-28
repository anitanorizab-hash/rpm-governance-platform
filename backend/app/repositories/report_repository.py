"""Report repository (CP17)."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operational.governance import Report


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kw) -> Report:
        r = Report(id=str(uuid.uuid4()), **kw); self.db.add(r); self.db.flush(); return r

    def get(self, report_id: str) -> Report | None:
        return self.db.get(Report, report_id)

    def list(self, limit=100, offset=0):
        return list(self.db.scalars(
            select(Report).order_by(Report.created_at.desc()).limit(limit).offset(offset)
        ))
