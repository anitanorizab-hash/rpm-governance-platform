"""CP17 tests: report draft → submit → approve/reject status sync → archive; RBAC; audit; no email."""
import uuid

from sqlalchemy import select

from app.models.operational.access import Teras
from app.models.operational.kpi import KPI
from app.models.operational.governance import Approval, Report
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


def _seed_kpi(db, code="TS1.R", risk="high"):
    t = db.scalar(select(Teras).where(Teras.number == 1))
    db.add(KPI(id=str(uuid.uuid4()), code=code, teras_id=t.id, statement="S", sector="BPSH",
               status="off_track", risk_level=risk, is_deleted=False)); db.commit()


def _generate(client, tok, period="2026-01"):
    return client.post("/api/v1/reports/generate", headers=_auth(tok), json={"period": period})


# 1 & 2. Generate draft with sections
def test_generate_draft(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _seed_kpi(db_session)
    r = _generate(client, tok)
    assert r.status_code == 201
    b = r.json()
    assert b["status"] == "draft"
    c = b["content"]
    assert {"kpi_achievement_overview", "risk_summary", "budget_fds_summary",
            "missing_information_summary"} <= c.keys()
    assert c["advisory_only"] is True and c["human_review_required"] is True


# 3 & 4 & 6. Submit → approve (by other) → status approved → archive
def test_submit_approve_archive(client, make_admin, db_session):
    gen_tok = _admin_token(client, make_admin, "gen@moe.gov.my")
    rid = _generate(client, gen_tok).json()["id"]
    sub = client.post(f"/api/v1/reports/{rid}/submit-for-review", headers=_auth(gen_tok))
    assert sub.status_code == 200 and sub.json()["report_status"] == "pending_review"
    approval_id = sub.json()["approval_id"]

    # a different executive approves
    appr_tok = _exec_token(client, db_session, "appr@moe.gov.my")
    ap = client.post(f"/api/v1/approvals/{approval_id}/approve", headers=_auth(appr_tok))
    assert ap.status_code == 200 and ap.json()["state"] == "approved"

    # report status syncs to approved
    got = client.get(f"/api/v1/reports/{rid}", headers=_auth(gen_tok)).json()
    assert got["status"] == "approved"

    arch = client.post(f"/api/v1/reports/{rid}/archive", headers=_auth(gen_tok))
    assert arch.status_code == 200 and arch.json()["status"] == "archived"


# 5. Rejected report stores reason
def test_reject_stores_reason(client, make_admin, db_session):
    gen_tok = _admin_token(client, make_admin, "gen2@moe.gov.my")
    rid = _generate(client, gen_tok).json()["id"]
    approval_id = client.post(f"/api/v1/reports/{rid}/submit-for-review", headers=_auth(gen_tok)).json()["approval_id"]
    appr_tok = _exec_token(client, db_session, "appr2@moe.gov.my")
    client.post(f"/api/v1/approvals/{approval_id}/reject", headers=_auth(appr_tok),
                json={"comment": "needs more detail"})
    got = client.get(f"/api/v1/reports/{rid}", headers=_auth(gen_tok)).json()
    assert got["status"] == "rejected" and got["reject_reason"] == "needs more detail"


# 7. Generation audited
def test_generation_audited(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _generate(client, tok)
    actions = {a["action"] for a in client.get("/api/v1/audit/logs", headers=_auth(tok)).json()}
    assert "report_generate" in actions


# 8 & 9. No email / no auto-publish
def test_no_email_no_autopublish(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    b = _generate(client, tok).json()
    assert b["status"] == "draft"                       # not published/approved automatically
    assert b["content"].get("issued") is None or b["content"].get("issued") is False
    # no notification rows created by report generation
    from app.models.operational.governance import Notification
    assert db_session.scalar(select(Notification)) is None


# 10. Role-scoped: read_only cannot generate
def test_role_scoped(client, db_session):
    _register(client, "ro@moe.gov.my"); _set_role(db_session, "ro@moe.gov.my", "read_only")
    tok = _login(client, "ro@moe.gov.my")["access_token"]
    assert _generate(client, tok).status_code == 403


# 11 & 12. Report Generation Agent uses approved skills + RALPH applied
def test_agent_skills_and_ralph(client, make_admin, db_session):
    from app.agents import registry
    agent = registry.get_agent("report_generation")
    assert set(agent.uses_skills) == {"report_writing", "dashboard_summary",
                                      "citation_grounding", "ralph_loop_review"}
    out = agent.run({"period": "2026-01", "stats": {}, "overview": {"total_kpis": 0, "risk": {}, "by_teras": {}}})
    assert out["ralph_review"] is not None and "verdict" in out["ralph_review"]
    assert out["issued"] is False and out["human_review_required"] is True


# requester cannot approve own report (CP9 rule)
def test_requester_cannot_approve_own(client, make_admin, db_session):
    gen_tok = _admin_token(client, make_admin, "self@moe.gov.my")  # super_admin
    rid = _generate(client, gen_tok).json()["id"]
    approval_id = client.post(f"/api/v1/reports/{rid}/submit-for-review", headers=_auth(gen_tok)).json()["approval_id"]
    # same user approves own → blocked (403) unless override
    assert client.post(f"/api/v1/approvals/{approval_id}/approve", headers=_auth(gen_tok)).status_code == 403
    ok = client.post(f"/api/v1/approvals/{approval_id}/approve?override=true", headers=_auth(gen_tok))
    assert ok.status_code == 200
