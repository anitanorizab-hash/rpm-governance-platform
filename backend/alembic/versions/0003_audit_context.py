"""Add audit request-context columns: ip_address, user_agent, request_id (CP5).

Guarded no-op on fresh DBs (0001 create_all already includes them); adds columns to pre-CP5 DBs.

Revision ID: 0003_audit_context
Revises: 0002_user_password
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0003_audit_context"
down_revision = "0002_user_password"
branch_labels = None
depends_on = None

_COLUMNS = (
    ("ip_address", sa.String(length=64)),
    ("user_agent", sa.String(length=512)),
    ("request_id", sa.String(length=64)),
)


def _cols(bind, table):
    return {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "audit_log")
    to_add = [(n, t) for n, t in _COLUMNS if n not in existing]
    if not to_add:
        return
    with op.batch_alter_table("audit_log") as batch:
        for name, type_ in to_add:
            batch.add_column(sa.Column(name, type_, nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "audit_log")
    with op.batch_alter_table("audit_log") as batch:
        for name, _ in _COLUMNS:
            if name in existing:
                batch.drop_column(name)
