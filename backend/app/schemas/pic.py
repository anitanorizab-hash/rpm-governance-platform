"""PIC Directory schemas (V1.1.1)."""
from __future__ import annotations

from pydantic import BaseModel, Field


class PICOut(BaseModel):
    id: str
    name: str
    email: str | None = None
    organisation_id: str | None = None
    organisation_name: str | None = None
    department: str | None = None
    active: bool = True
    assigned_kpi_count: int = 0
    assigned_kpi_codes: list[str] = []

    @classmethod
    def from_model(cls, p, *, assigned_count: int = 0, assigned_codes=None) -> "PICOut":
        return cls(
            id=p.id, name=p.name, email=p.email,
            organisation_id=p.organisation_id,
            organisation_name=(p.organisation.name if p.organisation else None),
            department=p.sector, active=bool(p.active),
            assigned_kpi_count=assigned_count, assigned_kpi_codes=assigned_codes or [],
        )


class PICCreateIn(BaseModel):
    name: str = Field(min_length=1)
    email: str | None = None
    organisation_id: str | None = None
    department: str | None = None
    active: bool = True


class PICPatchIn(BaseModel):
    name: str | None = None
    email: str | None = None
    organisation_id: str | None = None
    department: str | None = None
    active: bool | None = None


class PICAssignKpisIn(BaseModel):
    kpi_ids: list[str]


class PICImportOut(BaseModel):
    created: int
    updated: int
