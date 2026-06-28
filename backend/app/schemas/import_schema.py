"""Import schemas (CP6)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class RowWarning(BaseModel):
    row: int
    kpi_code: str | None = None
    missing_fields: list[str] = []


class ImportPreviewOut(BaseModel):
    plan_type: str
    total_rows: int
    sheets_parsed: int
    skipped_sheets: list[str] = []
    records_to_create: dict[str, int]      # e.g. {"kpi": 5, "pic": 3, ...}
    warnings: list[RowWarning] = []
    duplicate_risk: bool                   # same file already imported?
    file_hash: str


class ImportExecuteOut(BaseModel):
    batch_id: str
    plan_type: str
    rows_total: int
    rows_imported: int
    warnings_count: int
    status: str
    blocked: bool = False
    message: str | None = None


class ImportBatchOut(BaseModel):
    id: str
    filename: str | None = None
    plan_type: str | None = None
    organisation_id: str | None = None          # V1.1
    organisation_type: str | None = None         # V1.1 (resolved via organisation)
    organisation_name: str | None = None         # V1.1
    rows_total: int
    rows_imported: int
    warnings_count: int
    status: str
    imported_by: str | None = None
    created_at: datetime

    @classmethod
    def from_model(cls, m) -> "ImportBatchOut":
        org = getattr(m, "organisation", None)
        return cls(
            id=m.id, filename=m.filename, plan_type=m.plan_type,
            organisation_id=getattr(m, "organisation_id", None),
            organisation_type=(org.type if org else None),
            organisation_name=(org.name if org else None),
            rows_total=m.rows_total or 0,
            rows_imported=m.rows_imported or 0, warnings_count=m.warnings_count or 0,
            status=m.status, imported_by=m.imported_by, created_at=m.created_at,
        )
