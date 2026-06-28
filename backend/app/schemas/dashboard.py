"""Dashboard schemas (CP10)."""
from __future__ import annotations

from pydantic import BaseModel


class OverviewOut(BaseModel):
    total_kpis: int
    by_teras: dict[int, int]
    achievement: dict[str, int]
    risk: dict[str, int]
    completion: dict[str, int]
    missing_information: int
    finance: dict[str, int]


class TerasSummaryItem(BaseModel):
    teras_number: int
    kpi_count: int
    achievement: dict[str, int]
    risk: dict[str, int]
    completion: dict[str, int]
    missing_information: int
    finance: dict[str, int]


class RiskSummaryOut(BaseModel):
    overall: dict[str, int]
    by_teras: dict[int, dict[str, int]]


class BudgetSummaryOut(BaseModel):
    overall: dict[str, int]
    by_teras: dict[int, dict[str, int]]


class SubmissionSummaryOut(BaseModel):
    period: str
    overall: dict[str, int]
    by_teras: dict[int, dict[str, int]]


class HighRiskKPIItem(BaseModel):
    kpi_id: str
    code: str
    statement: str | None = None
    teras_number: int | None = None
    pic_email: str | None = None
    risk_level: str | None = None


class KPIMappingRow(BaseModel):
    kpi_id: str
    code: str
    teras_number: int | None = None
    pic: str | None = None
    sector: str | None = None
    organisation_type: str | None = None      # V1.1.3 (JPN / PPD)
    organisation_name: str | None = None       # V1.1.3
    status: str | None = None
    risk: str | None = None
    finance_status: str | None = None


class ExecutiveSummaryOut(BaseModel):
    generated_by: str          # "deterministic" (AI later)
    text: str
    highlights: dict[str, object]


# ---------- Organisation-aware comparison (V1.1) ----------
class PPDComparisonItem(BaseModel):
    organisation_id: str
    code: str
    name: str
    type: str
    rank: int
    total_kpis: int
    achieved: int
    achievement_rate: float
    high_risk: int
    missing_information: int
    achievement: dict[str, int]
    risk: dict[str, int]
    finance: dict[str, int]
    by_teras: dict[int, int]


class PPDComparisonOut(BaseModel):
    parent_organisation_id: str | None = None
    ppd_count: int
    ppds: list[PPDComparisonItem]
    top_performer: PPDComparisonItem | None = None
    lowest_performer: PPDComparisonItem | None = None
    highest_risk: PPDComparisonItem | None = None
