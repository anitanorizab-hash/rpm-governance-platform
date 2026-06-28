"""V1.1.1: make pic.email nullable (imported PICs have no email until captured). Guarded.

Revision ID: 0016_pic_email_nullable
Revises: 0015_kpi_org_unique_activity
Create Date: 2026-06-28
"""
from alembic import op
import sqlalchemy as sa

revision = "0016_pic_email_nullable"
down_revision = "0015_kpi_org_unique_activity"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("pic") as batch:
        batch.alter_column("email", existing_type=sa.String(length=255), nullable=True)


def downgrade() -> None:
    op.execute("UPDATE pic SET email = '' WHERE email IS NULL")
    with op.batch_alter_table("pic") as batch:
        batch.alter_column("email", existing_type=sa.String(length=255), nullable=False)
