# CLAUDE.md — Development Instruction File
### Agentic AI Strategic Governance Platform for RPM 2026–2035

> **This file governs all coding.** Read it before writing any code. It is derived from the frozen
> baselines and accepted blueprints. If a coding request conflicts with this file or the frozen baselines,
> **stop and flag it** — do not silently deviate. Status: Draft v0.1 (awaiting approval). Date: 2026-06-27.

---

## 1. Project Purpose
A government education-governance platform that centralises KPI execution of **RPM 2026–2035** across
**JPN → PPD → School**, replacing scattered Excel with a single, audit-grade system of record augmented by
an **advisory agentic-AI layer**. It enforces disciplined monthly KPI updates, detects missing data,
monitors performance and budget, provides **Financial Decision Support**, a **Teras 1–7 dashboard**, a
**RAG-grounded chatbot**, **KPI↔RPM alignment**, and an **Executive Copilot** — with **humans approving
every formal action**.

## 2. Frozen Baselines (authoritative — do not modify)
- **HMW v1.0** (`Project_Documents/02_PAIN_POINTS_HMW.md`)
- **BRD v1.0** (`Project_Documents/03_BRD.md`)
- **RTM v1.0** (`Project_Documents/05_REQUIREMENTS_TRACEABILITY_MATRIX.md`)
- **TRD v1.0** (`Project_Documents/04_TRD.md`)
- **Architecture blueprints:** A1 System (`06`), A2 Agents (`07`), A3 Skills (`08`), A4 RAG (`09`), A5 Database v1.0 (`10`), A6 API v1.0 (`11`).
- **Knowledge base:** `Project_Knowledge_Base/` (rules, decisions, glossary, change log, questions/gaps).
- **B2A Authoritative Decisions** (`PROJECT_CONTEXT.md §6c`) take precedence unless the user changes them.

## 3. Approved Tech Stack (AD-007/008, TR-009…019)
- **Frontend (L1):** React · Vite · Tailwind CSS · ShadCN UI · Recharts.
- **Backend (L2):** Python · FastAPI · SQLAlchemy · Alembic · JWT auth.
- **Database (L5):** SQLite (dev) · PostgreSQL (prod).
- **Vector/RAG (L4):** Chroma or pgvector · **keyword-search fallback for V1**.
- **LLM provider (L3):** Groq (dev) · OpenAI/Anthropic (prod) — via `config.md` + `.env`.
- **Embeddings:** **separate** from LLM — local Sentence Transformer / OpenAI (dev) → OpenAI (prod).
- **Six-layer architecture (AD-008):** L1 Presentation · L2 Application · L3 AI · L4 Knowledge · L5 Data · L6 Infrastructure.

## 4. Build Rules
- Build **layer by layer**; **test each layer before the next** (TR-006); develop in VS Code.
- **Only implement features traceable to BRD/RTM/TRD.** No invented features.
- Follow the **Build Sequence (§16)** and the API/DB/Agent/Skill blueprints.
- Keep changes small and verifiable; commit per layer (when the user asks to commit).

## 5. Architecture Rules
- Respect the **six layers**; dependencies flow downward. L1 talks only to L2 (REST `/api/v1`); L1 never touches DB/AI/Knowledge directly.
- **Operational plane (DB)** and **Knowledge plane (RAG/vector)** stay separate (BR-017); in prod, knowledge tables in a separate schema.
- Agents/services reach data **only through services/repositories** — never raw cross-layer access.

## 6. Agent Rules (`/agents`)
- **Capability-driven**; current primary agents per A2. Agents are **advisory** — they propose, never finally act.
- Agents communicate via the **Agent Orchestrator** + backend services; never directly with the DB.
- **No agent may approve, amend, delete, or send** official outputs (BR-028/ASM-11) — route to the Approval API (HITL).
- Every agent run + output is **logged** (Agent_Execution, AuditLog).

## 7. Skills Rules (`/skills`)
- Skills are **reusable, independently testable**; shared via the Skill Registry — **never duplicated** inside agents (BR-042).
- Skills **compute/draft only**; they never write official records or approve/send.
- Skills are **versioned**; logged when invoked by AI (Skill_Execution).

## 8. RAG Rules (`/rag`, `/knowledge`)
- RAG uses **RPM 2026–2035 as the main reference** (BR-012) + uploaded docs + **admin-validated live links** (BR-024).
- **Pelan Taktikal is operational input only** — never ingested as a knowledge source.
- Answers **cite sources** (BR-025); inaccessible source → clear message, **never guess** (BR-026); no grounding → fixed fallback string (BR-027):
  `"I cannot find this information in the available KPI data or knowledge sources."`
- Chatbot KPI data is **role-scoped**. Keyword fallback acceptable for V1; embeddings via Provider Adapter `embedding()`.

## 9. Database Rules (`/database`)
- Per A5: 3 groups (Operational/Knowledge/AI). SQLAlchemy models + **Alembic** migrations.
- **AuditLog is append-only** (no update/delete). KPI **Indicator/Target** separated for amendment history.
- **Budget status** uses the six-value vocabulary (reference table). Build SQLite first; validate on PostgreSQL early.
- Distinguish **AI_Recommendation (log)** from **Strategic_Recommendation (operational, human-reviewed)**.

## 10. API Rules (`/routes`, `/services`)
- All routes under **`/api/v1`**; consistent error envelope `{code,message,details,correlation_id}`.
- **JWT** on all protected routes; **RBAC** enforced server-side on every route.
- **AI APIs are advisory** (no approve/amend/send). **Reports/notifications send only after Approval API** (HITL).
- **Monthly updates in-system** (no monthly Excel); **Excel is import-once**.

## 11. Security Rules
- Login restricted to **`@moe.gov.my` / `@moe-dl.edu.my`** (BR-003).
- **JWT** (access + refresh, expiry); **CORS** to approved origins; **CSRF** for cookie refresh; **HTTPS in production**.
- **Secrets only in `.env`** (never in code or `config.md`); rate limiting; input validation (Pydantic + business rules).
- **Encrypt sensitive data at rest in production.** Least privilege; plane separation.

## 12. Human-in-the-Loop Rules
- **Human approval is mandatory** before any formal action, report issue, or email send (BR-015/ASM-11).
- AI proposes; an authorised officer disposes. Every decision is recorded in **Approval** + **AuditLog**.
- The **RALPH LOOP Review skill (S15)** may pre-check AI outputs but **never approves/sends**.

## 13. Configuration Rules
- AI providers configured via **`config.md`** (profiles: development / testing / production); **keys in `.env`**.
- **Business logic must be provider-agnostic** — use the Provider Adapter (`chat()` / `embedding()`); switching provider = config change only.
- Config changes are **audited**.

## 14. Testing Rules
- Per TRD §38: **Unit · Integration · API · AI Response Validation · RAG Validation · UAT · Security · Performance.**
- **Test each layer before the next.** Skills unit-tested (deterministic cores); RAG validated (retrieval/citation/fallback/role-access/grounding).
- Map tests to RTM `TC-*`. No layer is "done" until its tests pass.

## 15. Do-NOT-DO Rules
- ❌ Do **not** code features not traceable to BRD/RTM/TRD.
- ❌ Do **not** let AI agents approve, amend, delete, or send official outputs.
- ❌ Do **not** mix operational and knowledge data.
- ❌ Do **not** use Excel for monthly updates (import-once only).
- ❌ Do **not** hard-code an AI provider or put secrets in code/`config.md`.
- ❌ Do **not** ingest Pelan Taktikal as a knowledge source.
- ❌ Do **not** skip the audit trail or the human-approval gate.
- ❌ Do **not** modify frozen baselines (HMW/BRD/RTM/TRD/A5/A6) without a logged change request.

---

## 16. Build Sequence (exact order)
1. Project scaffolding (backend+frontend skeleton, `/api/v1`, health, error envelope)
2. Backend foundation (FastAPI app, structure)
3. Config & environment (`config.md`, `.env.example`, profiles, Provider Adapter stub)
4. Database models (SQLAlchemy — reference → access → KPI core → monitoring → finance → governance → cross-plane → knowledge → AI)
5. Alembic migrations
6. Authentication & RBAC (JWT access/refresh, MOE-domain, role dependency)
7. Import pipeline (one-time Excel → DB; `excel_parsing`)
8. KPI management (records, indicator/target, PIC, completeness)
9. Monthly update workflow (in-system; amendment-window control)
10. Audit trail (append-only; wired early)
11. Approval workflow (HITL)
12. Dashboard services (Teras 1–7 roll-ups)
13. Financial Decision Support (budget status, Low Cost High Impact, OBB, recommendations)
14. AI provider adapter (chat/embedding; Groq dev)
15. Skills layer (S1–S15; registry)
16. Agent layer (orchestrator + 11 agents)
17. RAG & knowledge base (ingestion, keyword V1 → embeddings/Chroma, retrieval+citation)
18. Chatbot (grounded, cited, role-scoped, fallback)
19. Executive Copilot (synthesis)
20. Reports (generate → approve → archive)
21. Notifications & email queue (reminders/escalation; retry; HITL send)
22. Frontend foundation (React/Vite/Tailwind/ShadCN; auth context; API client)
23. Frontend pages & integration (dashboard/KPI/finance/chatbot/copilot/approvals/admin)
24. Testing (all 8 types; per-layer)
25. Demo preparation

---

## 17. Development Control Checklist (apply to every change)
- [ ] Traceable to BRD/RTM/TRD (cite the requirement ID).
- [ ] Correct layer; respects layer boundaries.
- [ ] Operational vs knowledge separation preserved.
- [ ] JWT + RBAC enforced (if an API).
- [ ] AI output advisory + logged; no autonomous formal action.
- [ ] Human-approval gate present for formal actions/reports/emails.
- [ ] Provider via config/adapter; no secrets in code.
- [ ] Audit entry written for mutations/decisions.
- [ ] Tests written and passing for this layer.
- [ ] No frozen baseline modified.

---
*CLAUDE.md v0.1 — DRAFT. Governs development once approved. Derived from frozen baselines; not itself a baseline.*
