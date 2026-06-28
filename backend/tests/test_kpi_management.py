"""CP7 tests: KPI management, completeness, amendment window, soft delete, audit, RBAC."""
import uuid

import pytest
from sqlalchemy import select

from app.models.operational.access import PIC, Teras
from app.models.operational.kpi import KPI, KPIIndicator, KPITarget
from app.services import amendment_service

PWD = "Password123!"


def _register(client, email, name="User"):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": PWD})


def _login(client, email):
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


def _admin_token(client, make_admin, email="adm@moe.gov.my"):
    _register(client, email); make_admin(email)
    return _login(client, email)["access_token"]


def _seed_kpi(db, *, code, complete=True):
    """Create a KPI directly in the DB for management tests."""
    teras = db.scalar(select(Teras).where(Teras.number == 1))
    pic = None
    if complete:
        pic = PIC(id=str(uuid.uuid4()), name="Officer", email=f"{code}@moe.gov.my", sector="BPSH")
        db.add(pic); db.flush()
    kpi = KPI(id=str(uuid.uuid4()), code=code, teras_id=teras.id,
              statement=("Stmt" if complete else None), sector=("BPSH" if complete else None),
              pic_id=(pic.id if pic else None), is_deleted=False)
    db.add(kpi); db.flush()
    if complete:
        db.add(KPIIndicator(id=str(uuid.uuid4()), kpi_id=kpi.id, indicator_text="ind"))
        db.add(KPITarget(id=str(uuid.uuid4()), kpi_id=kpi.id, target_value="100%"))
    db.commit()
    return kpi.id


# 1. List KPIs with JWT
def test_list_requires_jwt_and_returns(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="TS1.S1.P1.KPI1")
    assert client.get("/api/v1/kpis").status_code == 401
    r = client.get("/api/v1/kpis", headers=_auth(tok))
    assert r.status_code == 200 and len(r.json()) >= 1


# 2. Filter by Teras
def test_filter_by_teras(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="TS1.A")
    r = client.get("/api/v1/kpis?teras=1", headers=_auth(tok))
    assert r.status_code == 200 and all(k["teras_number"] == 1 for k in r.json())
    assert client.get("/api/v1/kpis?teras=5", headers=_auth(tok)).json() == []


# 3. Detail view
def test_kpi_detail(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="TS1.DET")
    r = client.get(f"/api/v1/kpis/{kid}", headers=_auth(tok))
    assert r.status_code == 200
    body = r.json()
    assert body["code"] == "TS1.DET" and body["indicators"] == ["ind"] and body["is_complete"] is True


# 4. Completeness detects missing fields
def test_completeness_detects_missing(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="TS1.INC", complete=False)
    r = client.get(f"/api/v1/kpis/{kid}/completeness", headers=_auth(tok))
    assert r.status_code == 200
    miss = r.json()["missing_fields"]
    assert "indicator" in miss and "target" in miss and "pic_email" in miss
    assert r.json()["is_complete"] is False


# 5. Completeness summary
def test_completeness_summary(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="TS1.OK")
    _seed_kpi(db_session, code="TS1.BAD", complete=False)
    r = client.get("/api/v1/kpis/completeness/summary", headers=_auth(tok))
    assert r.status_code == 200
    body = r.json()
    assert body["total_kpis"] >= 2 and body["incomplete"] >= 1
    assert "indicator" in body["missing_field_counts"]


# 6. PIC assignment
def test_pic_assignment(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="TS1.PIC", complete=False)
    r = client.post(f"/api/v1/kpis/{kid}/assign-pic", headers=_auth(tok),
                    json={"name": "New PIC", "email": "newpic@moe.gov.my", "sector": "BPK"})
    assert r.status_code == 200 and r.json()["pic_email"] == "newpic@moe.gov.my"


# 7 & 8 & 9. Amendment window allow (Jul/Oct), block (else), super-admin override
def test_amendment_window(client, make_admin, db_session, monkeypatch):
    tok = _admin_token(client, make_admin)   # admin is super_admin via make_admin
    kid = _seed_kpi(db_session, code="TS1.AMD")

    monkeypatch.setattr(amendment_service, "_current_month", lambda: 7)   # July → allowed
    r = client.patch(f"/api/v1/kpis/{kid}", headers=_auth(tok), json={"statement": "Updated in July"})
    assert r.status_code == 200 and r.json()["statement"] == "Updated in July"

    monkeypatch.setattr(amendment_service, "_current_month", lambda: 3)   # March → blocked
    r2 = client.patch(f"/api/v1/kpis/{kid}", headers=_auth(tok), json={"statement": "March edit"})
    assert r2.status_code == 409

    # super admin override outside window
    r3 = client.patch(f"/api/v1/kpis/{kid}?override=true", headers=_auth(tok), json={"statement": "Override edit"})
    assert r3.status_code == 200 and r3.json()["statement"] == "Override edit"


# 10. Soft delete
def test_soft_delete(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="TS1.DEL")
    r = client.delete(f"/api/v1/kpis/{kid}", headers=_auth(tok))
    assert r.status_code == 200
    # no longer listed / retrievable, but row still exists (soft)
    assert client.get(f"/api/v1/kpis/{kid}", headers=_auth(tok)).status_code == 404
    assert db_session.get(KPI, kid).is_deleted is True


# 11. KPI changes audited
def test_kpi_changes_audited(client, make_admin, db_session, monkeypatch):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="TS1.AUD")
    monkeypatch.setattr(amendment_service, "_current_month", lambda: 10)
    client.patch(f"/api/v1/kpis/{kid}", headers=_auth(tok), json={"statement": "audited change"})
    actions = {a["action"] for a in client.get("/api/v1/audit/logs", headers=_auth(tok)).json()}
    assert "kpi_update" in actions


# 12. Non-authorised user blocked from managing
def test_non_authorised_blocked(client, db_session):
    _register(client, "reader@moe.gov.my")            # default read_only
    tok = _login(client, "reader@moe.gov.my")["access_token"]
    kid = _seed_kpi(db_session, code="TS1.RBAC")
    assert client.patch(f"/api/v1/kpis/{kid}", headers=_auth(tok), json={"status": "on-track"}).status_code == 403
    assert client.delete(f"/api/v1/kpis/{kid}", headers=_auth(tok)).status_code == 403
