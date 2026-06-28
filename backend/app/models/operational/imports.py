"""Import batch model (CP6) — OPERATIONAL plane. Records each one-time Excel import."""
from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin, fk_uuid, uuid_pk


class ImportBatch(Base, TimestampMixin):
    __tablename__ = "import_batch"
    id = uuid_pk()
    filename = Column(String(512))
    file_hash = Column(String(64), index=True)     # sha256 → import-once lock
    plan_type = Column(String(16))                 # jpn | ppd
    rows_total = Column(Integer, default=0)
    rows_imported = Column(Integer, default=0)
    warnings_count = Column(Integer, default=0)
    status = Column(String(16), default="completed")  # completed | failed
    warnings = Column(Text)                        # JSON list of warnings
    imported_by = fk_uuid("user.id")
    organisation_id = fk_uuid("organisation.id", nullable=True)   # V1.1: org this import targets

    organisation = relationship("Organisation")
