"""CP18 tests: notification draft → submit → approve → queue (dry-run) → retry; RBAC; audit; no auto-send."""
from sqlalchemy import select

from app.models.operational.governance import Notification
from app.repositories.user_repository import UserRepository

PWD = "Password123!"


def _register(client, email, name="User"):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": PWD})


def _login(client, email):
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


def _set_role(db, email, role):
    repo = UserRepository(db); u = repo.get_by_email(email); repo.set_roles(u, [role]); db.commit(); return u


def _admin_token(client, make_admin, email="adm@moe.gov.my"):
    _register(client, email); make_admin(email)
    return _login(client, email)["access_token"]


def _exec_token(client, db, email="exec@moe.gov.my"):
    _register(client, email); _set_role(db, email, "executive")
    return _login(client, email)["access_token"]


def _draft(client, tok, recipient="pic@moe.gov.my", type_="reminder"):
    return client.post("/api/v1/notifications/draft", headers=_auth(tok),
                       json={"type": type_, "recipient": recipient, "kpi": "TS1.K1",
                             "detail": "monthly update due"})


# 1 & 2. Draft created via agent/skill
def test_draft_created(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    r = _draft(client, tok)
    assert r.status_code == 201
    b = r.json()
    assert b["status"] == "draft" and b["subject"] and b["body"]
    assert "Reminder" in b["body"] or "reminder" in b["body"].lower()


# 3. Submit creates approval
def test_submit_creates_approval(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    nid = _draft(client, tok).json()["id"]
    sub = client.post(f"/api/v1/notifications/{nid}/submit-for-review", headers=_auth(tok))
    assert sub.status_code == 200 and sub.json()["approval_state"] == "pending_review"
    assert sub.json()["notification_status"] == "pending_review"


# 4. Unapproved cannot be queued
def test_unapproved_cannot_queue(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    nid = _draft(client, tok).json()["id"]
    # still draft → queue blocked
    assert client.post(f"/api/v1/notifications/{nid}/queue", headers=_auth(tok)).status_code == 409
    # pending_review → still blocked
    client.post(f"/api/v1/notifications/{nid}/submit-for-review", headers=_auth(tok))
    assert client.post(f"/api/v1/notifications/{nid}/queue", headers=_auth(tok)).status_code == 409


# 5 & 7 & 10. Approved → queue → dry-run sent (no real email)
def test_approve_then_queue_dry_run(client, make_admin, db_session):
    gen = _admin_token(client, make_admin, "gen@moe.gov.my")
    nid = _draft(client, gen).json()["id"]
    aid = client.post(f"/api/v1/notifications/{nid}/submit-for-review", headers=_auth(gen)).json()["approval_id"]
    appr = _exec_token(client, db_session, "appr@moe.gov.my")
    client.post(f"/api/v1/approvals/{aid}/approve", headers=_auth(appr))   # different approver
    q = client.post(f"/api/v1/notifications/{nid}/queue", headers=_auth(gen))
    assert q.status_code == 200
    assert q.json()["status"] == "sent" and q.json()["mode"] == "dry_run"   # dry-run, no real SMTP


# 6. Queue supports retry count (retry applies to a failed queue item)
def test_retry_count(client, make_admin, db_session):
    from app.models.operational.governance import Notification
    gen = _admin_token(client, make_admin, "gen2@moe.gov.my")
    nid = _draft(client, gen).json()["id"]
    aid = client.post(f"/api/v1/notifications/{nid}/submit-for-review", headers=_auth(gen)).json()["approval_id"]
    appr = _exec_token(client, db_session, "appr2@moe.gov.my")
    client.post(f"/api/v1/approvals/{aid}/approve", headers=_auth(appr))
    client.post(f"/api/v1/notifications/{nid}/queue", headers=_auth(gen))
    # simulate a delivery failure to exercise the retry path
    n = db_session.get(Notification, nid); n.status = "failed"; db_session.commit()
    r = client.post(f"/api/v1/notifications/email-queue/{nid}/retry", headers=_auth(gen))
    assert r.status_code == 200 and r.json()["retry_count"] == 1 and r.json()["status"] == "sent"


# 8. Audited
def test_audited(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _draft(client, tok)
    actions = {a["action"] for a in client.get("/api/v1/audit/logs", headers=_auth(tok)).json()}
    assert "notification_draft" in actions


# 9. Role-scoped: read_only cannot draft; PIC sees only own
def test_role_scoped(client, make_admin, db_session):
    _register(client, "ro@moe.gov.my"); _set_role(db_session, "ro@moe.gov.my", "read_only")
    rtok = _login(client, "ro@moe.gov.my")["access_token"]
    assert _draft(client, rtok).status_code == 403

    admin = _admin_token(client, make_admin)
    _draft(client, admin, recipient="pic@moe.gov.my")
    _draft(client, admin, recipient="other@moe.gov.my")
    _register(client, "pic@moe.gov.my"); _set_role(db_session, "pic@moe.gov.my", "kpi_pic")
    ptok = _login(client, "pic@moe.gov.my")["access_token"]
    mine = client.get("/api/v1/notifications", headers=_auth(ptok)).json()
    assert mine and all(n["recipient"] == "pic@moe.gov.my" for n in mine)


# 11. RALPH applied (agent uses it; advisory)
def test_ralph_applied():
    from app.agents import registry
    agent = registry.get_agent("notification")
    assert "ralph_loop_review" in agent.uses_skills
    out = agent.run({"type": "reminder", "kpi": "K"})
    assert out["ralph_review"] is not None and out["sent"] is False
    assert out["human_review_required"] is True


# 12. No notification bypasses approval (no SMTP send without config)
def test_no_bypass(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    nid = _draft(client, tok).json()["id"]
    # cannot queue a draft (must be approved)
    assert client.post(f"/api/v1/notifications/{nid}/queue", headers=_auth(tok)).status_code == 409
    n = db_session.get(Notification, nid)
    assert n.status == "draft"  # not sent/queued
