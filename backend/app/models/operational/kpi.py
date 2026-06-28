"""KPI core models (CP3) — OPERATIONAL plane.

KPI, KPIIndicator, KPITarget, Activity, KPIMonthlyUpdate, RiskAssessment, AlignmentScore.
Indicator/Target are separated from KPI to support amendment history (BR-008).
"""
from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin, fk_uuid, uuid_pk


class KPI(Base, TimestampMixin):
    __tablename__ = "kpi"
    # V1.1.1: KPI code is unique PER organisation (national codes repeat across PPDs).
    __table_args__ = (UniqueConstraint("organisation_id", "code", name="uq_kpi_organisation_id_code"),)
    id = uuid_pk()
    code = Column(String(64), nullable=False)   # TSx.Sy.Pz.KPIn (unique within an organisation)
    # Nullable so messy import rows with an unresolved Teras are stored + flagged (BR-005/006),
    # rather than failing the whole import. Completeness warnings surface the gap for follow-up.
    teras_id = fk_uuid("teras.id", nullable=True)
    prakarsa_id = fk_uuid("prakarsa.id")
    statement = Column(Text)                # amendment-controlled (BR-008)
    keberhasilan = Column(Text)
    department_id = fk_uuid("department.id")
    sector = Column(String(128))
    pic_id = fk_uuid("pic.id")
    organisation_id = fk_uuid("organisation.id", nullable=True)   # V1.1: owning org (JPN/PPD/School)
    quick_win = Column(Boolean, default=False)
    year_assigned = Column(Integer)
    status = Column(String(32))             # derived (on-track/lagging/achieved)
    risk_level = Column(String(32))         # derived
    is_deleted = Column(Boolean, default=False, nullable=False)   # soft delete (CP7)
    deleted_at = Column(DateTime(timezone=True))

    teras = relationship("Teras")
    pic = relationship("PIC")
    organisation = relationship("Organisation")
    indicators = relationship("KPIIndicator", back_populates="kpi")
    targets = relationship("KPITarget", back_populates="kpi")
    activities = relationship("Activity", back_populates="kpi")
    monthly_updates = relationship("KPIMonthlyUpdate", back_populates="kpi")


class KPIIndicator(Base, TimestampMixin):
    __tablename__ = "kpi_indicator"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    indicator_text = Column(Text)           # amendment-controlled
    unit = Column(String(64))
    kpi = relationship("KPI", back_populates="indicators")


class KPITarget(Base, TimestampMixin):
    __tablename__ = "kpi_target"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    year = Column(Integer)
    target_value = Column(String(128))      # amendment-controlled
    tov = Column(String(128))               # take-off value / baseline
    tov_type = Column(String(32))           # "value" | "KPI Baharu"
    kpi = relationship("KPI", back_populates="targets")


class Activity(Base, TimestampMixin):
    __tablename__ = "activity"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    type = Column(String(32))               # utama | sokongan
    description = Column(Text)
    milestone = Column(Text)
    nota_pengiraan = Column(Text)
    status = Column(String(64))             # V1.1.1: activity progress (e.g. Status Pelaksanaan Aktiviti)
    remarks = Column(Text)                  # V1.1.1: Catatan / operational notes
    kpi = relationship("KPI", back_populates="activities")


class KPIMonthlyUpdate(Base, TimestampMixin):
    __tablename__ = "kpi_monthly_update"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    period = Column(String(7), nullable=False)   # YYYY-MM (derived from year+month)
    reporting_year = Column(Integer)             # CP8
    reporting_month = Column(Integer)            # CP8 (1–12)
    achievement = Column(String(255))            # legacy free-text
    achievement_value = Column(String(64))       # CP8 raw value (e.g. "85%", "3")
    achievement_status = Column(String(32))      # CP8 derived: achieved/on_track/at_risk/off_track/not_updated
    finance_status = Column(String(32))          # CP8 six-value code
    budget_status_id = fk_uuid("budget_status.id")
    evidence_ref = Column(String(512))
    remarks = Column(Text)
    issue_description = Column(Text)             # CP8
    proposed_action = Column(Text)              # CP8
    submitted_by = fk_uuid("user.id")
    kpi = relationship("KPI", back_populates="monthly_updates")


class RiskAssessment(Base, TimestampMixin):
    __tablename__ = "risk_assessment"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    period = Column(String(7))
    risk_level = Column(String(32))         # at_risk | critical | low | …
    method = Column(String(64))             # rule-based (V1)


class AlignmentScore(Base, TimestampMixin):
    """KPI↔RPM alignment (cross-plane reference to a knowledge source)."""
    __tablename__ = "alignment_score"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    rpm_source_id = fk_uuid("knowledge_source.id")   # cross-plane logical link
    strength = Column(Float)
