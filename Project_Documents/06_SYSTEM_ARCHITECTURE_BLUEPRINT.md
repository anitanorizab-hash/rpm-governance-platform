# SYSTEM ARCHITECTURE BLUEPRINT
### Agentic AI Strategic Governance Platform — RPM 2026–2035
#### Primary implementation guide for developers

| Field | Value |
|-------|-------|
| Document | A1 — System Architecture Blueprint |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Audience | Software developers (implementation reference) |
| Baselines (frozen, not modified) | HMW v1.0, BRD v1.0, RTM v1.0, TRD v1.0 |
| Boundary | Architecture/diagrams only — **no code**; implements the frozen baselines (no new requirements). |

> **How to read this blueprint.** It is self-contained: each diagram is understandable on its own. It
> realises the six-layer architecture (AD-008) and the approved stack — Frontend: React/Vite/Tailwind/
> ShadCN/Recharts · Backend: Python/FastAPI/SQLAlchemy · DB: SQLite(dev)/PostgreSQL(prod) ·
> Vector: Chroma/pgvector (+keyword fallback) · LLM: Groq(dev)/OpenAI·Anthropic(prod), Embeddings:
> local ST/OpenAI(dev)→OpenAI(prod), via a Provider Adapter (`chat()`/`embedding()`). All AI is
> **advisory**; humans approve every formal action (HITL).

---

## 1. Overall System Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ USERS  (MOE accounts: @moe.gov.my / @moe-dl.edu.my)                                │
│ Super Admin · JPN Admin · Sector Admin · PPD Admin · KPI PIC · Finance · Executive │
└───────────────────────────────┬──────────────────────────────────────────────────┘
                                 │ HTTPS (JWT)
┌────────────────────────────────▼─────────────────────────────────────────────────┐
│ L1 PRESENTATION  — React + Vite + Tailwind + ShadCN UI + Recharts (SPA)            │
│   Dashboard(Teras1–7) · KPI forms · Chatbot · Copilot · Approvals · Admin          │
└───────────────────────────────┬────────────────────────────────────────────────── ┘
                                 │ REST /api/v1 (JSON, Bearer JWT)
┌────────────────────────────────▼─────────────────────────────────────────────────┐
│ L2 APPLICATION  — Python + FastAPI + SQLAlchemy                                    │
│   Auth/RBAC · Business Services · Workflow/HITL · Import · Notification engine      │
└───────┬───────────────────────────────┬───────────────────────────────┬──────────┘
        │ (advisory)                     │ (read/write)                   │ (grounding)
┌───────▼──────────────────┐  ┌──────────▼─────────────┐      ┌──────────▼───────────┐
│ L3 AI                    │  │ L5 DATA                │      │ L4 KNOWLEDGE          │
│ Agent Orchestrator       │  │ SQLite(dev)/Postgres   │      │ RAG · Vector store    │
│ Specialised Agents       │  │ Operational DB         │      │ (Chroma/pgvector)     │
│ Skills Layer · FDS       │◄─┤ Audit Trail            │      │ Docs + Live links     │
│ Chatbot · Copilot        │  └────────────────────────┘      │ Embeddings            │
│ Provider Adapter ────────┼───────────────► (external LLM/embedding providers)      │
└───────────────────────── ┘                                  └──────────────────────┘
┌────────────────────────────────────────────────────────────────────────────────── ┐
│ L6 INFRASTRUCTURE — config.md · .env · Provider switching · Logging · Monitoring · │
│                     Deployment · Security (JWT, RBAC, at-rest encryption[prod])     │
└──────────────────────────────────────────────────────────────────────────────────┘
            dependencies flow downward; L3↔L4 collaborate; L5/L6 underpin all
```

---

## 2. Component Diagram

```
┌─ L1 FRONTEND (React SPA) ─────────────────────────────────────────────┐
│  DashboardModule · KpiModule · FinanceModule · ChatbotPanel ·          │
│  CopilotPanel · ApprovalsModule · AdminModule                          │
└───────────────────────────────┬───────────────────────────────────────┘
                                 │ REST
┌─ L2 BACKEND (FastAPI) ─────────▼──────────────────────────────────────┐
│  AuthService ── RBAC                          (M1)                     │
│  ImportService · KpiService                   (M2)                     │
│  UpdateService · ValidationService            (M3/M4)                  │
│  DashboardService                             (M5)                     │
│  FinanceService ─► Financial Decision Support (M6)                     │
│  AgentOrchestrationService ─► AI Layer        (M7)                     │
│  KnowledgeService ─► RAG                       (M8)                     │
│  ChatbotService · CopilotService              (M9/M7)                  │
│  ReportService                                (M10)                    │
│  NotificationService (Email/queue/retry)      (M11)                    │
│  WorkflowService (HITL) · AuditService        (M12)                    │
│  AdminConfigService                           (M13)                    │
└───────┬───────────────────────┬───────────────────────┬───────────────┘
        ▼ (L5 DATA)             ▼ (L3 AI)               ▼ (L4 KNOWLEDGE)
┌──────────────────┐  ┌──────────────────────────┐  ┌─────────────────────────┐
│ Operational DB   │  │ Agent Orchestrator        │  │ RAG Pipeline            │
│  KPI·Teras·PIC   │  │ Agents: DataIntegration,  │  │  ingest→chunk→embed→    │
│  MonthlyUpdate   │  │  Validation, KPI Analysis,│  │  vector store           │
│  FinanceAlloc.   │  │  Risk, Financial Monitor, │  │  (Chroma/pgvector)      │
│  Recommendation  │  │  Budget Intelligence,     │  │  + keyword fallback     │
│  Risk/Alignment  │  │  Intervention, Notify,    │  │ Knowledge Repository:   │
│  AuditLog        │  │  Audit, Report, Chatbot,  │  │  Uploaded Docs ·        │
│  User·Role       │  │  Knowledge Alignment,     │  │  Live Knowledge Links   │
│  AmendmentWindow │  │  Executive Copilot,       │  │  (admin-validated)      │
└──────────────────┘  │  AI Summary               │  └─────────────────────────┘
                      │ Skills Layer (reusable)   │
                      │ FDS · Provider Adapter    │
                      └──────────────────────────┘
Cross-cutting: Authentication · Configuration(config.md/.env) · Audit · Notification · Reporting
```

---

## 3. Layer Interaction

```
L1 → L2 : REST /api/v1 over HTTPS; Bearer JWT; JSON; RBAC checked server-side.
L2 → L5 : SQLAlchemy repositories (CRUD, transactions); append-only writes to AuditLog.
L2 → L3 : AgentOrchestrationService invokes the Agent Orchestrator (advisory results only).
L2 → L4 : KnowledgeService requests RAG retrieval (returns cited context).
L3 → L4 : Agents (Chatbot/Copilot/Alignment) call RAG for grounding.
L3 → ext: Provider Adapter calls LLM (chat) and Embedding providers per config.
L3 → L2 : Returns drafts/recommendations → WorkflowService HITL gate before any action.
L6 ↔ all: config/secrets, provider selection, logging, monitoring, security envelop every layer.
Rule: L1 never touches L3/L4/L5 directly; all access is mediated by L2 services.
```

---

## 4. External Services

```
                         ┌──────────────► Groq           (LLM chat — DEVELOPMENT)
   [Provider Adapter] ───┼──────────────► OpenAI         (LLM chat + Embeddings — PROD/dev option)
     chat() / embedding()└──────────────► Anthropic      (LLM chat — PRODUCTION)
                          (selected by config.md + .env; switch = config only)

   [NotificationService] ───────────────► Email/SMTP     (approved sends only, after HITL)
   [KnowledgeService] ──────────────────► Live Knowledge Links (admin-validated; fetched for RAG)
   Embeddings(dev option): Local Sentence Transformer (in-process, no external call)
```
- Provider keys live only in `.env`; business logic is provider-agnostic.
- External fetches (links) are admin-validated; inaccessible → clear message, never guessed.

---

## 5. Request Flow (complete lifecycle)

```
[User] Login (email+password) 
   │ POST /api/v1/auth/login
   ▼
[AuthService] domain check (@moe.gov.my/@moe-dl.edu.my) → issue JWT (access+refresh)
   │ Bearer JWT
   ▼
[L1 Dashboard] GET /api/v1/dashboard/teras
   ▼
[FastAPI Router] RBAC dependency (role+scope) ── deny→403
   ▼
[DashboardService] (Business Service)
   ├─► [Operational DB] read KPI/MonthlyUpdate/Finance/Risk (role-scoped)
   ├─► [AI Layer] (optional) AI Summary / cached insights
   └─► assemble response
   ▼
[Response JSON] → [L1 renders Recharts + cards]      (every read/write logged to AuditLog)
```

---

## 6. Monthly KPI Workflow

```
[PIC login] ──► [Open KPI → MonthlyUpdateForm]
        │ POST /api/v1/kpis/{id}/monthly-updates
        ▼
[UpdateService] validate (completeness; amendment-window rule for statement/indicator/target)
        ▼
[Operational DB] save MonthlyUpdate + Evidence    ──►  [AuditService] log who/what/when
        ▼
[AI Analysis] (advisory): KPI Analysis (status) · Risk (rating) · Finance roll-up
        ▼
[Executive Dashboard] Teras 1–7 refresh (status·risk·budget·submission·AI summary)
        ▼
[Reports] monthly report DRAFT ──► [HITL approve] ──► issue/distribute (audited)
   If gaps/overdue → Notification Agent drafts reminder → HITL approve → send
```

---

## 7. Financial Decision Support (FDS) Workflow

```
[Budget data] FinanceAllocation (6-value status, OS object codes, expenditure)
        ▼
[Budget Intelligence]  budget status · funding-gap detection · budget-risk analysis
        ▼
[Low Cost High Impact Analysis]  analyse activities · expected impact · lower-cost alternatives
        │                         · resource optimisation (collaboration, consolidation,
        │                           shared resources, digital alternatives)
        ▼
[Strategic / Intervention Recommendation]  alternative programmes · strategies · prioritise
        ▼
[Executive Copilot]  Executive Financial Insight: recommendations + rationale (grounded via RAG)
        ▼
[HUMAN APPROVAL] (HITL gate)  ──► approved → action/report ; rejected → revise
        (all FDS outputs advisory; logged to AuditLog; surfaced on Dashboard DSH-05/08)
```

---

## 8. AI Workflow

```
[User request]  (e.g. "summarise at-risk KPIs and budget options")
        ▼
[Executive Copilot]  (or Chatbot for Q&A)
        ▼
[Agent Orchestrator]  (custom, V1) — assembles context, routes, logs
        ▼
[Specialised Agents]  KPI Analysis · Risk · Financial Monitoring · Budget Intelligence ·
                      Intervention · Knowledge Alignment · AI Summary · Report/Notification
        ▼
[Skills Layer]  reusable: status_classification · risk_scoring · low_cost_high_impact ·
                teras_aggregation · rag_retrieval_and_citation · email_drafting · audit_logging
        ▼
[Knowledge (RAG)]  retrieve from RPM 2026–2035 + docs + live links → cited context
        │  (Provider Adapter: chat() via Groq/OpenAI/Anthropic; embedding() via ST/OpenAI)
        ▼
[Response]  advisory output + citations  ──► HITL gate if it triggers a formal action
            If no grounding → fixed fallback: "I cannot find this information…"
```

---

## 9. Deployment View

```
┌──────────────── DEVELOPMENT (local) ────────────┐   ┌──────── PRODUCTION (cloud / gov-approved*) ───────┐
│ React+Vite dev server (localhost)                │   │ Built SPA (static hosting / reverse proxy)        │
│ FastAPI (uvicorn, local)                         │   │ FastAPI (ASGI) behind HTTPS                        │
│ DB: SQLite (file)                                │   │ DB: PostgreSQL + pgvector (separate schema)       │
│ Vector: Chroma / keyword fallback                │   │ Vector: pgvector                                  │
│ LLM: Groq   Embeddings: local ST / OpenAI        │   │ LLM: OpenAI/Anthropic  Embeddings: OpenAI         │
│ config.md (mode=development) · .env (dev keys)    │   │ config.md (mode=production) · .env via secrets mgr │
│ HTTP ok locally                                  │   │ HTTPS required · data encrypted at rest           │
└──────────────────────────────────────────────────┘   └────────────────────────────────────────────────── ┘
   profiles: development · testing · production         *Hosting/residency/compliance = Requires User
   build & test layer-by-layer (TR-006)                  Confirmation before production (RUC-01/02)
```

---

## 10. Traceability & Notes (for developers)

- **Layers → modules:** L1→M5/UI; L2→M1/M2/M3/M10/M11/M12; L3→M6/M7/M9; L4→M8; L5→M2/M12; L6→M13 (TRD §9.2).
- **Every component implements a frozen requirement** (RTM v1.0); this blueprint adds **no new requirements**.
- **Non-negotiables to honour in code:** MOE-domain login + RBAC; Excel import-once; in-system monthly
  updates; Jul/Oct amendment window + audit; operational/knowledge plane separation; advisory AI + HITL
  before any formal action/report/email; cited answers + fixed fallback; provider switching via config.
- **Build order (recommended):** L5 Data → L2 core services/Auth → L1 dashboard/forms → L3 agents/skills
  → L4 RAG → notification/reporting → cross-cutting (audit/security/logging) → tests per layer.

---
*End of System Architecture Blueprint v0.1 — DRAFT. No code. Frozen baselines unmodified. Awaiting approval.*
