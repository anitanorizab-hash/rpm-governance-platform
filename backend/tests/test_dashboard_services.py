"""CP10 tests: dashboard aggregation by Teras 1–7, role scoping, executive stub, no-AI."""
import uuid

from sqlalchemy import select

from app.models.operational.access import PIC, Teras
from app.models.operational.kpi import KPI, KPITarget, KPIMonthlyUpdate, RiskAssessment
from app.repositories.user_repository import UserRepository

PWD = "Password123!"


def _register(client, email, name="User"):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": PWD})


def _login(client, email):
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


def _set_role(db, email, role, scope=None):
    repo = UserRepository(db); u = repo.get_by_email(email); repo.set_roles(u, [role])
    if scope is not None:
        u.scope = scope
    db.commit(); return u


def _admin_token(client, make_admin, email="adm@moe.gov.my"):
    _register(client, email); make_admin(email)
    return _login(client, email)["access_token"]


def _seed_kpi(db, *, code, teras_n=1, sector="BPSH", pic_email=None,
              status=None, risk=None, finance=None, with_update=False):
    teras = db.scalar(select(Teras).where(Teras.number == teras_n))
    pic = None
    if pic_email:
        pic = PIC(id=str(uuid.uuid4()), name="Owner", email=pic_email, sector=sector)
        db.add(pic); db.flush()
    kpi = KPI(id=str(uuid.uuid4()), code=code, teras_id=teras.id, statement="Stmt",
              sector=sector, pic_id=(pic.id if pic else None), is_deleted=False,
              status=status, risk_level=risk)
    db.add(kpi); db.flush()
    db.add(KPITarget(id=str(uuid.uuid4()), kpi_id=kpi.id, target_value="100%"))
    if with_update:
        db.add(KPIMonthlyUpdate(id=str(uuid.uuid4()), kpi_id=kpi.id, period="2026-01",
                                reporting_year=2026, reporting_month=1, achievement_status=status,
                                finance_status=finance))
    db.commit()
    return kpi.id


# 1. Overview
def test_overview(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="K1", teras_n=1, status="achieved", risk="low", finance="received", with_update=True)
    _seed_kpi(db_session, code="K2", teras_n=2, status="off_track", risk="high", finance="pending", with_update=True)
    r = client.get("/api/v1/dashboard/overview", headers=_auth(tok))
    assert r.status_code == 200
    b = r.json()
    assert b["total_kpis"] == 2 and b["by_teras"]["1"] == 1 and b["by_teras"]["2"] == 1
    assert b["risk"].get("high") == 1


# 2. Teras summary returns Teras 1–7
def test_teras_summary_all_seven(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="K3", teras_n=3, with_update=True, status="on_track")
    r = client.get("/api/v1/dashboard/teras-summary", headers=_auth(tok))
    assert r.status_code == 200
    data = r.json()
    assert [t["teras_number"] for t in data] == [1, 2, 3, 4, 5, 6, 7]
    assert next(t for t in data if t["teras_number"] == 3)["kpi_count"] == 1


# 3. Risk summary
def test_risk_summary(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="K4", teras_n=1, risk="high", with_update=True)
    r = client.get("/api/v1/dashboard/risk-summary", headers=_auth(tok))
    assert r.status_code == 200 and r.json()["overall"].get("high") == 1


# 4. Budget summary
def test_budget_summary(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="K5", teras_n=1, finance="insufficient", with_update=True)
    r = client.get("/api/v1/dashboard/budget-summary", headers=_auth(tok))
    assert r.status_code == 200 and r.json()["overall"].get("insufficient") == 1


# 5. Submission summary
def test_submission_summary(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="K6", teras_n=1, with_update=True)
    _seed_kpi(db_session, code="K7", teras_n=1, with_update=False)
    r = client.get("/api/v1/dashboard/submission-summary?year=2026&month=1", headers=_auth(tok))
    assert r.status_code == 200
    assert r.json()["overall"]["submitted"] == 1 and r.json()["overall"]["not_submitted"] == 1


# 6. High-risk list
def test_high_risk_kpis(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="K8", teras_n=1, risk="high", with_update=True)
    _seed_kpi(db_session, code="K9", teras_n=1, risk="low", with_update=True)
    r = client.get("/api/v1/dashboard/high-risk-kpis", headers=_auth(tok))
    assert r.status_code == 200
    codes = {x["code"] for x in r.json()}
    assert "K8" in codes and "K9" not in codes


# 7. KPI mapping
def test_kpi_mapping(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="K10", teras_n=2, pic_email="p@moe.gov.my",
              status="on_track", risk="medium", finance="pending", with_update=True)
    r = client.get("/api/v1/dashboard/kpi-mapping", headers=_auth(tok))
    assert r.status_code == 200
    row = next(x for x in r.json() if x["code"] == "K10")
    assert row["teras_number"] == 2 and row["risk"] == "medium" and row["finance_status"] == "pending"


# 8. Role scoping: sector_admin sees only own sector
def test_role_scoped_sector_admin(client, db_session):
    _register(client, "sec@moe.gov.my"); _set_role(db_session, "sec@moe.gov.my", "sector_admin", scope="BPSH")
    tok = _login(client, "sec@moe.gov.my")["access_token"]
    _seed_kpi(db_session, code="MINE", teras_n=1, sector="BPSH", with_update=True)
    _seed_kpi(db_session, code="OTHER", teras_n=1, sector="BPK", with_update=True)
    r = client.get("/api/v1/dashboard/kpi-mapping", headers=_auth(tok))
    codes = {x["code"] for x in r.json()}
    assert "MINE" in codes and "OTHER" not in codes


# 9. Executive summary stub (deterministic)
def test_executive_summary_stub(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="K11", teras_n=1, risk="high", with_update=True)
    r = client.get("/api/v1/dashboard/executive-summary", headers=_auth(tok))
    assert r.status_code == 200
    b = r.json()
    assert b["generated_by"] == "deterministic"
    assert "KPI" in b["text"] and "highlights" in b


# 10. No AI provider is called (dashboards work even if provider raises)
def test_no_ai_provider_called(client, make_admin, db_session, monkeypatch):
    import app.providers.provider_factory as pf

    def _boom():
        raise AssertionError("LLM provider must NOT be called by dashboard services")
    monkeypatch.setattr(pf, "get_llm_provider", _boom)
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="K12", teras_n=1, with_update=True)
    for path in ("overview", "teras-summary", "executive-summary", "kpi-mapping"):
        assert client.get(f"/api/v1/dashboard/{path}", headers=_auth(tok)).status_code == 200
