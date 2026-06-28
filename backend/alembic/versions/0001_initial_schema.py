"""Initial schema + reference seed (CP3).

Creates all tables from Base.metadata (operational + knowledge + AI groups) and seeds reference data
(roles, Teras 1–7, budget statuses, July/October amendment windows). No real KPI data.

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-27
"""
from alembic import op
from sqlalchemy.orm import Session

from app.db.base import Base
import app.models  # noqa: F401  (populate metadata)
from app.db.seed import seed_reference_data

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)
    with Session(bind=bind) as session:
        seed_reference_data(session)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
