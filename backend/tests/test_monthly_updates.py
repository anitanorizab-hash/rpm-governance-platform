"""CP8 tests: monthly update workflow, RBAC, duplicate, validation, analysis, risk, audit."""
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


def _set_role(db, email, role):
    repo = UserRepository(db)
    user = repo.get_by_email(email)
    repo.set_roles(user, [role])
    db.commit()
    return user


def _seed_kpi(db, *, code, pic_email=None, target="100%"):
    teras = db.scalar(select(Teras).where(Teras.number == 1))
    pic = None
    if pic_email:
        pic = PIC(id=str(uuid.uuid4()), name="Owner", email=pic_email, sector="BPSH")
        db.add(pic); db.flush()
    kpi = KPI(id=str(uuid.uuid4()), code=code, teras_id=teras.id, statement="Stmt",
              sector="BPSH", pic_id=(pic.id if pic else None), is_deleted=False)
    db.add(kpi); db.flush()
    db.add(KPITarget(id=str(uuid.uuid4()), kpi_id=kpi.id, target_value=target))
    db.commit()
    return kpi.id


def _payload(kpi_id, **kw):
    base = {"kpi_id": kpi_id, "reporting_year": 2026, "reporting_month": 1,
            "achievement_value": "100%", "finance_status": "received"}
    base.update(kw)
    return base


# 1. PIC can submit for assigned KPI
def test_pic_can_submit_assigned(client, db_session):
    _register(client, "pic@moe.gov.my"); _set_role(db_session, "pic@moe.gov.my", "kpi_pic")
    tok = _login(client, "pic@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="K.A", pic_email="pic@moe.gov.my")
    r = client.post("/api/v1/monthly-updates", headers=_auth(tok), json=_payload(kid))
    assert r.status_code == 201
    assert r.json()["achievement_status"] == "achieved"   # 100% vs 100% target


# 2. PIC cannot submit for unassigned KPI
def test_pic_cannot_submit_unassigned(client, db_session):
    _register(client, "pic2@moe.gov.my"); _set_role(db_session, "pic2@moe.gov.my", "kpi_pic")
    tok = _login(client, "pic2@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="K.B", pic_email="someone-else@moe.gov.my")
    r = client.post("/api/v1/monthly-updates", headers=_auth(tok), json=_payload(kid))
    assert r.status_code == 403


# 3 & 4. Duplicate blocked; admin override allows replacement
def test_duplicate_blocked_then_override(client, make_admin, db_session):
    _register(client, "adm@moe.gov.my"); make_admin("adm@moe.gov.my")
    tok = _login(client, "adm@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="K.C")
    assert client.post("/api/v1/monthly-updates", headers=_auth(tok), json=_payload(kid)).status_code == 201
    dup = client.post("/api/v1/monthly-updates", headers=_auth(tok), json=_payload(kid))
    assert dup.status_code == 409
    ov = client.post("/api/v1/monthly-updates?override=true", headers=_auth(tok),
                     json=_payload(kid, achievement_value="50%"))
    assert ov.status_code == 201 and ov.json()["achievement_status"] == "at_risk"


# 5. Invalid finance status rejected
def test_invalid_finance_status(client, make_admin, db_session):
    _register(client, "a5@moe.gov.my"); make_admin("a5@moe.gov.my")
    tok = _login(client, "a5@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="K.D")
    r = client.post("/api/v1/monthly-updates", headers=_auth(tok), json=_payload(kid, finance_status="bogus"))
    assert r.status_code == 422


# 6. Invalid month rejected
def test_invalid_month(client, make_admin, db_session):
    _register(client, "a6@moe.gov.my"); make_admin("a6@moe.gov.my")
    tok = _login(client, "a6@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="K.E")
    r = client.post("/api/v1/monthly-updates", headers=_auth(tok), json=_payload(kid, reporting_month=13))
    assert r.status_code == 422


# 7, 8, 9. Audited + analysis + risk
def test_audit_analysis_risk(client, make_admin, db_session):
    _register(client, "a7@moe.gov.my"); make_admin("a7@moe.gov.my")
    tok = _login(client, "a7@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="K.F")
    client.post("/api/v1/monthly-updates", headers=_auth(tok), json=_payload(kid, achievement_value="30%"))
    # analysis status persisted
    upd = db_session.scalar(select(KPIMonthlyUpdate).where(KPIMonthlyUpdate.kpi_id == kid))
    assert upd.achievement_status == "off_track"   # 30% vs 100%
    # risk assessment row created
    ra = db_session.scalar(select(RiskAssessment).where(RiskAssessment.kpi_id == kid))
    assert ra is not None and ra.risk_level == "high"
    # audited
    actions = {a["action"] for a in client.get("/api/v1/audit/logs", headers=_auth(tok)).json()}
    assert "monthly_update_create" in actions


# 10. Executive cannot update
def test_executive_cannot_update(client, db_session):
    _register(client, "exec@moe.gov.my"); _set_role(db_session, "exec@moe.gov.my", "executive")
    tok = _login(client, "exec@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="K.G")
    r = client.post("/api/v1/monthly-updates", headers=_auth(tok), json=_payload(kid))
    assert r.status_code == 403


# 11. Monthly update does not modify KPI statement/indicator/target
def test_update_does_not_modify_kpi_definition(client, make_admin, db_session):
    _register(client, "a11@moe.gov.my"); make_admin("a11@moe.gov.my")
    tok = _login(client, "a11@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="K.H")
    before = db_session.get(KPI, kid).statement
    target_before = db_session.scalar(select(KPITarget).where(KPITarget.kpi_id == kid)).target_value
    client.post("/api/v1/monthly-updates", headers=_auth(tok), json=_payload(kid))
    db_session.expire_all()
    assert db_session.get(KPI, kid).statement == before
    assert db_session.scalar(select(KPITarget).where(KPITarget.kpi_id == kid)).target_value == target_before


# 12. No monthly Excel upload endpoint exists
def test_no_monthly_excel_upload(client, make_admin, db_session):
    _register(client, "a12@moe.gov.my"); make_admin("a12@moe.gov.my")
    tok = _login(client, "a12@moe.gov.my")["access_token"]
    # No Excel-upload endpoint for monthly updates: POST is unavailable (404 not-found or 405 method-not-allowed).
    assert client.post("/api/v1/monthly-updates/upload", headers=_auth(tok)).status_code in (404, 405)
    assert client.post("/api/v1/monthly-updates/import", headers=_auth(tok)).status_code in (404, 405)


# summary endpoint
def test_summary(client, make_admin, db_session):
    _register(client, "a13@moe.gov.my"); make_admin("a13@moe.gov.my")
    tok = _login(client, "a13@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="K.I")
    client.post("/api/v1/monthly-updates", headers=_auth(tok), json=_payload(kid))
    r = client.get("/api/v1/monthly-updates/summary", headers=_auth(tok))
    assert r.status_code == 200 and r.json()["total_updates"] >= 1
    assert "achieved" in r.json()["by_status"]
