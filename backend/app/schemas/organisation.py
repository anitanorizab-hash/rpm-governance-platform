"""Organisation schemas (V1.1)."""
from __future__ import annotations

from pydantic import BaseModel


class OrganisationOut(BaseModel):
    id: str
    code: str
    name: str
    type: str                                   # JPN | PPD | School
    parent_organisation_id: str | None = None
    sector: str | None = None
    active: bool

    @classmethod
    def from_model(cls, o):
        return cls(id=o.id, code=o.code, name=o.name, type=o.type,
                   parent_organisation_id=o.parent_organisation_id,
                   sector=o.sector, active=o.active)
