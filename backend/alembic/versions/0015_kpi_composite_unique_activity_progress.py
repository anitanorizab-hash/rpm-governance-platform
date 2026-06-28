"""V1.1.1: KPI code unique per organisation + Activity progress fields. Guarded.

- Drop global unique(kpi.code); add composite unique(organisation_id, code).
- Add activity.status and activity.remarks (nullable).

Revision ID: 0015_kpi_org_unique_activity
Revises: 0014_import_batch_organisation
Create Date: 2026-06-28
"""
from alembic import op
import sqlalchemy as sa

revision = "0015_kpi_org_unique_activity"
down_revision = "0014_import_batch_organisation"
branch_labels = None
depends_on = None


def _cols(bind, table):
    return {c["name"] for c in sa.inspect(bind).get_columns(table)}


def _uniques(bind, table):
    return {u["name"] for u in sa.inspect(bind).get_unique_constraints(table)}


def upgrade() -> None:
    bind = op.get_bind()

    # 1) KPI: global unique(code) -> composite unique(organisation_id, code)
    uniques = _uniques(bind, "kpi")
    with op.batch_alter_table("kpi") as batch:
        if "uq_kpi_code" in uniques:
            batch.drop_constraint("uq_kpi_code", type_="unique")
        if "uq_kpi_organisation_id_code" not in uniques:
            batch.create_unique_constraint("uq_kpi_organisation_id_code", ["organisation_id", "code"])

    # 2) Activity progress fields
    act = _cols(bind, "activity")
    with op.batch_alter_table("activity") as batch:
        if "status" not in act:
            batch.add_column(sa.Column("status", sa.String(length=64), nullable=True))
        if "remarks" not in act:
            batch.add_column(sa.Column("remarks", sa.Text(), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    act = _cols(bind, "activity")
    with op.batch_alter_table("activity") as batch:
        for c in ("remarks", "status"):
            if c in act:
                batch.drop_column(c)
    uniques = _uniques(bind, "kpi")
    with op.batch_alter_table("kpi") as batch:
        if "uq_kpi_organisation_id_code" in uniques:
            batch.drop_constraint("uq_kpi_organisation_id_code", type_="unique")
        if "uq_kpi_code" not in uniques:
            batch.create_unique_constraint("uq_kpi_code", ["code"])
