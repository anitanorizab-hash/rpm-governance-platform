"""CP11 tests: FDS deterministic analysis, finance-risk mapping, OBB, LCHI, recommendation,
advisory-only, approval integration, audit, role scoping, no-AI."""
import uuid

from sqlalchemy import select

from app.models.operational.access import Teras
from app.models.operational.finance import FinancialAllocation, StrategicRecommendation
from app.models.operational.kpi import KPI, KPITarget, KPIMonthlyUpdate
from app.repositories.user_repository import UserRepository
from app.services.fds_service import FDSService

PWD = "Password123!"


def _register(client, email, name="User"):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": PWD})


def _login(client, email):
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


def _set_role(db, email, role):
    repo = UserRepository(db); u = repo.get_by_email(email); repo.set_roles(u, [role]); db.commit(); return u


def _admin_token(client, make_admin, email="adm@moe.gov.my"):
    _register(client, email); make_admin(email)
    return _login(client, email)["access_token"]


def _seed_kpi(db, *, code, target="100%", achievement="30%", finance="insufficient", cost=60000.0):
    teras = db.scalar(select(Teras).where(Teras.number == 1))
    kpi = KPI(id=str(uuid.uuid4()), code=code, teras_id=teras.id, statement="Stmt",
              keberhasilan="Improve outcome", sector="BPSH", is_deleted=False)
    db.add(kpi); db.flush()
    db.add(KPITarget(id=str(uuid.uuid4()), kpi_id=kpi.id, target_value=target))
    db.add(KPIMonthlyUpdate(id=str(uuid.uuid4()), kpi_id=kpi.id, period="2026-01",
                            reporting_year=2026, reporting_month=1,
                            achievement_value=achievement, finance_status=finance))
    if cost:
        db.add(FinancialAllocation(id=str(uuid.uuid4()), kpi_id=kpi.id, object_code="OS29000",
                                   amount=cost, expenditure=cost * 0.5))
    db.commit()
    return kpi.id


# 1. Analysis works
def test_analysis_works(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="F1")
    r = client.get(f"/api/v1/fds/kpis/{kid}/analysis", headers=_auth(tok))
    assert r.status_code == 200
    b = r.json()
    assert b["advisory_only"] is True
    assert {"budget_intelligence", "low_cost_high_impact", "obb_analysis", "strategic_recommendation"} <= b.keys()


# 2. Six finance statuses map to correct risk
def test_finance_risk_mapping(db_session):
    svc = FDSService(db_session)
    expected = {"received": "low", "not_required": "low", "will_be_received": "medium",
                "pending": "medium", "insufficient": "high", "not_received": "high"}
    for status, risk in expected.items():
        assert svc.budget_intelligence(status)["financial_risk"] == risk
    # funding gap detection
    assert svc.budget_intelligence("pending")["funding_gap"] is True
    assert svc.budget_intelligence("received")["funding_gap"] is False


# 3 & 4. OBB + LCHI quadrant
def test_obb_and_lchi(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="F2", achievement="30%", cost=60000.0)  # high cost, low impact
    b = client.get(f"/api/v1/fds/kpis/{kid}/analysis", headers=_auth(tok)).json()
    assert b["low_cost_high_impact"]["quadrant"] == "Avoid / Redesign"
    assert b["obb_analysis"]["value_for_money"] == "low"
    assert b["obb_analysis"]["outcome_risk"] == "high"


# 5 & 6. Strategic recommendation draft + advisory-only
def test_strategic_recommendation_advisory(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="F3")
    rec = client.get(f"/api/v1/fds/kpis/{kid}/analysis", headers=_auth(tok)).json()["strategic_recommendation"]
    assert rec["recommended_action"] and rec["priority"] in (1, 2, 3)
    assert rec["human_review_required"] is True


# 7 & 8. generate persists + submit-for-approval routes to approval (not approved) + audited
def test_generate_submit_for_approval(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="F4")
    gen = client.post(f"/api/v1/fds/kpis/{kid}/generate", headers=_auth(tok))
    assert gen.status_code == 201
    rec_id = gen.json()["recommendation_id"]
    assert rec_id

    sub = client.post(f"/api/v1/fds/recommendations/{rec_id}/submit-for-approval", headers=_auth(tok))
    assert sub.status_code == 200
    body = sub.json()
    assert body["approval_state"] == "pending_review"      # NOT approved
    assert body["recommendation_status"] == "pending_approval"
    # recommendation persisted, still a draft-type record (not executed)
    rec = db_session.get(StrategicRecommendation, rec_id)
    assert rec is not None
    # audited
    actions = {a["action"] for a in client.get("/api/v1/audit/logs", headers=_auth(tok)).json()}
    assert "fds_generate" in actions and "fds_submit_for_approval" in actions


# 9. Role-scoped: read_only cannot generate
def test_role_scoped_generate(client, db_session):
    _register(client, "ro@moe.gov.my"); _set_role(db_session, "ro@moe.gov.my", "read_only")
    tok = _login(client, "ro@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="F5")
    # read_only may VIEW analysis...
    assert client.get(f"/api/v1/fds/kpis/{kid}/analysis", headers=_auth(tok)).status_code == 200
    # ...but cannot GENERATE
    assert client.post(f"/api/v1/fds/kpis/{kid}/generate", headers=_auth(tok)).status_code == 403


# 10. No AI provider called
def test_no_ai_provider_called(client, make_admin, db_session, monkeypatch):
    import app.providers.provider_factory as pf
    monkeypatch.setattr(pf, "get_llm_provider", lambda: (_ for _ in ()).throw(AssertionError("no AI in FDS")))
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="F6")
    assert client.get(f"/api/v1/fds/kpis/{kid}/analysis", headers=_auth(tok)).status_code == 200
    assert client.post(f"/api/v1/fds/kpis/{kid}/generate", headers=_auth(tok)).status_code == 201
    assert client.get("/api/v1/fds/summary", headers=_auth(tok)).status_code == 200
