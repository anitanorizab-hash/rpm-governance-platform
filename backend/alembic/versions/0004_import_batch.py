"""Create import_batch table (CP6). Guarded no-op on fresh DBs (0001 create_all already made it).

Revision ID: 0004_import_batch
Revises: 0003_audit_context
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "0004_import_batch"
down_revision = "0003_audit_context"
branch_labels = None
depends_on = None


def _has_table(bind, name: str) -> bool:
    return name in sa.inspect(bind).get_table_names()


def upgrade() -> None:
    bind = op.get_bind()
    if _has_table(bind, "import_batch"):
        return
    op.create_table(
        "import_batch",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("filename", sa.String(length=512)),
        sa.Column("file_hash", sa.String(length=64), index=True),
        sa.Column("plan_type", sa.String(length=16)),
        sa.Column("rows_total", sa.Integer()),
        sa.Column("rows_imported", sa.Integer()),
        sa.Column("warnings_count", sa.Integer()),
        sa.Column("status", sa.String(length=16)),
        sa.Column("warnings", sa.Text()),
        sa.Column("imported_by", sa.String(length=36), sa.ForeignKey("user.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    bind = op.get_bind()
    if _has_table(bind, "import_batch"):
        op.drop_table("import_batch")
