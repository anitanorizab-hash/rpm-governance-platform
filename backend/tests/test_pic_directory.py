"""V1.1.1 PIC Directory tests: CRUD, soft delete, KPI assignment, search, bulk import/export, RBAC."""
import io
import uuid

import openpyxl
from sqlalchemy import select

from app.models.operational.access import Teras
from app.models.operational.kpi import KPI
from app.models.operational.organisation import Organisation

PWD = "Password123!"


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


def _admin_token(client, make_admin, email="picadm@moe.gov.my"):
    client.post("/api/v1/auth/register", json={"email": email, "name": "Adm", "password": PWD})
    make_admin(email)
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()["access_token"]


def _seed_kpi(db, code="PIC.K1"):
    teras = db.scalar(select(Teras).where(Teras.number == 1))
    org = db.scalar(select(Organisation).where(Organisation.code == "PPD-KINTA-UTARA"))
    k = KPI(id=str(uuid.uuid4()), code=code, teras_id=teras.id, statement="S",
            organisation_id=org.id, is_deleted=False)
    db.add(k); db.commit()
    return k.id


# 1. Create + list
def test_create_and_list_pic(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    org = db_session.scalar(select(Organisation).where(Organisation.code == "PPD-KINTA-UTARA"))
    r = client.post("/api/v1/pics", headers=_auth(tok), json={
        "name": "Pn. Aisyah", "email": "aisyah@moe.gov.my", "organisation_id": org.id,
        "department": "SPS", "active": True})
    assert r.status_code == 201 and r.json()["email"] == "aisyah@moe.gov.my"
    lst = client.get("/api/v1/pics", headers=_auth(tok)).json()
    assert any(p["name"] == "Pn. Aisyah" for p in lst)


# 2. RBAC: non-admin cannot manage PICs
def test_pic_admin_only(client):
    client.post("/api/v1/auth/register", json={"email": "p2@moe.gov.my", "name": "P", "password": PWD})
    tok = client.post("/api/v1/auth/login", json={"email": "p2@moe.gov.my", "password": PWD}).json()["access_token"]
    assert client.get("/api/v1/pics", headers=_auth(tok)).status_code == 403
    assert client.post("/api/v1/pics", headers=_auth(tok), json={"name": "X"}).status_code == 403


# 3. Assign KPIs → KPI gets the PIC, and the KPI detail exposes the PIC email (automation uses it)
def test_assign_kpis_feeds_automation_email(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session)
    pic = client.post("/api/v1/pics", headers=_auth(tok),
                      json={"name": "En. Salleh", "email": "salleh@moe.gov.my"}).json()
    r = client.post(f"/api/v1/pics/{pic['id']}/assign-kpis", headers=_auth(tok), json={"kpi_ids": [kid]})
    assert r.json()["assigned"] == 1
    detail = client.get(f"/api/v1/kpis/{kid}", headers=_auth(tok)).json()
    assert detail["pic_email"] == "salleh@moe.gov.my"          # automation will use this
    picdet = client.get(f"/api/v1/pics/{pic['id']}", headers=_auth(tok)).json()
    assert picdet["assigned_kpi_count"] == 1


# 4. Edit + soft delete + search/filter
def test_edit_softdelete_search(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    pid = client.post("/api/v1/pics", headers=_auth(tok),
                      json={"name": "Cik Mariam", "email": "mariam@moe.gov.my", "active": True}).json()["id"]
    client.patch(f"/api/v1/pics/{pid}", headers=_auth(tok), json={"email": "mariam.updated@moe.gov.my", "active": False})
    got = client.get(f"/api/v1/pics/{pid}", headers=_auth(tok)).json()
    assert got["email"] == "mariam.updated@moe.gov.my" and got["active"] is False
    # search
    found = client.get("/api/v1/pics?search=mariam", headers=_auth(tok)).json()
    assert any(p["id"] == pid for p in found)
    # inactive filter
    inactive = client.get("/api/v1/pics?status=inactive", headers=_auth(tok)).json()
    assert any(p["id"] == pid for p in inactive)
    # soft delete → gone from default list
    client.delete(f"/api/v1/pics/{pid}", headers=_auth(tok))
    assert not any(p["id"] == pid for p in client.get("/api/v1/pics", headers=_auth(tok)).json())


# 5. Bulk export + import (Excel)
def test_bulk_export_and_import(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    client.post("/api/v1/pics", headers=_auth(tok), json={"name": "Export Me", "email": "exp@moe.gov.my"})
    exp = client.get("/api/v1/pics/export", headers=_auth(tok))
    assert exp.status_code == 200 and exp.headers["content-type"].startswith(
        "application/vnd.openxmlformats")
    # build an import workbook
    wb = openpyxl.Workbook(); ws = wb.active
    ws.append(["Name", "Email", "Organisation", "Department", "Status"])
    ws.append(["Imported PIC", "imported@moe.gov.my", "PPD-MANJUNG", "SPM", "Active"])
    buf = io.BytesIO(); wb.save(buf)
    r = client.post("/api/v1/pics/import", headers=_auth(tok),
                    files={"file": ("pics.xlsx", buf.getvalue())})
    assert r.status_code == 200 and r.json()["created"] == 1
    assert any(p["email"] == "imported@moe.gov.my" for p in client.get("/api/v1/pics", headers=_auth(tok)).json())
