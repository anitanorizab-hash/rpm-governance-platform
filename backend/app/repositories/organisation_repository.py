"""Organisation repository (V1.1): reads for the JPN → PPD → School hierarchy."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operational.organisation import Organisation


class OrganisationRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, *, type_: str | None = None, parent_id: str | None = None,
             active_only: bool = True) -> list[Organisation]:
        stmt = select(Organisation)
        if type_:
            stmt = stmt.where(Organisation.type == type_)
        if parent_id:
            stmt = stmt.where(Organisation.parent_organisation_id == parent_id)
        if active_only:
            stmt = stmt.where(Organisation.active.is_(True))
        return list(self.db.scalars(stmt.order_by(Organisation.name)))

    def get(self, org_id: str) -> Organisation | None:
        return self.db.get(Organisation, org_id)

    def get_by_code(self, code: str) -> Organisation | None:
        return self.db.scalar(select(Organisation).where(Organisation.code == code))
