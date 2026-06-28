# DEVELOPMENT DEPENDENCY MAP (A8)
### Agentic AI Strategic Governance Platform — RPM 2026–2035
#### Final build-ordering artifact before coding

| Field | Value |
|-------|-------|
| Document | A8 — Development Dependency Map |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Companion | `./CLAUDE.md` (§16 build sequence), `12_IMPLEMENTATION_PREP.md` (prompts) |
| Baselines (frozen/approved) | HMW/BRD/RTM/TRD v1.0; A1–A6; A7/CLAUDE.md v1.0 |
| Boundary | Dependency/ordering only — **not a requirements doc; no code.** |

> Legend: **API** = A6 group; **DB** = A5 entities; **Skills/Agents** = A3/A2. "Test required before
> continuing" must pass before the next dependent item starts (build-test-stop, TR-006).

---

## 1. Dependency Map (per item)

| # | Item | Depends on | Produces | Folder | API group | DB entities | Agents/Skills | Test before continuing |
|---|------|-----------|----------|--------|-----------|-------------|---------------|------------------------|
| 1 | **Backend foundation** | — | FastAPI app, `/api/v1`, error envelope, CORS | `backend/app`, `api/v1` | G18 Health | — | — | App starts; `/health` 200 |
| 2 | **Config & environment** | 1 | config.md profiles, `.env` loader, Provider Adapter iface | `core/config`, `providers` | G17 (later) | (config store) | Provider Adapter | Config loads per profile; adapter selects (mock) |
| 3 | **Database models** | 1 | SQLAlchemy models (3 groups) | `models`, `db` | — | All (A5) | — | Models import; SQLite create OK |
| 4 | **Alembic migrations** | 3 | migration scripts; schema | `alembic` | — | All | — | Migrate up/down on SQLite + PostgreSQL |
| 5 | **Authentication & RBAC** | 2,3,4 | JWT, RBAC dependency, login | `services/auth`, `core/security`, `api/.../auth,users` | G1, G2 | User, Role | — | Login/refresh; domain reject; RBAC allow/deny |
| 6 | **Audit trail** | 3,4 | append-only audit + hook | `audit`, `services/audit`, `api/.../audit` | G16 | Audit_Log | S13 audit_logging | Append immutable; scoped read |
| 7 | **Initial Excel import** | 3,4,5,6 | import pipeline; master records | `services/import`, `skills` | G4 | KPI,Teras,Strategy,Prakarsa,Activity,PIC,Financial_Allocation | Data Integration, S2 | Sample workbook imports; warnings; import-once |
| 8 | **KPI management** | 5,6,7 | KPI CRUD, indicator/target, PIC, completeness | `services/kpi`, `api/.../kpis` | G3 | KPI,Indicator,Target,PIC,Amendment_Window,KPI_Amendment | Validation, S2 | CRUD; completeness; **amendment-window 409** |
| 9 | **Monthly KPI updates** | 5,6,8 | in-system monthly entry | `services/update,validation`, `api/.../updates` | G5 | KPI_Monthly_Update,Evidence,Budget_Status | S1,S3 (post-save) | Save; six-value status; own-scope; no Excel |
| 10 | **Approval & HITL** | 5,6 | draft→approve/reject state machine | `services/workflow`, `api/.../approvals` | G15 | Approval (+targets) | — | Approve/reject; role; no-action-without-approval |
| 11 | **Dashboard (Teras 1–7)** | 8,9 | per-Teras roll-ups, mapping, high-risk | `services/dashboard`, `api/.../dashboard` | G6 | KPI,Monthly_Update,Risk,Financial_Allocation,Alignment_Score | S1,S14 | Aggregations; role scope; 7 Teras present |
| 12 | **Financial Decision Support** | 9,(13,14,15) | budget status, LCHI, OBB, recommendations | `services/finance`, `api/.../fds` | G7 | Financial_Allocation,Budget_Status,OBB,LCHI,Strategic_Recommendation | FDS Agent, S4,S5,S6,S7 | Status/funding-gap/LCHI/OBB; advisory only |
| 13 | **AI provider adapter** | 2 | chat()/embedding() across providers | `providers` | (internal) | Provider_Usage,AI_Cost_Log | — | chat() Groq; embedding() ST/OpenAI; switch by config |
| 14 | **Skills layer** | 3,6,13 | S1–S15 registry | `skills` | G9 (internal) | Skill_Execution | S1–S15 | Each skill unit-tested (deterministic cores) |
| 15 | **Agent layer** | 6,10,13,14 | orchestrator + 11 agents | `agents` | G8 | Agent_Execution,AI_Recommendation | all agents | Orchestration; advisory; HITL routing; logged |
| 16 | **RAG & knowledge base** | 3,6,13 | ingestion, retrieval, citation, vector | `rag`, `knowledge`, `api/.../knowledge` | G10 | Knowledge_Source,Document,Live_Link,Chunk,Embedding_Metadata,Citation,Refresh_History | S9,S10, link_fetch | Ingest; keyword→vector; cite; admin-validate links |
| 17 | **Chatbot** | 14,15,16 | grounded cited Q&A | `services/chatbot`, `agents/chatbot`, `api/.../chatbot` | G11 | Chat_Session,AI_Conversation,Citation | Chatbot Agent,S9,S10,S15 | Grounding order; role-scope; cite; fallback string |
| 18 | **Executive Copilot** | 11,12,15,16 | synthesised executive insight | `services/copilot`, `agents/executive_copilot`, `api/.../copilot` | G12 | AI_Conversation,AI_Recommendation,Citation | Copilot,S1/3/4/8/9/10/14/15 | Synthesis from KPI/Risk/FDS/RAG; advisory; cited |
| 19 | **Reports** | 10,11,12,15 | generate→approve→archive | `reports`, `services/report`, `api/.../reports` | G13 | Report,Approval,Audit_Log | Report Agent,S11,S1/3/4/10/15 | Draft; submit; **issue only after approval** |
| 20 | **Notifications & email queue** | 9,10,15 | reminders/alerts/escalation; queue+retry | `notifications`, `services/notification`, `api/.../notifications` | G14 | Notification,Approval | Notification Agent,S12 | Draft; **send only after approval**; retry on fail |
| 21 | **Frontend foundation** | 1,5 | React/Vite/Tailwind/ShadCN; AuthContext; API client | `frontend/src` (App, context, services) | consumes G1 | — | — | App runs; login flow; protected route guard |
| 22 | **Frontend integration** | 21 + (8,9,11,12,17,18,19,20,10) | pages wired to APIs | `frontend/src/pages,components,charts` | consumes G3/G5/G6/G7/G11/G12/G13/G14/G15 | — | — | Each page reads/writes its API; role-scoped UI |
| 23 | **Testing** | per-layer (continuous) + full pass | unit/integration/api/ai/rag/UAT/security/perf | `backend/tests`, FE tests | all | all | all | TRD §38 suite green; RTM TC-* mapped |
| 24 | **Demo preparation** | 22,23 | seeded demo, scenarios, walkthrough | `Data`, `Knowledge`, demo scripts | all | all | all | End-to-end demo runs (import→update→dashboard→FDS→report→approve) |

---

## 2. Dependency chains (text diagram)

```
1 Backend foundation
├─► 2 Config/Env ──► 13 Provider Adapter ──┐
├─► 3 DB models ──► 4 Migrations ──┐        │
│                                  ▼        │
└─► (1+2+3+4) ─► 5 Auth/RBAC       │        │
                     │             │        │
        6 Audit ◄────┘ (needs 3,4) │        │
           │                       │        │
           ▼                       ▼        ▼
        7 Import ─► 8 KPI mgmt ─► 9 Monthly updates        14 Skills (needs 3,6,13)
                         │             │                        │
                10 Approval/HITL       ▼                        ▼
                         │        11 Dashboard            15 Agents (needs 6,10,13,14)
                         │             │                        │
                         ▼             ▼          16 RAG (needs 3,6,13)
                12 FDS (needs 9,13,14,15) ◄───────────┤         │
                         │                            ▼         ▼
                         ├──────────────► 17 Chatbot (14,15,16)
                         ├──────────────► 18 Copilot (11,12,15,16)
                         ├──────────────► 19 Reports (10,11,12,15)
                         └──────────────► 20 Notifications (9,10,15)
21 Frontend foundation (1,5) ─► 22 Frontend integration (21 + backend APIs)
23 Testing (continuous, per layer) ─► 24 Demo (22,23)
```

---

## 3. Build Order (critical path)
`1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 13 → 14 → 15 → 16 → 12 → 17 → 18 → 19 → 20 → 21 → 22 → 23 → 24`

> Matches CLAUDE.md §16. Note: **13 (Provider Adapter)** and **14 (Skills)** can start as soon as **2/3/6**
> are ready; **12 (FDS)** is placed after skills/agents because it consumes S4/S5/S6/S7 + FDS Agent.

---

## 4. What can be built in parallel
- **Track A (data/app spine):** 3→4 then 5→6→7→8→9→10→11.
- **Track B (AI core):** 13→14→15→16 (needs only 2/3/6 to start) — can run **alongside** Track A after 6.
- **Track C (frontend):** 21 can start after **5** (auth) using stubbed/real APIs; 22 follows backend APIs.
- **Testing (23):** continuous, in parallel, per layer.
- Convergence: **12 FDS, 17 Chatbot, 18 Copilot, 19 Reports, 20 Notifications** need both tracks ready.

## 5. What must NOT be built before its dependencies
- ❌ No **routes** before **Auth/RBAC (5)** — every protected route needs JWT+RBAC.
- ❌ No **agent/skill writes or any formal action** before **Audit (6)** and **Approval/HITL (10)**.
- ❌ No **Chatbot/Copilot (17/18)** before **RAG (16)** + **Agents (15)** — else ungrounded answers.
- ❌ No **FDS (12)** before **Skills (14)** + **Agents (15)** + **provider (13)**.
- ❌ No **Reports/Notifications send (19/20)** before **Approval (10)** — nothing sends without approval.
- ❌ No **monthly Excel** path ever; **import (7)** is one-time only.
- ❌ No **frontend integration (22)** of a page before its **backend API** exists.

---

## 6. Exact Next Coding Prompt — CP1 Project Scaffolding

> Run this only after A8 approval. Build-test-stop.

```
CP1 — PROJECT SCAFFOLDING

Goal: Create the backend and frontend skeletons per CLAUDE.md §1 and A8 item 1, with nothing
business-specific yet. Then verify both apps start.

Backend (/backend):
- Python + FastAPI app (app/main.py) mounting router prefix /api/v1.
- Consistent error envelope {code, message, details, correlation_id} via an exception handler.
- CORS middleware (allow the local frontend origin only).
- Health endpoints (A6 G18): GET /api/v1/health (liveness) and GET /api/v1/health/ready (stub).
- Folder skeleton (empty packages with __init__): api/v1/routes, core, services, repositories,
  models/{operational,knowledge,ai}, schemas, agents, skills, rag, providers, knowledge,
  notifications, reports, audit, db.
- Files: requirements.txt (fastapi, uvicorn, sqlalchemy, alembic, pydantic, python-jose, passlib,
  python-dotenv), pyproject.toml, config.md (skeleton: profiles development/testing/production,
  llm_provider, embedding_provider, models), .env.example (no secrets), db/session.py (SQLite dev URL).

Frontend (/frontend):
- React + Vite + TypeScript + Tailwind + ShadCN UI scaffold; Recharts installed.
- src/: App.tsx with a router, an empty AuthContext, a services/api.ts client pointing to /api/v1,
  a placeholder Login page and a protected Dashboard placeholder.
- .env.example (VITE_API_BASE_URL).

Constraints (from CLAUDE.md):
- No business logic, no DB models, no auth logic yet (those are CP3/CP4).
- No secrets committed. /api/v1 versioning. Provider-agnostic placeholders only.

Test before continuing:
- Backend: `uvicorn` starts; GET /api/v1/health returns 200 {status:"ok"}.
- Frontend: dev server starts; Login placeholder renders; API client base URL resolves.
- Report what was created and the test results. Then STOP and wait for approval to proceed to CP2.
```

---

## Final Output (summary)
1. **Complete dependency map** — §1 (24 items, each with depends-on/produces/folder/API/DB/agents-skills/test).
2. **Build order** — §3 (critical path).
3. **Parallel tracks** — §4 (data spine · AI core · frontend · testing).
4. **Do-not-build-early rules** — §5.
5. **Exact next coding prompt** — §6 (CP1 Project Scaffolding).

> **No code written.** Coding starts at CP1 only after approval.

---
*End of Development Dependency Map v0.1 — DRAFT. No code. Frozen baselines unmodified. Awaiting approval.*
