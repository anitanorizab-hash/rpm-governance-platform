"""Skill registry (CP12): the 15 approved skills (A3), discoverable by name."""
from __future__ import annotations

from app.skills.audit_logging_skill import AuditLoggingSkill
from app.skills.citation_grounding_skill import CitationGroundingSkill
from app.skills.dashboard_summary_skill import DashboardSummarySkill
from app.skills.fds_skill import FDSSkill
from app.skills.kpi_analysis_skill import KPIAnalysisSkill
from app.skills.low_cost_high_impact_skill import LowCostHighImpactSkill
from app.skills.notification_writing_skill import NotificationWritingSkill
from app.skills.obb_analysis_skill import OBBAnalysisSkill
from app.skills.ralph_loop_review_skill import RalphLoopReviewSkill
from app.skills.rag_retrieval_skill import RAGRetrievalSkill
from app.skills.report_writing_skill import ReportWritingSkill
from app.skills.risk_scoring_skill import RiskScoringSkill
from app.skills.rpm_alignment_skill import RPMAlignmentSkill
from app.skills.strategic_recommendation_skill import StrategicRecommendationSkill
from app.skills.validation_skill import ValidationSkill

_SKILL_CLASSES = [
    KPIAnalysisSkill, ValidationSkill, RiskScoringSkill, FDSSkill, LowCostHighImpactSkill,
    OBBAnalysisSkill, StrategicRecommendationSkill, RPMAlignmentSkill, RAGRetrievalSkill,
    CitationGroundingSkill, ReportWritingSkill, NotificationWritingSkill, AuditLoggingSkill,
    DashboardSummarySkill, RalphLoopReviewSkill,
]

# name → skill instance
REGISTRY = {cls.name: cls() for cls in _SKILL_CLASSES}


def get_skill(name: str):
    return REGISTRY.get(name)


def list_skills():
    return [s.metadata() for s in REGISTRY.values()]
