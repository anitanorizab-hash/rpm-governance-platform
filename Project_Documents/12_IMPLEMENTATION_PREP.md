# IMPLEMENTATION PREPARATION PACKAGE (A7)
### Agentic AI Strategic Governance Platform — RPM 2026–2035
#### Final pre-coding package: folder structure · build sequence · control rules · first 10 coding prompts

| Field | Value |
|-------|-------|
| Document | A7 — Implementation Prep |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Companion | `./CLAUDE.md` (canonical development instruction file) |
| Baselines (frozen/approved) | HMW/BRD/RTM/TRD v1.0; A1–A4 accepted; A5/A6 v1.0 |
| Boundary | Preparation only — **no code**. |

---

## 1. Complete Folder Structure

### 1.1 Backend (`/backend`)
```
backend/
├── app/
│   ├── main.py                     # FastAPI app, /api/v1 mount, error envelope, CORS
│   ├── api/v1/
│   │   ├── deps.py                 # JWT + RBAC dependencies
│   │   └── routes/                 # one router per API group (A6 G1–G18)
│   │       ├── auth.py  users.py  kpis.py  import_.py  updates.py
│   │       ├── dashboard.py  fds.py  ai.py  skills.py  knowledge.py
│   │       ├── chatbot.py  copilot.py  reports.py  notifications.py
│   │       ├── approvals.py  audit.py  config.py  health.py
│   ├── core/
│   │   ├── config.py               # loads config.md profile + .env
│   │   ├── security.py             # JWT access/refresh, password, RBAC helpers
│   │   ├── logging.py  errors.py
│   ├── services/                   # business services (A1/A6) → one per service
│   │   ├── auth_service.py  kpi_service.py  import_service.py
│   │   ├── update_service.py  validation_service.py  dashboard_service.py
│   │   ├── finance_service.py  agent_orchestration_service.py
│   │   ├── knowledge_service.py  chatbot_service.py  copilot_service.py
│   │   ├── report_service.py  notification_service.py
│   │   ├── workflow_service.py  audit_service.py  admin_config_service.py
│   ├── repositories/               # SQLAlchemy data access (per entity group)
│   ├── models/                     # SQLAlchemy models (A5)
│   │   ├── operational/  knowledge/  ai/   base.py
│   ├── schemas/                    # Pydantic request/response
│   ├── agents/                     # A2
│   │   ├── orchestrator.py
│   │   ├── kpi_analysis.py  validation.py  fds.py  risk.py
│   │   ├── strategic_recommendation.py  knowledge_alignment.py
│   │   ├── chatbot.py  report_generation.py  notification.py
│   │   ├── audit.py  executive_copilot.py
│   ├── skills/                     # A3 (S1–S15) + registry
│   │   ├── registry.py
│   │   └── s01_kpi_analysis.py … s15_ralph_loop_review.py
│   ├── rag/                        # A4
│   │   ├── ingestion.py  chunking.py  embeddings.py
│   │   ├── retrieval.py  citation.py  vector_store.py
│   ├── providers/                  # provider abstraction (TRD §17.2)
│   │   ├── adapter.py  groq_client.py  openai_client.py
│   │   ├── anthropic_client.py  embeddings_provider.py
│   ├── knowledge/                  # sources, links, refresh
│   ├── notifications/              # email_queue.py  sender.py
│   ├── reports/                    # generator.py  templates/
│   ├── audit/                      # logger.py
│   └── db/                         # session.py  base.py
├── alembic/                        # versions/  env.py
├── tests/                          # unit/  integration/  api/  ai/  rag/
├── config.md                       # business config (profiles, providers, models)
├── .env.example                    # required env vars (no secrets committed)
├── requirements.txt  pyproject.toml
```

### 1.2 Frontend (`/frontend`)
```
frontend/
├── src/
│   ├── main.tsx  App.tsx
│   ├── pages/                       # Login, Dashboard, KpiList, KpiDetail,
│   │                               # MonthlyUpdate, Finance, Chatbot, Copilot,
│   │                               # Approvals, Reports, Admin
│   ├── components/
│   │   ├── ui/                      # ShadCN UI components
│   │   ├── dashboard/  kpi/  charts/ (Recharts)  common/
│   ├── services/                    # api.ts, authService.ts, kpiService.ts, …
│   ├── context/                     # AuthContext.tsx
│   ├── hooks/                        # useAuth, useKpis, useDashboard, …
│   ├── lib/  styles/
├── index.html  vite.config.ts  tailwind.config.js  package.json  .env.example
```

### 1.3 Project Documentation & Data
```
Project_Documents/      # 01..12 (HMW, BRD, TRD, RTM, A1–A7)
Project_Knowledge_Base/ # 11 KB files (rules, decisions, glossary, change log, gaps)
Architecture/           # exported diagrams / architecture references (optional)
Prompts/                # coding prompts (this package) + prompt-engineering guide
Data/                   # operational input (Pelan Taktikal JPN/PPD) + raw sources
Knowledge/              # RAG corpus: RPM 2026–2035, guidelines, link registry
Logs/                   # runtime/application logs (gitignored)
CLAUDE.md               # development instruction file (root)
```

---

## 2. Build Sequence (25 steps)
See `CLAUDE.md §16` — the authoritative ordered sequence (scaffolding → backend foundation → config →
DB models → migrations → auth/RBAC → import → KPI → monthly update → audit → approval → dashboard → FDS →
provider adapter → skills → agents → RAG → chatbot → copilot → reports → notifications → frontend
foundation → frontend pages → testing → demo).

---

## 3. Development Control Checklist
See `CLAUDE.md §17` — applied to **every** change:
1. Traceable to BRD/RTM/TRD · 2. Build layer by layer · 3. Test each layer before next · 4. No agent
auto-approve/amend/delete/send · 5. All AI outputs logged · 6. Official actions require human approval ·
7. Operational/knowledge separation · 8. Excel import-once · 9. Monthly updates in-system · 10. AI provider
config-driven.

---

## 4. First 10 Coding Prompts (to use AFTER approval)

> Each prompt builds one layer, tests it, and stops. Run in order; do not skip. Cite RTM IDs in each.

**Prompt 1 — Project scaffolding.**
"Create the backend (`/backend`) and frontend (`/frontend`) skeletons per CLAUDE.md §1 folder structure.
Backend: FastAPI app with `/api/v1` mount, health endpoints (G18), consistent error envelope, CORS.
Frontend: React+Vite+Tailwind+ShadCN scaffold with an empty AuthContext and API client. Add
`requirements.txt`, `pyproject.toml`, `package.json`, `.env.example`, `config.md` skeleton. No business
logic yet. Then verify both apps start and the health endpoint returns OK."

**Prompt 2 — Config & environment + Provider Adapter stub.**
"Implement `core/config.py` to load profile (development/testing/production) from `config.md` and secrets
from `.env`. Implement the Provider Adapter interface (`chat()`, `embedding()`) with a Groq client (dev)
and stubs for OpenAI/Anthropic + embeddings (local ST/OpenAI). Business logic must stay provider-agnostic.
Add unit tests for config loading and adapter selection (TR-013/018, BR-044). Test, then stop."

**Prompt 3 — Database models + Alembic.**
"Implement SQLAlchemy models for the Operational group per A5 (reference → access → KPI core → monitoring →
finance → governance → cross-plane), plus Knowledge and AI metadata groups. Set up Alembic and create the
initial migration. AuditLog append-only; Indicator/Target separated; Budget_Status reference table. Build
on SQLite; verify the schema also migrates on PostgreSQL. Add model unit tests. Test, then stop."

**Prompt 4 — Authentication & RBAC.**
"Implement AuthService + JWT (access/refresh, expiry), MOE-domain restriction (@moe.gov.my/@moe-dl.edu.my),
and the RBAC dependency used by all routes. Implement G1 Auth API and G2 User/Role API. Enforce
server-side RBAC. Add CORS + CSRF (cookie refresh) config. Tests: login/refresh/logout, domain rejection,
RBAC allow/deny (FRQ-001/002, BR-003/031). Test, then stop."

**Prompt 5 — Audit trail (wired early).**
"Implement AuditService + append-only AuditLog and the `audit_logging` skill (S13). Provide a reusable hook
services call on every mutation/decision. Implement G16 Audit API (read-only, role-scoped). Tests: append
immutability, query scoping (FRQ-024, BR-009/029). Test, then stop."

**Prompt 6 — Import pipeline (one-time Excel).**
"Implement ImportService + `excel_parsing` skill to import Pelan Taktikal JPN/PPD into operational entities
(Teras/Strategy/Prakarsa/KPI/Activity/PIC/Financial_Allocation). Implement Validation skill (S2) for
completeness. Implement G4 Import API. Enforce import-once; reject knowledge files. Log an import batch.
Tests with a sample workbook (FRQ-003, INTQ-001, BR-001/018). Test, then stop."

**Prompt 7 — KPI management + completeness.**
"Implement KpiService and G3 KPI API (CRUD, PIC assignment, indicator/target, completeness). Enforce the
**amendment-window rule** (statement/indicator/target editable only in July/October → else 409) backed by
Amendment_Window + KPI_Amendment with audit. Tests for completeness warnings and amendment-window
behaviour (FRQ-004/005/006/010, BR-004/008). Test, then stop."

**Prompt 8 — Monthly update workflow.**
"Implement UpdateService and G5 Monthly Update API: PIC submits achievement, finance_status (six-value),
evidence, remarks; in-system only (no Excel). Persist KPI_Monthly_Update + Evidence; write audit. Trigger
KPI Analysis (S1) and Risk (S3) skills post-save (advisory). Tests: validation, role-scope (own KPIs),
six-value status (FRQ-007, BR-002/010). Test, then stop."

**Prompt 9 — Approval workflow (HITL).**
"Implement WorkflowService and G15 Approval API: a generic draft→pending→approve/reject state machine for
reports, notifications, and recommendations. No formal action proceeds without approval; every decision is
audited. Tests: approve/reject paths, role enforcement, no-action-without-approval (FRQ-017, BR-015,
ASM-11). Test, then stop."

**Prompt 10 — Dashboard services (Teras 1–7).**
"Implement DashboardService and G6 Dashboard API: per-Teras roll-ups (count, achievement, risk, missing
info, budget status, submission), KPI mapping table, and high-risk quick list. Role-scoped reads. Use S1/
S14 for status/aggregation; AI summary can be a stub for now. Tests: aggregation correctness, role scoping,
all 7 Teras represented (FRQ-011/025, BR-020/021). Test, then stop."

> Prompts 11+ (later): FDS → skills layer (S4/S5/S6/S7…) → agent layer/orchestrator → RAG (keyword→vectors)
> → chatbot → copilot → reports → notifications/email → frontend foundation → frontend pages → full testing
> → demo. Each follows the same build-test-stop discipline.

---

## Final Output (summary)
1. **Folder structure** — §1 (backend, frontend, docs/data).
2. **CLAUDE.md** — created at project root (15 rule sections + build sequence + control checklist).
3. **Build sequence** — CLAUDE.md §16 (25 steps).
4. **Development control checklist** — CLAUDE.md §17 (10 controls).
5. **First 10 coding prompts** — §4 above.

> **No code written.** Coding begins only after this package is approved.

---
*End of Implementation Preparation Package v0.1 — DRAFT. No code. Frozen baselines unmodified. Awaiting approval.*
