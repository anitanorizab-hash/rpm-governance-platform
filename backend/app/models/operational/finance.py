"""Financial Decision Support models (CP3) — OPERATIONAL plane.

FinancialAllocation, OBBAnalysis, LowCostHighImpactAnalysis, StrategicRecommendation.
"""
from __future__ import annotations

from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin, fk_uuid, uuid_pk


class FinancialAllocation(Base, TimestampMixin):
    __tablename__ = "financial_allocation"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    activity_id = fk_uuid("activity.id")
    object_code = Column(String(16))        # OS21000 … OS42000
    amount = Column(Float)
    budget_status_id = fk_uuid("budget_status.id")
    warrant = Column(Float)
    expenditure = Column(Float)
    frequency = Column(String(32))
    # monthly projections Jan..Dec
    jan = Column(Float); feb = Column(Float); mar = Column(Float); apr = Column(Float)
    may = Column(Float); jun = Column(Float); jul = Column(Float); aug = Column(Float)
    sep = Column(Float); oct = Column(Float); nov = Column(Float); dec = Column(Float)
    jumlah = Column(Float)


class OBBAnalysis(Base, TimestampMixin):
    __tablename__ = "obb_analysis"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    period = Column(String(7))
    vfm_indicator = Column(String(64))      # value-for-money indicator
    rationale = Column(Text)


class LowCostHighImpactAnalysis(Base, TimestampMixin):
    __tablename__ = "low_cost_high_impact_analysis"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    activity_id = fk_uuid("activity.id")
    cost = Column(Float)
    impact = Column(Float)
    quadrant = Column(String(32))           # low-cost-high-impact, etc.
    recommendation_id = fk_uuid("strategic_recommendation.id")


class StrategicRecommendation(Base, TimestampMixin):
    """Human-reviewed recommendation (FDS/Intervention). Linked to its raw AI log via source_ai_rec_id."""
    __tablename__ = "strategic_recommendation"
    id = uuid_pk()
    kpi_id = fk_uuid("kpi.id", nullable=False)
    type = Column(String(32))               # LCHI | Intervention | ResourceOpt | OBB
    content = Column(Text)
    rationale = Column(Text)
    priority = Column(Integer)
    status = Column(String(32))             # draft | approved | rejected
    reviewed_by = fk_uuid("user.id")
    source_ai_rec_id = fk_uuid("ai_recommendation.id")   # link to AI metadata (no duplication)
