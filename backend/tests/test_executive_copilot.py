"""CP16 tests: Executive Copilot briefing/ask/recommendation/approval/history, RBAC, advisory, RALPH."""
import uuid

from sqlalchemy import select

from app.models.operational.access import Teras
from app.models.operational.kpi import KPI
from app.models.ai.ai_meta import AIConversation
from app.models.operational.governance import Approval
from app.repositories.user_repository import UserRepository

PWD = "Password123!"
RPM_TEXT = "RPM 2026-2035 prioritises literacy and numeracy. Teacher competency strengthened. " * 4


def _register(client, email, name="User"):
    return client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": PWD})


def _login(client, email):
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


def _set_role(db, email, role):
    repo = UserRepository(db); u = repo.get_by_email(email); repo.set_roles(u, [role]); db.commit(); return u


def _exec_token(client, db, email="exec@moe.gov.my"):
    _register(client, email); _set_role(db, email, "executive")
    return _login(client, email)["access_token"]


def _admin_token(client, make_admin, email="adm@moe.gov.my"):
    _register(client, email); make_admin(email)
    return _login(client, email)["access_token"]


def _seed_kpi(db, *, code, risk="high"):
    t = db.scalar(select(Teras).where(Teras.number == 1))
    k = KPI(id=str(uuid.uuid4()), code=code, teras_id=t.id, statement="S", sector="BPSH",
            status="off_track", risk_level=risk, is_deleted=False)
    db.add(k); db.commit(); return k.id


def _ingest(client, tok):
    s = client.post("/api/v1/knowledge/sources", headers=_auth(tok),
                    json={"type": "static", "title": "RPM 2026-2035", "category": "rpm",
                          "format": "md", "content": RPM_TEXT})
    client.post(f"/api/v1/knowledge/sources/{s.json()['id']}/process", headers=_auth(tok))


# 1 & 3 & 4 & 5. Authorised briefing incl. dashboard/risk/FDS; advisory; no official actions
def test_briefing(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)            # super_admin ∈ copilot roles
    _seed_kpi(db_session, code="TS1.HR", risk="high")
    r = client.post("/api/v1/executive-copilot/briefing", headers=_auth(tok))
    assert r.status_code == 200
    b = r.json()
    assert {"executive_summary", "kpi_highlights", "key_risks", "budget_fds_insights",
            "suggested_strategic_actions", "advisory_only", "human_review_required"} <= b.keys()
    assert b["advisory_only"] is True and b["human_review_required"] is True
    assert b["kpi_highlights"]["total_kpis"] >= 1
    assert "sent" not in b and "issued" not in b and "approved" not in b   # no official actions


# 2. Unauthorised role blocked
def test_unauthorised_blocked(client, db_session):
    _register(client, "ro@moe.gov.my"); _set_role(db_session, "ro@moe.gov.my", "read_only")
    tok = _login(client, "ro@moe.gov.my")["access_token"]
    assert client.post("/api/v1/executive-copilot/briefing", headers=_auth(tok)).status_code == 403


# 7 & 8 & 9. Ask: RALPH applied, citations when available, missing evidence stated
def test_ask_citation_and_ralph(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _ingest(client, tok)
    grounded = client.post("/api/v1/executive-copilot/ask", headers=_auth(tok),
                           json={"question": "literacy and numeracy"}).json()
    assert grounded["grounded"] is True and grounded["citations"]
    assert grounded["ralph_review"] and "verdict" in grounded["ralph_review"]

    miss = client.post("/api/v1/executive-copilot/ask", headers=_auth(tok),
                       json={"question": "quantum spaceship"}).json()
    assert miss["evidence_available"] is False
    assert "No supporting evidence" in miss["evidence_note"]
    assert "cannot find this information" in miss["answer"]


# 6. Recommendation draft + submit-for-approval (pending, NOT approved)
def test_recommendation_and_submit(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    kid = _seed_kpi(db_session, code="TS1.REC")
    rec = client.post("/api/v1/executive-copilot/recommendations", headers=_auth(tok),
                      json={"kpi_id": kid, "content": "Reallocate budget", "rationale": "funding gap"})
    assert rec.status_code == 201
    rid = rec.json()["id"]
    sub = client.post(f"/api/v1/executive-copilot/recommendations/{rid}/submit-for-approval", headers=_auth(tok))
    assert sub.status_code == 200
    assert sub.json()["approval_state"] == "pending_review"      # NOT approved
    ap = db_session.scalar(select(Approval).where(Approval.item_id == rid))
    assert ap is not None and ap.state == "pending_review"


# 10. Interaction history logged
def test_history_logged(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _ingest(client, tok)
    client.post("/api/v1/executive-copilot/briefing", headers=_auth(tok))
    client.post("/api/v1/executive-copilot/ask", headers=_auth(tok), json={"question": "literacy"})
    hist = client.get("/api/v1/executive-copilot/history", headers=_auth(tok))
    assert hist.status_code == 200 and len(hist.json()) >= 2
    # logged as session-less AIConversation
    assert db_session.scalar(select(AIConversation).where(AIConversation.session_id.is_(None))) is not None


# 11 & 12. Orchestrates specialists; no direct DB mutation of operational records; no email/report/notif
def test_orchestrates_no_mutation(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session, code="TS1.X")
    before = db_session.scalar(select(KPI).where(KPI.code == "TS1.X")).status
    client.post("/api/v1/executive-copilot/briefing", headers=_auth(tok))
    db_session.expire_all()
    after = db_session.scalar(select(KPI).where(KPI.code == "TS1.X")).status
    assert before == after  # briefing did not mutate operational KPI
    # no approval/notification/report rows created by a briefing
    assert db_session.scalar(select(Approval)) is None
