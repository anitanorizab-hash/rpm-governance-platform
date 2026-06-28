"""Organisation API (V1.1) — list the JPN → PPD hierarchy. JWT; read-only; additive."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.organisation import OrganisationOut
from app.services.organisation_service import OrganisationService

router = APIRouter(prefix="/organisations", tags=["organisations"])


@router.get("", response_model=list[OrganisationOut])
def list_organisations(type: str | None = Query(default=None),
                       parent_id: str | None = Query(default=None),
                       current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = OrganisationService(db).list_organisations(type_=type, parent_id=parent_id)
    return [OrganisationOut.from_model(o) for o in rows]
