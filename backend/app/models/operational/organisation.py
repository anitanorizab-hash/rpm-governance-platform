"""Organisation hierarchy model (V1.1) — OPERATIONAL plane.

JPN → PPD → School. Every KPI belongs to one Organisation (KPI.organisation_id).
Self-referential: a PPD's parent is its JPN; a School's parent (future) is its PPD.
Reference/master data — seeded in app.db.seed. No business logic here.
"""
from __future__ import annotations

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin, fk_uuid, uuid_pk


class Organisation(Base, TimestampMixin):
    __tablename__ = "organisation"
    id = uuid_pk()
    code = Column(String(64), unique=True, nullable=False)              # e.g. JPN, PPD-KINTA-UTARA
    name = Column(String(255), nullable=False)
    type = Column(String(32), nullable=False)                          # JPN | PPD | School
    parent_organisation_id = fk_uuid("organisation.id", nullable=True)  # JPN for a PPD; PPD for a School
    sector = Column(String(128))                                        # optional inherited context
    active = Column(Boolean, default=True, nullable=False)

    parent = relationship("Organisation", remote_side=[id], backref="children")
