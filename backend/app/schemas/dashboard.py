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
    status: str | None = None
    risk: str | None = None
    finance_status: str | None = None


class ExecutiveSummaryOut(BaseModel):
    generated_by: str          # "deterministic" (AI later)
    text: str
    highlights: dict[str, object]
