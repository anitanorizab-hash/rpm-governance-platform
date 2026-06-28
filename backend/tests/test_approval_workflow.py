"""CP9 tests: approval state machine, RBAC, own-request rule, immutability, audit, gate helper."""
from app.repositories.user_repository import UserRepository
from app.services.approval_service import ApprovalService

PWD = "Password123!"


def _register(client, email, name="User"):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": PWD})


def _login(client, email):
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


def _set_role(db, email, role):
    repo = UserRepository(db); u = repo.get_by_email(email); repo.set_roles(u, [role]); db.commit(); return u


def _user(client, db, email, role):
    _register(client, email); _set_role(db, email, role)
    return _login(client, email)["access_token"]


def _create(client, tok, submit=False, item_type="report", item_id="r1"):
    return client.post("/api/v1/approvals", headers=_auth(tok),
                       json={"item_type": item_type, "item_id": item_id, "submit": submit})


# 1 & 2. create draft → submit → pending_review
def test_create_and_submit(client, db_session):
    rtok = _user(client, db_session, "req@moe.gov.my", "jpn_admin")
    ap = _create(client, rtok).json()
    assert ap["state"] == "draft"
    sub = client.post(f"/api/v1/approvals/{ap['id']}/submit", headers=_auth(rtok)).json()
    assert sub["state"] == "pending_review"


# 3. approve by an approver (different person)
def test_approve_flow(client, db_session):
    rtok = _user(client, db_session, "req2@moe.gov.my", "jpn_admin")
    etok = _user(client, db_session, "exec2@moe.gov.my", "executive")
    ap = _create(client, rtok, submit=True).json()
    r = client.post(f"/api/v1/approvals/{ap['id']}/approve", headers=_auth(etok))
    assert r.status_code == 200 and r.json()["state"] == "approved" and r.json()["decision"] == "approve"


# 4. reject
def test_reject_flow(client, db_session):
    rtok = _user(client, db_session, "req3@moe.gov.my", "jpn_admin")
    etok = _user(client, db_session, "exec3@moe.gov.my", "executive")
    ap = _create(client, rtok, submit=True).json()
    r = client.post(f"/api/v1/approvals/{ap['id']}/reject", headers=_auth(etok),
                    json={"comment": "insufficient"})
    assert r.status_code == 200 and r.json()["state"] == "rejected"


# 5. cancel
def test_cancel_flow(client, db_session):
    rtok = _user(client, db_session, "req4@moe.gov.my", "jpn_admin")
    ap = _create(client, rtok).json()
    r = client.post(f"/api/v1/approvals/{ap['id']}/cancel", headers=_auth(rtok))
    assert r.status_code == 200 and r.json()["state"] == "cancelled"


# 6. final states immutable
def test_final_state_immutable(client, db_session):
    rtok = _user(client, db_session, "req5@moe.gov.my", "jpn_admin")
    etok = _user(client, db_session, "exec5@moe.gov.my", "executive")
    ap = _create(client, rtok, submit=True).json()
    client.post(f"/api/v1/approvals/{ap['id']}/approve", headers=_auth(etok))
    again = client.post(f"/api/v1/approvals/{ap['id']}/approve", headers=_auth(etok))
    assert again.status_code == 409
    assert client.post(f"/api/v1/approvals/{ap['id']}/reject", headers=_auth(etok)).status_code == 409


# 7. requester cannot approve own; super admin override can
def test_requester_cannot_approve_own_unless_override(client, db_session, make_admin):
    etok = _user(client, db_session, "selfexec@moe.gov.my", "executive")
    ap = _create(client, etok, submit=True).json()
    blocked = client.post(f"/api/v1/approvals/{ap['id']}/approve", headers=_auth(etok))
    assert blocked.status_code == 403

    # super admin requesting own + override
    _register(client, "sa@moe.gov.my"); make_admin("sa@moe.gov.my")
    satok = _login(client, "sa@moe.gov.my")["access_token"]
    ap2 = _create(client, satok, submit=True, item_id="r2").json()
    ok = client.post(f"/api/v1/approvals/{ap2['id']}/approve?override=true", headers=_auth(satok))
    assert ok.status_code == 200 and ok.json()["state"] == "approved"


# 8. non-approver role cannot decide
def test_non_approver_blocked(client, db_session):
    rtok = _user(client, db_session, "req8@moe.gov.my", "jpn_admin")
    ptok = _user(client, db_session, "pic8@moe.gov.my", "kpi_pic")
    ap = _create(client, rtok, submit=True).json()
    assert client.post(f"/api/v1/approvals/{ap['id']}/approve", headers=_auth(ptok)).status_code == 403


# 9. transitions audited
def test_transitions_audited(client, db_session):
    rtok = _user(client, db_session, "req9@moe.gov.my", "jpn_admin")
    etok = _user(client, db_session, "exec9@moe.gov.my", "executive")
    ap = _create(client, rtok, submit=True).json()
    client.post(f"/api/v1/approvals/{ap['id']}/approve", headers=_auth(etok))
    actions = {a["action"] for a in client.get("/api/v1/audit/logs", headers=_auth(etok)).json()}
    assert "approval_approve" in actions


# 10. no AI agent / unauthenticated cannot decide
def test_unauthenticated_cannot_decide(client):
    assert client.post("/api/v1/approvals/anything/approve").status_code == 401


# 11. is_approved gate helper (service-level, reusable)
def test_is_approved_gate(client, db_session):
    rtok = _user(client, db_session, "req11@moe.gov.my", "jpn_admin")
    etok = _user(client, db_session, "exec11@moe.gov.my", "executive")
    ap = _create(client, rtok, submit=True, item_type="notification", item_id="n1").json()
    svc = ApprovalService(db_session)
    assert svc.is_approved("notification", "n1") is False
    client.post(f"/api/v1/approvals/{ap['id']}/approve", headers=_auth(etok))
    db_session.expire_all()
    assert svc.is_approved("notification", "n1") is True
