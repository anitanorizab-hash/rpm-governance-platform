"""FDS schemas (CP11)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class FDSAnalysisOut(BaseModel):
    kpi_id: str
    code: str
    advisory_only: bool = True
    budget_intelligence: dict
    low_cost_high_impact: dict
    obb_analysis: dict
    strategic_recommendation: dict
    recommendation_id: str | None = None


class RecommendationOut(BaseModel):
    id: str
    kpi_id: str
    type: str | None = None
    content: str | None = None
    rationale: str | None = None
    priority: int | None = None
    status: str | None = None
    created_at: datetime

    @classmethod
    def from_model(cls, m) -> "RecommendationOut":
        return cls(id=m.id, kpi_id=m.kpi_id, type=m.type, content=m.content,
                   rationale=m.rationale, priority=m.priority, status=m.status, created_at=m.created_at)


class SubmitForApprovalOut(BaseModel):
    recommendation_id: str
    approval_id: str
    approval_state: str
    recommendation_status: str


class FDSSummaryOut(BaseModel):
    total_recommendations: int
    by_status: dict[str, int]
    by_priority: dict[int, int]
    financial_risk_distribution: dict[str, int]
