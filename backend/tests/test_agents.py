"""CP13 tests: agent registry, metadata, skill use, orchestrator, fallback, logging, copilot, RBAC."""
from sqlalchemy import select

from app.agents import registry
from app.agents.base import Agent
from app.agents.orchestrator import AgentOrchestrator
from app.models.ai.ai_meta import AgentExecution
from app.repositories.user_repository import UserRepository

PWD = "Password123!"
EXPECTED_AGENTS = {
    "kpi_analysis", "validation", "financial_decision_support", "risk_assessment",
    "strategic_recommendation", "knowledge_alignment", "kpi_chatbot",
    "report_generation", "notification", "audit_trail", "executive_copilot",
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


# 1 & 2 & 3. Registry loads 11; metadata; agents declare skills
def test_registry_11_with_metadata_and_skills():
    assert set(registry.REGISTRY) == EXPECTED_AGENTS
    for meta in registry.list_agents():
        assert {"name", "description", "uses_skills", "human_review_required", "version"} <= meta.keys()
        assert isinstance(registry.get_agent(meta["name"]), Agent)
        if meta["name"] != "executive_copilot":
            assert len(meta["uses_skills"]) >= 1


# 4. Orchestrator executes one agent
def test_orchestrator_single():
    orch = AgentOrchestrator()
    res = orch.run_agent("kpi_analysis", {"achievement": "100%", "target": "100%"})
    assert res["status"] == "ok"
    assert res["output"]["analysis"]["achievement_status"] == "achieved"
    assert res["output"]["advisory_only"] is True


# 5. Orchestrator executes a sequence (passes context)
def test_orchestrator_sequence():
    orch = AgentOrchestrator()
    res = orch.run_sequence(["kpi_analysis", "risk_assessment"],
                            {"achievement": "30%", "target": "100%"})
    assert res["status"] == "completed" and len(res["steps"]) == 2
    assert res["steps"][1]["output"]["risk"]["risk_level"] == "high"


# 6. Failed agent returns safe fallback (unknown agent / raising agent)
def test_failed_agent_safe_fallback(monkeypatch):
    orch = AgentOrchestrator()
    res = orch.run_agent("does_not_exist", {})
    assert res["status"] == "error" and res["fallback"] is True

    # a raising agent → caught safely
    monkeypatch.setattr(registry.get_agent("kpi_analysis"), "run",
                        lambda ctx: (_ for _ in ()).throw(RuntimeError("boom")))
    res2 = orch.run_agent("kpi_analysis", {})
    assert res2["status"] == "error" and res2["fallback"] is True and res2["human_review_required"] is True


# 7. Agent execution logged
def test_agent_execution_logged(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    r = client.post("/api/v1/agents/risk_assessment/execute", headers=_auth(tok),
                    json={"achievement": "30%", "target": "100%"})
    assert r.status_code == 200 and r.json()["output"]["risk"]["risk_level"] == "high"
    assert db_session.scalar(select(AgentExecution).where(AgentExecution.agent_name == "risk_assessment")) is not None


# 8. Executive Copilot orchestrates specialists (not replaces)
def test_executive_copilot_orchestrates():
    res = registry.get_agent("executive_copilot").run(
        {"achievement": "30%", "target": "100%", "finance_status": "insufficient",
         "overview": {"total_kpis": 5, "risk": {"high": 2}, "missing_information": 3, "by_teras": {1: 5}}}
    )
    sub = res["specialist_outputs"]
    assert {"kpi_analysis", "risk_assessment", "financial_decision_support", "knowledge_alignment"} <= sub.keys()
    assert res["human_review_required"] is True
    assert "Executive insight" in res["insight"]


# 9. Chatbot agent uses placeholder RAG safely (fixed fallback)
def test_chatbot_placeholder_safe():
    res = registry.get_agent("kpi_chatbot").run({"query": "What is KPI X?"})
    assert res["retrieval_mode"] == "placeholder"
    assert res["fallback"] is True
    assert "cannot find this information" in res["answer"]


# 10 & 11. API protected; unauthorised role cannot execute
def test_api_protected_and_rbac(client, db_session):
    assert client.get("/api/v1/agents").status_code == 401
    _register(client, "ro@moe.gov.my"); _set_role(db_session, "ro@moe.gov.my", "read_only")
    tok = _login(client, "ro@moe.gov.my")["access_token"]
    assert client.get("/api/v1/agents", headers=_auth(tok)).status_code == 200
    assert client.post("/api/v1/agents/kpi_analysis/execute", headers=_auth(tok),
                       json={}).status_code == 403


# 12. No agent approves/sends/deletes/amends official output
def test_agents_no_official_actions():
    notif = registry.get_agent("notification").run({"type": "reminder", "kpi": "K"})
    assert notif["sent"] is False and notif["human_review_required"] is True
    rep = registry.get_agent("report_generation").run({"period": "2026-01", "stats": {}})
    assert rep["issued"] is False and rep["human_review_required"] is True
    fds = registry.get_agent("financial_decision_support").run(
        {"achievement": "30%", "target": "100%", "finance_status": "insufficient"})
    assert fds["advisory_only"] is True and fds["human_review_required"] is True
