"""Add Approval.state + requested_by (CP9). Guarded on fresh DBs.

Revision ID: 0008_approval_state
Revises: 0007_monthly_update_fields
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0008_approval_state"
down_revision = "0007_monthly_update_fields"
branch_labels = None
depends_on = None

_COLUMNS = (
    ("state", sa.String(length=20)),
    ("requested_by", sa.String(length=36)),
)


def _cols(bind, table):
    return {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "approval")
    with op.batch_alter_table("approval") as batch:
        for name, type_ in _COLUMNS:
            if name not in existing:
                batch.add_column(sa.Column(name, type_, nullable=True))
    op.execute("UPDATE approval SET state = 'draft' WHERE state IS NULL")


def downgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "approval")
    with op.batch_alter_table("approval") as batch:
        for name, _ in _COLUMNS:
            if name in existing:
                batch.drop_column(name)
