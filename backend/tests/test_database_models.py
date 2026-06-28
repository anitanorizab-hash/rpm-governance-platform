"""CP3 tests: connection, table creation, relationships, seed data, plane separation."""
import uuid

import pytest
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import Session

from app.db.base import Base
import app.models  # noqa: F401  (populate metadata)
from app.db.seed import seed_reference_data
from app.models.operational.access import BudgetStatus, Role, Teras, PIC, Department
from app.models.operational.kpi import KPI, KPIMonthlyUpdate
from app.models.operational.governance import AmendmentWindow, AuditLog


@pytest.fixture()
def session():
    """In-memory SQLite with full schema + seed (isolated per test)."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, future=True)
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        seed_reference_data(s)
        yield s


def test_database_connection_and_tables(session):
    insp = inspect(session.get_bind())
    tables = set(insp.get_table_names())
    # representative tables from each group must exist
    for t in ("role", "teras", "kpi", "financial_allocation", "audit_log",
              "knowledge_source", "agent_execution"):
        assert t in tables, f"missing table {t}"
    # 38 entities total
    assert len(tables) >= 38


def test_reference_seed_data(session):
    assert session.scalar(select(Role).where(Role.name == "kpi_pic")) is not None
    assert len(list(session.scalars(select(Teras)))) == 7
    assert len(list(session.scalars(select(BudgetStatus)))) == 6
    windows = list(session.scalars(select(AmendmentWindow)))
    assert {w.month for w in windows} == {7, 10}


def test_core_relationships(session):
    teras = session.scalar(select(Teras).where(Teras.number == 1))
    dept = Department(id=str(uuid.uuid4()), name="BPSH")
    pic = PIC(id=str(uuid.uuid4()), name="Officer A", email="a@moe.gov.my", sector="SPb")
    session.add_all([dept, pic]); session.flush()
    kpi = KPI(id=str(uuid.uuid4()), code="TS1.S1.P1.KPI2", teras_id=teras.id,
              statement="Sample", pic_id=pic.id)
    session.add(kpi); session.flush()
    upd = KPIMonthlyUpdate(id=str(uuid.uuid4()), kpi_id=kpi.id, period="2026-01", achievement="50%")
    session.add(upd); session.commit()
    # relationship traversal works
    assert kpi.teras.number == 1
    assert kpi.pic.email == "a@moe.gov.my"
    assert session.scalar(select(KPIMonthlyUpdate).where(KPIMonthlyUpdate.kpi_id == kpi.id)).achievement == "50%"


def test_audit_log_is_append_only_shape(session):
    """AuditLog has created_at but NOT updated_at (append-only by design)."""
    cols = {c.name for c in AuditLog.__table__.columns}
    assert "created_at" in cols
    assert "updated_at" not in cols


def test_plane_separation(session):
    """Operational, knowledge and AI models live in separate modules/tables."""
    assert KPI.__module__.startswith("app.models.operational")
    from app.models.knowledge.knowledge import KnowledgeSource
    from app.models.ai.ai_meta import AgentExecution
    assert KnowledgeSource.__module__.startswith("app.models.knowledge")
    assert AgentExecution.__module__.startswith("app.models.ai")
    # distinct tables
    assert KPI.__tablename__ != KnowledgeSource.__tablename__ != AgentExecution.__tablename__
