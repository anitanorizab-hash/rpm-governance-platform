"""Add User.password_hash (CP4).

Revision ID: 0002_user_password
Revises: 0001_initial
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_user_password"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def _has_column(bind, table: str, column: str) -> bool:
    return column in {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade() -> None:
    """Add User.password_hash if it is not already present.

    Note: migration 0001 builds the schema via Base.metadata.create_all on the live model
    metadata, which already includes password_hash on a fresh database. This guard makes 0002
    a safe no-op there, while still adding the column to any pre-CP4 database. The chain stays
    consistent in both cases.
    """
    bind = op.get_bind()
    if _has_column(bind, "user", "password_hash"):
        return  # already created by 0001 on a fresh DB
    with op.batch_alter_table("user") as batch:
        batch.add_column(sa.Column("password_hash", sa.String(length=255), nullable=True))
    op.execute("UPDATE \"user\" SET password_hash = '!' WHERE password_hash IS NULL")
    with op.batch_alter_table("user") as batch:
        batch.alter_column("password_hash", existing_type=sa.String(length=255), nullable=False)


def downgrade() -> None:
    bind = op.get_bind()
    if _has_column(bind, "user", "password_hash"):
        with op.batch_alter_table("user") as batch:
            batch.drop_column("password_hash")
