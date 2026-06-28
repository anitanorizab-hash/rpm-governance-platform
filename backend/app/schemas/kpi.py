"""KPI schemas (CP7)."""
from __future__ import annotations

from pydantic import BaseModel, Field


class KPIListItem(BaseModel):
    id: str
    code: str
    statement: str | None = None
    teras_number: int | None = None
    sector: str | None = None
    status: str | None = None
    pic_email: str | None = None
    organisation_id: str | None = None       # V1.1 (enables org-scoped UI filtering)
    is_complete: bool


class KPIDetail(BaseModel):
    id: str
    code: str
    statement: str | None = None
    teras_number: int | None = None
    sector: str | None = None
    status: str | None = None
    indicators: list[str] = []
    targets: list[str] = []
    activities: list[str] = []
    pic_name: str | None = None
    pic_email: str | None = None
    financial_allocation_total: float | None = None
    is_complete: bool
    missing_fields: list[str] = []


class KPICreateIn(BaseModel):
    code: str = Field(min_length=1)
    statement: str | None = None
    teras_id: str | None = None
    indicator: str | None = None
    target: str | None = None
    department: str | None = None


class KPIPatchIn(BaseModel):
    # amendable (Jul/Oct only)
    statement: str | None = None
    indicator: str | None = None
    target: str | None = None
    # editable anytime
    status: str | None = None
    department: str | None = None


class PICAssignIn(BaseModel):
    name: str
    email: str
    sector: str | None = None


class CompletenessOut(BaseModel):
    kpi_id: str
    code: str
    is_complete: bool
    missing_fields: list[str] = []


class CompletenessSummaryOut(BaseModel):
    total_kpis: int
    complete: int
    incomplete: int
    missing_field_counts: dict[str, int] = {}
