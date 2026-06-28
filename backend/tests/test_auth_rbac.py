"""CP4 tests: JWT auth + RBAC (10 scenarios)."""

PWD = "Password123!"


def _register(client, email, name="User"):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": PWD})


def _login(client, email):
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD})


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_valid_moe_email_registration(client):
    r = _register(client, "officer@moe.gov.my")
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "officer@moe.gov.my"
    assert "read_only" in body["roles"]   # default least-privilege role


def test_invalid_email_domain_rejected(client):
    r = _register(client, "person@gmail.com")
    assert r.status_code == 400
    assert "moe.gov.my" in r.json()["message"]


def test_login_success(client):
    _register(client, "a@moe-dl.edu.my")
    r = _login(client, "a@moe-dl.edu.my")
    assert r.status_code == 200
    assert r.json()["access_token"] and r.json()["refresh_token"]


def test_login_failure_wrong_password(client):
    _register(client, "b@moe.gov.my")
    r = client.post("/api/v1/auth/login", json={"email": "b@moe.gov.my", "password": "wrong-pass"})
    assert r.status_code == 401


def test_access_token_works(client):
    _register(client, "c@moe.gov.my")
    token = _login(client, "c@moe.gov.my").json()["access_token"]
    r = client.get("/api/v1/auth/me", headers=_auth(token))
    assert r.status_code == 200
    assert r.json()["email"] == "c@moe.gov.my"


def test_refresh_token_works(client):
    _register(client, "d@moe.gov.my")
    refresh = _login(client, "d@moe.gov.my").json()["refresh_token"]
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
    assert r.status_code == 200
    assert r.json()["access_token"]


def test_protected_route_blocks_unauthenticated(client):
    r = client.get("/api/v1/auth/me")            # no token
    assert r.status_code == 401


def test_role_protected_route_blocks_insufficient_role(client):
    _register(client, "plain@moe.gov.my")        # default read_only
    token = _login(client, "plain@moe.gov.my").json()["access_token"]
    r = client.get("/api/v1/users", headers=_auth(token))   # admin-only
    assert r.status_code == 403


def test_admin_can_list_users(client, make_admin):
    _register(client, "boss@moe.gov.my")
    make_admin("boss@moe.gov.my")
    token = _login(client, "boss@moe.gov.my").json()["access_token"]
    r = client.get("/api/v1/users", headers=_auth(token))
    assert r.status_code == 200
    assert any(u["email"] == "boss@moe.gov.my" for u in r.json())


def test_non_admin_cannot_list_users(client):
    _register(client, "reader@moe.gov.my")
    token = _login(client, "reader@moe.gov.my").json()["access_token"]
    r = client.get("/api/v1/users", headers=_auth(token))
    assert r.status_code == 403
