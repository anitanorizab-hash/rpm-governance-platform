"""Monthly update schemas (CP8)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

FINANCE_STATUSES = {
    "received", "will_be_received", "pending", "not_received", "not_required", "insufficient",
}


class MonthlyUpdateIn(BaseModel):
    kpi_id: str
    reporting_year: int = Field(ge=2020, le=2100)
    reporting_month: int = Field(ge=1, le=12)
    achievement_value: str | None = None
    finance_status: str | None = None
    evidence_ref: str | None = None
    remarks: str | None = None
    issue_description: str | None = None
    proposed_action: str | None = None


class MonthlyUpdatePatch(BaseModel):
    achievement_value: str | None = None
    finance_status: str | None = None
    evidence_ref: str | None = None
    remarks: str | None = None
    issue_description: str | None = None
    proposed_action: str | None = None


class MonthlyUpdateOut(BaseModel):
    id: str
    kpi_id: str
    reporting_year: int | None = None
    reporting_month: int | None = None
    achievement_value: str | None = None
    achievement_status: str | None = None
    finance_status: str | None = None
    evidence_ref: str | None = None
    remarks: str | None = None
    issue_description: str | None = None
    proposed_action: str | None = None
    created_at: datetime

    @classmethod
    def from_model(cls, m) -> "MonthlyUpdateOut":
        return cls(
            id=m.id, kpi_id=m.kpi_id, reporting_year=m.reporting_year, reporting_month=m.reporting_month,
            achievement_value=m.achievement_value, achievement_status=m.achievement_status,
            finance_status=m.finance_status, evidence_ref=m.evidence_ref, remarks=m.remarks,
            issue_description=m.issue_description, proposed_action=m.proposed_action, created_at=m.created_at,
        )


class MonthlyUpdateSummaryOut(BaseModel):
    total_updates: int
    by_status: dict[str, int] = {}
    by_risk: dict[str, int] = {}
