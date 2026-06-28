"""V1.1.2 tests: RPM RAG chatbot, enriched intervention recommendation, audit trail."""
from app.db.knowledge_seed import seed_rpm_knowledge
from app.services import strategic_recommendation_service as strat

PWD = "Password123!"


def _auth(t):
    return {"Authorization": f"Bearer {t}"}


def _admin_token(client, make_admin, email="v112@moe.gov.my"):
    client.post("/api/v1/auth/register", json={"email": email, "name": "Adm", "password": PWD})
    make_admin(email)
    return client.post("/api/v1/auth/login", json={"email": email, "password": PWD}).json()["access_token"]


# Issue 2 — enriched intervention recommendation
def test_recommendation_is_enriched():
    rec = strat.build(finance_risk="high", funding_gap=True, quadrant="Priority Action", vfm="high",
                      kpi_status="off_track", activity="Bengkel coaching GBK",
                      milestone="2 bengkel selesai", remarks="belum mula")
    for key in ("recommended_action", "reason", "related_activity", "related_milestone",
                "urgency", "expected_impact", "low_cost_option", "human_review_required"):
        assert key in rec
    assert rec["related_activity"] == "Bengkel coaching GBK"
    assert rec["urgency"] == "High" and rec["human_review_required"] is True


# Issue 1 — RPM policy question answered + cited
def test_rpm_chatbot_answers_infrastructure(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    seed_rpm_knowledge(db_session)                     # register + process RPM reference
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    r = client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                    json={"message": "Which Teras focuses on infrastructure?"})
    b = r.json()
    assert b["grounded"] is True and b["fallback_used"] is False
    assert "infrastructure" in b["answer"].lower() or "teras 4" in b["answer"].lower()
    assert b["citations"]                              # cited


# Issue 1 — fixed fallback still applies when ungrounded
def test_rpm_chatbot_fallback_when_unknown(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    seed_rpm_knowledge(db_session)
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    r = client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                    json={"message": "zzz quantum spaceship colony"}).json()
    assert r["fallback_used"] is True
    assert "cannot find this information" in r["answer"]


# Issue 3 — chatbot interaction is audited
def test_chatbot_interaction_audited(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    sid = client.post("/api/v1/chatbot/sessions", headers=_auth(tok)).json()["id"]
    client.post(f"/api/v1/chatbot/sessions/{sid}/messages", headers=_auth(tok),
                json={"message": "literacy"})
    audit = client.get("/api/v1/audit/logs", headers=_auth(tok)).json()
    assert any(a["action"] == "chatbot_message" for a in audit)


# Issue 3 — audit trail is append-only (no update/delete endpoints)
def test_audit_is_append_only(client, make_admin):
    tok = _admin_token(client, make_admin)
    logs = client.get("/api/v1/audit/logs", headers=_auth(tok))
    assert logs.status_code == 200
    # no mutation endpoints exist → method not allowed
    assert client.patch("/api/v1/audit/logs/anything", headers=_auth(tok), json={}).status_code == 405
    assert client.delete("/api/v1/audit/logs/anything", headers=_auth(tok)).status_code == 405
