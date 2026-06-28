"""V1.1 Phase 3 tests: organisation passthrough for report/copilot + org-aware chatbot context."""
import uuid

from sqlalchemy import select

from app.models.operational.access import Teras
from app.models.operational.kpi import KPI
from app.models.operational.organisation import Organisation

PWD = "Password123!"


def _register(client, email, name="User"):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": PWD})


def _login(client, email):
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


def _admin_token(client, make_admin, email="p3adm@moe.gov.my"):
    _register(client, email); make_admin(email)
    return _login(client, email)["access_token"]


def _org(db, code):
    return db.scalar(select(Organisation).where(Organisation.code == code))


def _seed_kpi(db, *, code, organisation_id, teras_number=1):
    teras = db.scalar(select(Teras).where(Teras.number == teras_number))
    k = KPI(id=str(uuid.uuid4()), code=code, teras_id=teras.id, statement="S",
            organisation_id=organisation_id, is_deleted=False)
    db.add(k); db.commit()
    return k.id


# 1. Report generation passes organisation_id through and records it
def test_report_generate_organisation_passthrough(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kinta = _org(db_session, "PPD-KINTA-UTARA")
    _seed_kpi(db_session, code="RPT.K1", organisation_id=kinta.id)
    r = client.post(f"/api/v1/reports/generate?organisation_id={kinta.id}", headers=_auth(tok),
                    json={"period": "2026-06", "type": "monthly"})
    assert r.status_code == 201
    assert r.json()["content"]["organisation_id"] == kinta.id


# 2. Executive Copilot briefing scopes its KPI highlights to the organisation
def test_copilot_briefing_organisation_scope(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kinta = _org(db_session, "PPD-KINTA-UTARA")
    jpn = _org(db_session, "JPN")
    _seed_kpi(db_session, code="COP.K1", organisation_id=kinta.id)
    _seed_kpi(db_session, code="COP.K2", organisation_id=kinta.id)
    _seed_kpi(db_session, code="COP.J1", organisation_id=jpn.id)
    r = client.post(f"/api/v1/executive-copilot/briefing?organisation_id={kinta.id}", headers=_auth(tok))
    assert r.status_code == 200
    assert r.json()["kpi_highlights"]["total_kpis"] == 2     # scoped to the PPD


# 3. Chatbot scopes operational context to a referenced PPD
def test_chatbot_org_scoped(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kinta = _org(db_session, "PPD-KINTA-UTARA")
    _seed_kpi(db_session, code="CB.K1", organisation_id=kinta.id)
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    r = client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                    json={"message": "show me the performance for Kinta Utara"})
    b = r.json()
    assert b["operational_summary"] is not None
    assert "Kinta" in b["operational_summary"]["scope"]


# 4. Chatbot supplies PPD comparison context for comparison questions
def test_chatbot_ppd_comparison_context(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kinta = _org(db_session, "PPD-KINTA-UTARA")
    _seed_kpi(db_session, code="CB.C1", organisation_id=kinta.id)
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    r = client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                    json={"message": "compare PPD performance across districts"})
    b = r.json()
    assert b["operational_summary"] is not None
    comp = b["operational_summary"].get("ppd_comparison")
    assert comp is not None
    codes = {p["name"] for p in comp["ppds"]}
    assert "PPD Kinta Utara" in codes and "PPD Manjung" in codes
    assert b["grounded"] is True
