"""Add KPI soft-delete columns is_deleted, deleted_at (CP7). Guarded on fresh DBs.

Revision ID: 0006_kpi_soft_delete
Revises: 0005_kpi_teras_nullable
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0006_kpi_soft_delete"
down_revision = "0005_kpi_teras_nullable"
branch_labels = None
depends_on = None


def _cols(bind, table):
    return {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "kpi")
    with op.batch_alter_table("kpi") as batch:
        if "is_deleted" not in existing:
            batch.add_column(sa.Column("is_deleted", sa.Boolean(), nullable=True))
        if "deleted_at" not in existing:
            batch.add_column(sa.Column("deleted_at", sa.DateTime(timezone=True)))
    op.execute("UPDATE kpi SET is_deleted = 0 WHERE is_deleted IS NULL")


def downgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "kpi")
    with op.batch_alter_table("kpi") as batch:
        for c in ("deleted_at", "is_deleted"):
            if c in existing:
                batch.drop_column(c)
