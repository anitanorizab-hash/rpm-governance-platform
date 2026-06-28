"""CP15 tests: chatbot sessions/messages, RAG citation, fallback, role scoping, RALPH, logging, no-actions."""
import uuid

from sqlalchemy import select

from app.models.operational.access import PIC, Teras
from app.models.operational.kpi import KPI
from app.models.ai.ai_meta import AIConversation
from app.repositories.user_repository import UserRepository
from app.skills import registry as skill_registry

PWD = "Password123!"
RPM_TEXT = ("RPM 2026-2035 prioritises literacy and numeracy for all pupils. "
            "Teacher competency and digital learning are strengthened. ") * 4


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


def _ingest(client, tok):
    s = client.post("/api/v1/knowledge/sources", headers=_auth(tok),
                    json={"type": "static", "title": "RPM 2026-2035", "category": "rpm",
                          "format": "md", "content": RPM_TEXT})
    client.post(f"/api/v1/knowledge/sources/{s.json()['id']}/process", headers=_auth(tok))


def _seed_kpi(db, *, code, pic_email=None, status="on_track"):
    teras = db.scalar(select(Teras).where(Teras.number == 1))
    pic = None
    if pic_email:
        pic = PIC(id=str(uuid.uuid4()), name="Owner", email=pic_email, sector="BPSH")
        db.add(pic); db.flush()
    k = KPI(id=str(uuid.uuid4()), code=code, teras_id=teras.id, statement="S", sector="BPSH",
            pic_id=(pic.id if pic else None), status=status, is_deleted=False)
    db.add(k); db.commit(); return k.id


# 1 & 2 & 3. Create session, send message, logged
def test_session_message_logged(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _ingest(client, tok)
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    r = client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                    json={"message": "literacy numeracy pupils"})
    assert r.status_code == 200
    assert db_session.scalar(select(AIConversation).where(AIConversation.session_id == sid)) is not None


# 4. RAG answer includes citation
def test_answer_with_citation(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _ingest(client, tok)
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    r = client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                    json={"message": "teacher competency digital learning"})
    b = r.json()
    assert b["grounded"] is True and b["fallback_used"] is False and b["citations"]


# 5. Missing answer → fixed fallback
def test_fallback(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _ingest(client, tok)
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    r = client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                    json={"message": "zzz quantum spaceship"})
    assert r.json()["fallback_used"] is True
    assert "cannot find this information" in r.json()["answer"]


# 6 & 7. PIC cannot access unassigned KPI data; admin can
def test_role_scoped_operational_context(client, make_admin, db_session):
    # PIC
    _register(client, "pic@moe.gov.my"); _set_role(db_session, "pic@moe.gov.my", "kpi_pic")
    ptok = _login(client, "pic@moe.gov.my")["access_token"]
    _seed_kpi(db_session, code="TS1.OWN", pic_email="pic@moe.gov.my")
    _seed_kpi(db_session, code="TS1.OTHER", pic_email="other@moe.gov.my")
    psid = client.post("/api/v1/chatbot/sessions", headers=_auth(ptok)).json()["id"]
    pr = client.post(f"/api/v1/chatbot/sessions/{psid}/messages", headers=_auth(ptok),
                     json={"message": "status of TS1.OWN and TS1.OTHER"}).json()
    codes = {c["code"] for c in pr["operational_context"]}
    assert "TS1.OWN" in codes and "TS1.OTHER" not in codes   # restricted KPI not exposed

    # Admin sees both
    atok = _admin_token(client, make_admin)
    asid = client.post("/api/v1/chatbot/sessions", headers=_auth(atok)).json()["id"]
    ar = client.post(f"/api/v1/chatbot/sessions/{asid}/messages", headers=_auth(atok),
                     json={"message": "status of TS1.OWN and TS1.OTHER"}).json()
    acodes = {c["code"] for c in ar["operational_context"]}
    assert {"TS1.OWN", "TS1.OTHER"} <= acodes


# 8 & 12. Chatbot does not execute official actions; no email/report/approval
def test_no_official_actions(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _ingest(client, tok)
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    r = client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                    json={"message": "literacy"}).json()
    assert r["human_review_required"] is False  # info-only; no approval/send/report triggered
    # response contains no execution/sent/report-issue flags
    assert "sent" not in r and "approved" not in r


# 9. RALPH LOOP review present + flags unsafe (skill-level)
def test_ralph_review(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _ingest(client, tok)
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    r = client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                    json={"message": "teacher competency"}).json()
    assert r["ralph_review"] is not None and "verdict" in r["ralph_review"]
    unsafe = skill_registry.get_skill("ralph_loop_review").run(
        {"text": "send the email and approve now", "citations": [],
         "advisory_only": False, "human_review_required": False})
    assert "unsafe_direct_action" in unsafe["issues"]


# 10. Session access control
def test_session_access_control(client, db_session):
    _register(client, "u1@moe.gov.my"); tok1 = _login(client, "u1@moe.gov.my")["access_token"]
    _register(client, "u2@moe.gov.my"); tok2 = _login(client, "u2@moe.gov.my")["access_token"]
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok1)).json()["id"]
    # u2 (not owner, not admin) cannot view u1's session
    assert client.get(f"/api/v1/chatbot/sessions/{sid}", headers=_auth(tok2)).status_code == 403
    assert client.get(f"/api/v1/chatbot/sessions/{sid}", headers=_auth(tok1)).status_code == 200


# 11. Conversation history + empty message rejected
def test_history_and_validation(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _ingest(client, tok)
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok), json={"message": "literacy"})
    hist = client.get(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok))
    assert hist.status_code == 200 and len(hist.json()) >= 1
    # empty message → 422 (pydantic min_length)
    assert client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                       json={"message": ""}).status_code == 422
