"""Add Report fields: title, content, summary, reject_reason, approval_id (CP17). Guarded.

Revision ID: 0010_report_fields
Revises: 0009_document_content
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0010_report_fields"
down_revision = "0009_document_content"
branch_labels = None
depends_on = None

_COLUMNS = (
    ("title", sa.String(length=512)),
    ("content", sa.Text()),
    ("summary", sa.Text()),
    ("reject_reason", sa.Text()),
    ("approval_id", sa.String(length=36)),
)


def _cols(bind, table):
    return {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "report")
    with op.batch_alter_table("report") as batch:
        for name, type_ in _COLUMNS:
            if name not in existing:
                batch.add_column(sa.Column(name, type_, nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "report")
    with op.batch_alter_table("report") as batch:
        for name, _ in _COLUMNS:
            if name in existing:
                batch.drop_column(name)
