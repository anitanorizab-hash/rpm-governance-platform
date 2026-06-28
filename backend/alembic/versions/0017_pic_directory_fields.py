"""V1.1.1 PIC Directory: add pic.organisation_id, active, is_deleted, deleted_at. Guarded.

Revision ID: 0017_pic_directory
Revises: 0016_pic_email_nullable
Create Date: 2026-06-28
"""
from alembic import op
import sqlalchemy as sa

revision = "0017_pic_directory"
down_revision = "0016_pic_email_nullable"
branch_labels = None
depends_on = None

_COLUMNS = (
    ("organisation_id", sa.String(length=36)),
    ("active", sa.Boolean()),
    ("is_deleted", sa.Boolean()),
    ("deleted_at", sa.DateTime(timezone=True)),
)


def _cols(bind, table):
    return {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "pic")
    with op.batch_alter_table("pic") as batch:
        for name, type_ in _COLUMNS:
            if name not in existing:
                batch.add_column(sa.Column(name, type_, nullable=True))
    # default existing rows to active + not-deleted
    op.execute("UPDATE pic SET active = 1 WHERE active IS NULL")
    op.execute("UPDATE pic SET is_deleted = 0 WHERE is_deleted IS NULL")


def downgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "pic")
    with op.batch_alter_table("pic") as batch:
        for name, _ in reversed(_COLUMNS):
            if name in existing:
                batch.drop_column(name)
