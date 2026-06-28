"""CP12 tests: skill registry, metadata, deterministic vs AI, fallback, RALPH LOOP, logging, RBAC."""
from sqlalchemy import select

from app.models.ai.ai_meta import SkillExecution
from app.repositories.user_repository import UserRepository
from app.skills import registry
from app.skills.base import Skill

PWD = "Password123!"
EXPECTED_SKILLS = {
    "kpi_analysis", "validation", "risk_scoring", "fds", "low_cost_high_impact", "obb_analysis",
    "strategic_recommendation", "rpm_alignment", "rag_retrieval", "citation_grounding",
    "report_writing", "notification_writing", "audit_logging", "dashboard_summary", "ralph_loop_review",
}


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


# 1 & 2. Registry loads all 15; each has metadata
def test_registry_loads_15_with_metadata():
    assert set(registry.REGISTRY) == EXPECTED_SKILLS
    for meta in registry.list_skills():
        assert {"name", "description", "deterministic", "uses_provider", "version"} <= meta.keys()
        assert isinstance(registry.get_skill(meta["name"]), Skill)


# 3. Deterministic skill runs without AI provider
def test_deterministic_skill_runs():
    out = registry.get_skill("risk_scoring").run({"achievement": "30%", "target": "100%"})
    assert out["risk_level"] == "high"
    kpi = registry.get_skill("kpi_analysis").run({"achievement": "100%", "target": "100%"})
    assert kpi["achievement_status"] == "achieved"


# 4 & 5. AI-assisted skill uses adapter only + safe fallback when no provider key
def test_ai_skill_fallback_without_key():
    skill = registry.get_skill("notification_writing")
    assert skill.uses_provider is True
    out = skill.run({"type": "reminder", "kpi": "TS1.KPI1"})
    # No provider key in tests → safe fallback (deterministic template), no crash.
    assert out["source"] == "fallback" and out["sent"] is False
    assert "Reminder" in out["draft"]


# 6. RALPH LOOP flags unsafe output
def test_ralph_loop_flags_unsafe():
    skill = registry.get_skill("ralph_loop_review")
    bad = skill.run({"text": "I will send the email and approve the report now.",
                     "citations": [], "advisory_only": False, "human_review_required": False})
    assert bad["passed"] is False
    assert "unsafe_direct_action" in bad["issues"]
    assert "missing_citation" in bad["issues"]
    assert "not_advisory_only" in bad["issues"]
    good = skill.run({"text": "Advisory summary.", "citations": [{"title": "RPM"}],
                      "advisory_only": True, "human_review_required": True})
    assert good["passed"] is True


# 7. Skill execution logged
def test_skill_execution_logged(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    r = client.post("/api/v1/skills/risk_scoring/execute", headers=_auth(tok),
                    json={"achievement": "30%", "target": "100%"})
    assert r.status_code == 200 and r.json()["result"]["risk_level"] == "high"
    assert db_session.scalar(select(SkillExecution).where(SkillExecution.skill_name == "risk_scoring")) is not None


# 8 & 9. API protected; unauthorised role cannot execute
def test_api_protected_and_rbac(client, db_session):
    # unauthenticated
    assert client.get("/api/v1/skills").status_code == 401
    # read_only cannot execute
    _register(client, "ro@moe.gov.my"); _set_role(db_session, "ro@moe.gov.my", "read_only")
    tok = _login(client, "ro@moe.gov.my")["access_token"]
    assert client.get("/api/v1/skills", headers=_auth(tok)).status_code == 200       # can view
    assert client.post("/api/v1/skills/risk_scoring/execute", headers=_auth(tok),
                       json={}).status_code == 403                                    # cannot execute


# 10. No skill approves/sends/deletes official output (advisory shapes only)
def test_skills_do_not_execute_official_actions():
    notif = registry.get_skill("notification_writing").run({"type": "reminder", "kpi": "K"})
    assert notif["sent"] is False
    report = registry.get_skill("report_writing").run({"period": "2026-01", "stats": {}})
    assert report["human_review_required"] is True
    # citation skill emits fixed fallback when ungrounded (never fabricates)
    cg = registry.get_skill("citation_grounding").run({"answer": None, "sources": []})
    assert cg["fallback"] is True and "cannot find this information" in cg["answer"]


# get single skill endpoint
def test_get_skill_endpoint(client, make_admin):
    tok = _admin_token(client, make_admin)
    r = client.get("/api/v1/skills/kpi_analysis", headers=_auth(tok))
    assert r.status_code == 200 and r.json()["name"] == "kpi_analysis"
    assert client.get("/api/v1/skills/nope", headers=_auth(tok)).status_code == 404
