"""Add Document.content + extract_error (CP14). Guarded on fresh DBs.

Revision ID: 0009_document_content
Revises: 0008_approval_state
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0009_document_content"
down_revision = "0008_approval_state"
branch_labels = None
depends_on = None

_COLUMNS = (("content", sa.Text()), ("extract_error", sa.String(length=512)))


def _cols(bind, table):
    return {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "document")
    with op.batch_alter_table("document") as batch:
        for name, type_ in _COLUMNS:
            if name not in existing:
                batch.add_column(sa.Column(name, type_, nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "document")
    with op.batch_alter_table("document") as batch:
        for name, _ in _COLUMNS:
            if name in existing:
                batch.drop_column(name)
