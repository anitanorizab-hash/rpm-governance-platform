"""Organisation service (V1.1): list/get the organisation hierarchy. Read-only, no AI."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.organisation_repository import OrganisationRepository


class OrganisationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrganisationRepository(db)

    def list_organisations(self, *, type_: str | None = None, parent_id: str | None = None):
        return self.repo.list(type_=type_, parent_id=parent_id)

    def get(self, org_id: str):
        return self.repo.get(org_id)
