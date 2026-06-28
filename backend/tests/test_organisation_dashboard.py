"""V1.1 Phase 2 tests: organisation listing + org-scoped dashboard + PPD comparison."""
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


def _admin_token(client, make_admin, email="orgadm@moe.gov.my"):
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


# 1. /organisations lists the seeded hierarchy and filters by type
def test_list_organisations(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    r = client.get("/api/v1/organisations", headers=_auth(tok))
    assert r.status_code == 200
    codes = {o["code"] for o in r.json()}
    assert {"JPN", "PPD-KINTA-UTARA", "PPD-MANJUNG"} <= codes
    r2 = client.get("/api/v1/organisations?type=PPD", headers=_auth(tok))
    assert {o["type"] for o in r2.json()} == {"PPD"}
    assert len(r2.json()) >= 2


# 2. organisation_id scopes the dashboard overview (additive, backward-compatible)
def test_overview_organisation_filter(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kinta = _org(db_session, "PPD-KINTA-UTARA")
    jpn = _org(db_session, "JPN")
    _seed_kpi(db_session, code="ORG.K1", organisation_id=kinta.id)
    _seed_kpi(db_session, code="ORG.K2", organisation_id=kinta.id)
    _seed_kpi(db_session, code="ORG.J1", organisation_id=jpn.id)

    all_ov = client.get("/api/v1/dashboard/overview", headers=_auth(tok)).json()
    assert all_ov["total_kpis"] == 3                     # unfiltered = backward-compatible

    kinta_ov = client.get(f"/api/v1/dashboard/overview?organisation_id={kinta.id}",
                          headers=_auth(tok)).json()
    assert kinta_ov["total_kpis"] == 2                   # scoped to the PPD


# 3. PPD comparison ranks PPDs and includes empty PPDs with zeroed metrics
def test_ppd_comparison(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kinta = _org(db_session, "PPD-KINTA-UTARA")
    _seed_kpi(db_session, code="CMP.K1", organisation_id=kinta.id)

    r = client.get("/api/v1/dashboard/ppd-comparison", headers=_auth(tok))
    assert r.status_code == 200
    body = r.json()
    assert body["ppd_count"] >= 2
    by_code = {p["code"]: p for p in body["ppds"]}
    assert by_code["PPD-KINTA-UTARA"]["total_kpis"] == 1
    assert by_code["PPD-MANJUNG"]["total_kpis"] == 0     # empty PPD still represented
    assert all("rank" in p for p in body["ppds"])
    assert body["top_performer"] is not None
