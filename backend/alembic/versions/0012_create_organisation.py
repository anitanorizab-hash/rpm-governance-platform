"""Create organisation table (V1.1) — JPN → PPD → School hierarchy. Guarded.

Revision ID: 0012_create_organisation
Revises: 0011_notification_fields
Create Date: 2026-06-28
"""
from alembic import op
import sqlalchemy as sa

revision = "0012_create_organisation"
down_revision = "0011_notification_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if sa.inspect(bind).has_table("organisation"):
        return
    op.create_table(
        "organisation",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("parent_organisation_id", sa.String(length=36), nullable=True),
        sa.Column("sector", sa.String(length=128), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_organisation"),
        sa.UniqueConstraint("code", name="uq_organisation_code"),
        sa.ForeignKeyConstraint(
            ["parent_organisation_id"], ["organisation.id"],
            name="fk_organisation_parent_organisation_id_organisation",
        ),
    )
    op.create_index("ix_organisation_type", "organisation", ["type"])


def downgrade() -> None:
    bind = op.get_bind()
    if not sa.inspect(bind).has_table("organisation"):
        return
    op.drop_index("ix_organisation_type", table_name="organisation")
    op.drop_table("organisation")
