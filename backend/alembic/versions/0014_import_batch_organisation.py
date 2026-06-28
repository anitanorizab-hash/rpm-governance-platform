"""Add import_batch.organisation_id FK to organisation (V1.1). Nullable. Guarded.

Revision ID: 0014_import_batch_organisation
Revises: 0013_kpi_add_organisation_id
Create Date: 2026-06-28
"""
from alembic import op
import sqlalchemy as sa

revision = "0014_import_batch_organisation"
down_revision = "0013_kpi_add_organisation_id"
branch_labels = None
depends_on = None


def _cols(bind, table):
    return {c["name"] for c in sa.inspect(bind).get_columns(table)}


def upgrade() -> None:
    bind = op.get_bind()
    if "organisation_id" in _cols(bind, "import_batch"):
        return
    with op.batch_alter_table("import_batch") as batch:
        batch.add_column(
            sa.Column(
                "organisation_id", sa.String(length=36),
                sa.ForeignKey("organisation.id", name="fk_import_batch_organisation_id_organisation"),
                nullable=True,
            )
        )


def downgrade() -> None:
    bind = op.get_bind()
    if "organisation_id" not in _cols(bind, "import_batch"):
        return
    with op.batch_alter_table("import_batch") as batch:
        batch.drop_column("organisation_id")
