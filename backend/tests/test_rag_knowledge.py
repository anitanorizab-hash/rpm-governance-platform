"""CP14 tests: knowledge sources, processing, chunking, keyword fallback, citations, fallback,
live-link validation, RBAC, plane isolation, skill/agent RAG integration."""
from sqlalchemy import func, select

from app.models.operational.kpi import KPI
from app.models.knowledge.knowledge import Chunk, KnowledgeSource
from app.rag import chunker
from app.repositories.user_repository import UserRepository
from app.skills import registry as skill_registry
from app.agents import registry as agent_registry

PWD = "Password123!"
RPM_TEXT = ("RPM 2026-2035 prioritises literacy and numeracy for all pupils. "
            "Schools must strengthen teacher competency and digital learning. ") * 5


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


def _create_and_process(client, tok, content=RPM_TEXT, fmt="md", title="RPM 2026-2035"):
    s = client.post("/api/v1/knowledge/sources", headers=_auth(tok),
                    json={"type": "static", "title": title, "category": "rpm",
                          "format": fmt, "content": content})
    sid = s.json()["id"]
    proc = client.post(f"/api/v1/knowledge/sources/{sid}/process", headers=_auth(tok))
    return sid, s, proc


# 1. Create knowledge source
def test_create_source(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    r = client.post("/api/v1/knowledge/sources", headers=_auth(tok),
                    json={"type": "static", "title": "Guideline", "format": "txt", "content": "hello"})
    assert r.status_code == 201 and r.json()["status"] == "active"


# 2 & 3 & 5. Process TXT/MD; chunking; embedding unavailable does not fail
def test_process_and_chunking(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _, _, proc = _create_and_process(client, tok)
    body = proc.json()
    assert body["chunks"] >= 1
    assert body["embedded"] is False          # no sentence-transformers in tests → keyword fallback
    assert body["mode"] == "keyword"
    # chunker unit
    assert len(chunker.chunk_text("x" * 2000)) > 1


# 4 & 6. Keyword fallback + citations
def test_query_keyword_with_citation(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _create_and_process(client, tok)
    r = client.post("/api/v1/knowledge/query", headers=_auth(tok),
                    json={"query": "literacy numeracy pupils"})
    assert r.status_code == 200
    b = r.json()
    assert b["grounded"] is True and b["fallback"] is False and b["mode"] == "keyword"
    assert b["citations"] and b["citations"][0]["title"] == "RPM 2026-2035"


# 7. Missing answer → fixed fallback
def test_query_fallback(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _create_and_process(client, tok)
    r = client.post("/api/v1/knowledge/query", headers=_auth(tok),
                    json={"query": "zzzz quantum spaceship"})
    assert r.json()["fallback"] is True
    assert "cannot find this information" in r.json()["answer"]


# 8. Live link requires validation (excluded from retrieval until validated)
def test_live_link_validation(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    reg = client.post("/api/v1/knowledge/live-links", headers=_auth(tok),
                      json={"title": "Official", "url": "https://moe.gov.my/x"})
    assert reg.status_code == 201 and reg.json()["status"] == "pending_validation"
    src = db_session.get(KnowledgeSource, reg.json()["source_id"])
    assert src.status == "pending_validation"
    val = client.post(f"/api/v1/knowledge/live-links/{reg.json()['link_id']}/validate", headers=_auth(tok))
    assert val.status_code == 200 and val.json()["status"] == "active"


# 9. Non-admin cannot upload/process
def test_non_admin_cannot_upload(client, db_session):
    _register(client, "ro@moe.gov.my"); _set_role(db_session, "ro@moe.gov.my", "read_only")
    tok = _login(client, "ro@moe.gov.my")["access_token"]
    r = client.post("/api/v1/knowledge/sources", headers=_auth(tok),
                    json={"type": "static", "title": "x", "format": "txt", "content": "y"})
    assert r.status_code == 403


# 10. Knowledge query does not modify operational data
def test_query_no_operational_change(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _create_and_process(client, tok)
    before = db_session.scalar(select(func.count()).select_from(KPI))
    client.post("/api/v1/knowledge/query", headers=_auth(tok), json={"query": "literacy"})
    after = db_session.scalar(select(func.count()).select_from(KPI))
    assert before == after  # no KPI created/changed by a knowledge query


# 11. RAG Retrieval Skill calls rag_service
def test_rag_skill_calls_service(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _create_and_process(client, tok)
    out = skill_registry.get_skill("rag_retrieval").run({"query": "teacher competency", "db": db_session})
    assert out["mode"] == "keyword" and len(out["results"]) >= 1
    # without db → placeholder
    assert skill_registry.get_skill("rag_retrieval").run({"query": "x"})["mode"] == "placeholder"


# 12. Chatbot agent uses real RAG retrieval (via API; db injected) + safe fallback without corpus
def test_chatbot_agent_real_rag(client, make_admin, db_session):
    tok = _admin_token(client, make_admin)
    _create_and_process(client, tok)
    r = client.post("/api/v1/agents/kpi_chatbot/execute", headers=_auth(tok),
                    json={"query": "literacy numeracy"})
    out = r.json()["output"]
    assert out["retrieval_mode"] == "keyword"
    assert out["fallback"] is False and out["citations"]
    # direct agent run without db → safe fallback
    direct = agent_registry.get_agent("kpi_chatbot").run({"query": "literacy"})
    assert direct["fallback"] is True and "cannot find this information" in direct["answer"]
