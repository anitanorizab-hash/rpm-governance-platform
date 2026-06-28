"""Add monthly-update fields (CP8). Guarded on fresh DBs.

Revision ID: 0007_monthly_update_fields
Revises: 0006_kpi_soft_delete
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0007_monthly_update_fields"
down_revision = "0006_kpi_soft_delete"
branch_labels = None
depends_on = None

_COLUMNS = (
    ("reporting_year", sa.Integer()),
    ("reporting_month", sa.Integer()),
    ("achievement_value", sa.String(length=64)),
    ("achievement_status", sa.String(length=32)),
    ("finance_status", sa.String(length=32)),
    ("issue_description", sa.Text()),
    ("proposed_action", sa.Text()),
)


def _cols(bind, table):
    return {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "kpi_monthly_update")
    with op.batch_alter_table("kpi_monthly_update") as batch:
        for name, type_ in _COLUMNS:
            if name not in existing:
                batch.add_column(sa.Column(name, type_, nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "kpi_monthly_update")
    with op.batch_alter_table("kpi_monthly_update") as batch:
        for name, _ in _COLUMNS:
            if name in existing:
                batch.drop_column(name)
