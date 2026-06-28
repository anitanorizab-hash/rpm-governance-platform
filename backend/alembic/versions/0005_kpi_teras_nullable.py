"""Make kpi.teras_id nullable (CP6 fix) so incomplete import rows are stored + flagged, not failed.

Revision ID: 0005_kpi_teras_nullable
Revises: 0004_import_batch
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0005_kpi_teras_nullable"
down_revision = "0004_import_batch"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("kpi") as batch:
        batch.alter_column("teras_id", existing_type=sa.String(length=36), nullable=True)


def downgrade() -> None:
    with op.batch_alter_table("kpi") as batch:
        batch.alter_column("teras_id", existing_type=sa.String(length=36), nullable=False)
