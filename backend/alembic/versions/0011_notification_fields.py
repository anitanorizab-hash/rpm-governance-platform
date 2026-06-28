"""Add Notification fields (CP18): subject, body, related_entity_type/id, approval_id,
failure_reason, created_by. Guarded.

Revision ID: 0011_notification_fields
Revises: 0010_report_fields
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0011_notification_fields"
down_revision = "0010_report_fields"
branch_labels = None
depends_on = None

_COLUMNS = (
    ("subject", sa.String(length=512)),
    ("body", sa.Text()),
    ("related_entity_type", sa.String(length=48)),
    ("related_entity_id", sa.String(length=36)),
    ("approval_id", sa.String(length=36)),
    ("failure_reason", sa.Text()),
    ("created_by", sa.String(length=36)),
)


def _cols(bind, table):
    return {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "notification")
    with op.batch_alter_table("notification") as batch:
        for name, type_ in _COLUMNS:
            if name not in existing:
                batch.add_column(sa.Column(name, type_, nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    existing = _cols(bind, "notification")
    with op.batch_alter_table("notification") as batch:
        for name, _ in _COLUMNS:
            if name in existing:
                batch.drop_column(name)
