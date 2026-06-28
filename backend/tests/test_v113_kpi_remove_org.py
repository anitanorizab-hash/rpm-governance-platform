"""V1.1.3 tests: KPI soft-remove (reason + org audit, not hard delete) and org level/name in responses."""
import uuid

from sqlalchemy import select

from app.models.operational.access import Teras
from app.models.operational.kpi import KPI
from app.models.operational.organisation import Organisation

PWD = "Password123!"


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


def _admin_token(client, make_admin, email="v113@moe.gov.my"):
    client.post("/api/v1/auth/register", json={"email": email, "name": "Adm", "password": PWD})
    make_admin(email)
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()["access_token"]


def _seed_kpi(db, code, org_code="PPD-KINTA-UTARA"):
    teras = db.scalar(select(Teras).where(Teras.number == 1))
    org = db.scalar(select(Organisation).where(Organisation.code == org_code))
    k = KPI(id=str(uuid.uuid4()), code=code, teras_id=teras.id, statement="Sample KPI",
            organisation_id=org.id, is_deleted=False)
    db.add(k); db.commit()
    return k.id


# 1. KPI list/detail expose Level + Organisation
def test_kpi_list_and_detail_include_organisation(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, "ORG.LIST.1")
    item = next(k for k in client.get("/api/v1/kpis", headers=_auth(tok)).json() if k["id"] == kid)
    assert item["organisation_type"] == "PPD" and item["organisation_name"] == "PPD Kinta Utara"
    detail = client.get(f"/api/v1/kpis/{kid}", headers=_auth(tok)).json()
    assert detail["organisation_type"] == "PPD" and detail["organisation_name"] == "PPD Kinta Utara"


# 2. /kpis organisation_id filter
def test_kpi_organisation_filter(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kinta = db_session.scalar(select(Organisation).where(Organisation.code == "PPD-KINTA-UTARA"))
    manjung = db_session.scalar(select(Organisation).where(Organisation.code == "PPD-MANJUNG"))
    _seed_kpi(db_session, "ORG.K.A", "PPD-KINTA-UTARA")
    _seed_kpi(db_session, "ORG.M.A", "PPD-MANJUNG")
    res = client.get(f"/api/v1/kpis?organisation_id={kinta.id}", headers=_auth(tok)).json()
    assert all(k["organisation_id"] == kinta.id for k in res)
    assert any(k["code"] == "ORG.K.A" for k in res) and not any(k["code"] == "ORG.M.A" for k in res)


# 3. Soft remove: reason + org captured in audit; excluded from active; retained (not hard-deleted)
def test_kpi_soft_remove(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, "REMOVE.ME")
    r = client.delete(f"/api/v1/kpis/{kid}?reason=Officially agreed for removal at Aug review",
                      headers=_auth(tok))
    assert r.status_code == 200 and r.json()["soft_delete"] is True
    # excluded from active list
    active = client.get("/api/v1/kpis", headers=_auth(tok)).json()
    assert not any(k["id"] == kid for k in active)
    # visible with include_removed
    removed = client.get("/api/v1/kpis?include_removed=true", headers=_auth(tok)).json()
    assert any(k["id"] == kid for k in removed)
    # NOT hard-deleted — row still present, flagged
    db_session.expire_all()
    row = db_session.get(KPI, kid)
    assert row is not None and row.is_deleted is True and row.deleted_at is not None
    # audit captured reason + org context
    audit = client.get("/api/v1/audit/logs?action=kpi_remove", headers=_auth(tok)).json()
    entry = next(a for a in audit if a.get("entity_id") == kid)
    assert "Officially agreed" in (entry.get("reason") or "")


# 4. Only admins may remove
def test_kpi_remove_rbac(client, make_admin, db_session):
    kid = _seed_kpi(db_session, "RBAC.KPI")
    client.post("/api/v1/auth/register", json={"email": "pic113@moe.gov.my", "name": "P", "password": PWD})
    from app.repositories.user_repository import UserRepository
    repo = UserRepository(db_session); u = repo.get_by_email("pic113@moe.gov.my")
    repo.set_roles(u, ["kpi_pic"]); db_session.commit()
    tok = client.post("/api/v1/auth/login", json={"email": "pic113@moe.gov.my", "password": PWD}).json()["access_token"]
    assert client.delete(f"/api/v1/kpis/{kid}?reason=x", headers=_auth(tok)).status_code == 403
