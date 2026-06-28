"""CP5 tests: audit service + append-only + role-scoped read + masking + auth-event coverage."""

from app.core.audit import mask_payload
from app.repositories.audit_repository import AuditRepository
from app.services.audit_service import AuditService

PWD = "Password123!"


def _register(client, email, name="User"):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": PWD})


def _login(client, email):
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


# 1. Create audit log through AuditService
def test_audit_service_record(db_session):
    svc = AuditService(db_session)
    entry = svc.record(entity_type="kpi", action="test_action", entity_id="kpi-1", actor_id=None)
    assert entry.id and entry.action == "test_action"
    assert AuditRepository(db_session).get(entry.id) is not None


# 2. Append-only behaviour: repository exposes no update/delete
def test_audit_append_only_no_mutators():
    repo_attrs = dir(AuditRepository)
    assert "update" not in repo_attrs
    assert "delete" not in repo_attrs
    assert "remove" not in repo_attrs


# 3. Audit list requires authentication
def test_audit_requires_auth(client):
    assert client.get("/api/v1/audit/logs").status_code == 401


# 4 & 5. Admin sees all; normal user sees only their own logs
def test_admin_sees_all_normal_user_scoped(client, make_admin):
    _register(client, "admin@moe.gov.my"); make_admin("admin@moe.gov.my")
    _register(client, "user1@moe.gov.my")
    admin_tok = _login(client, "admin@moe.gov.my")["access_token"]
    user_tok = _login(client, "user1@moe.gov.my")["access_token"]

    user_id = client.get("/api/v1/users/me", headers=_auth(user_tok)).json()["id"]

    admin_logs = client.get("/api/v1/audit/logs", headers=_auth(admin_tok)).json()
    user_logs = client.get("/api/v1/audit/logs", headers=_auth(user_tok)).json()

    # admin sees logs from more than one actor
    assert len({l["actor_id"] for l in admin_logs}) >= 2
    # normal user sees ONLY their own actions
    assert user_logs and all(l["actor_id"] == user_id for l in user_logs)


# 6. Normal user can view own logs
def test_user_sees_own_logs(client):
    _register(client, "own@moe.gov.my")
    tok = _login(client, "own@moe.gov.my")["access_token"]
    logs = client.get("/api/v1/audit/logs", headers=_auth(tok)).json()
    assert any(l["action"] in ("register", "login") for l in logs)


# 7. Sensitive fields are masked
def test_sensitive_masking():
    masked = mask_payload({"password": "secret123", "name": "Ali", "access_token": "abc"})
    assert masked["password"] == "***"
    assert masked["access_token"] == "***"
    assert masked["name"] == "Ali"


# 8. Audit logs cannot be updated/deleted through the API (no such routes → 405)
def test_audit_no_update_delete_api(client, make_admin):
    _register(client, "boss@moe.gov.my"); make_admin("boss@moe.gov.my")
    tok = _login(client, "boss@moe.gov.my")["access_token"]
    some_id = "00000000-0000-0000-0000-000000000000"
    assert client.delete(f"/api/v1/audit/logs/{some_id}", headers=_auth(tok)).status_code == 405
    assert client.put(f"/api/v1/audit/logs/{some_id}", headers=_auth(tok), json={}).status_code == 405


# 9. Auth events are audited (login success + failure + register)
def test_auth_events_audited(client, make_admin):
    _register(client, "ev@moe.gov.my"); make_admin("ev@moe.gov.my")
    _login(client, "ev@moe.gov.my")
    # a failed login
    client.post("/api/v1/auth/login", json={"email": "ev@moe.gov.my", "password": "wrong"})
    tok = _login(client, "ev@moe.gov.my")["access_token"]
    actions = {l["action"] for l in client.get("/api/v1/audit/logs", headers=_auth(tok)).json()}
    assert "register" in actions
    assert "login" in actions
    assert "login_failed" in actions
