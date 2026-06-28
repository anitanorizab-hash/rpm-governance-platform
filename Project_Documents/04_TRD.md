# TECHNICAL REQUIREMENTS DOCUMENT (TRD)
## Agentic AI Strategic Governance Platform for RPM 2026–2035

> **Build status:** ✅ **v1.0 FROZEN — APPROVED TECHNICAL BASELINE (Freeze Gate 2 PASSED, 2026-06-27).**
> All parts §1–§42 complete; T6 audit + refinements applied. Reopened only via an explicit, logged change
> request. **Baselines (frozen, not modified):** HMW v1.0 (D1), BRD v1.0 (D2), RTM v1.0 (R1).

---

# 1. Document Control

| Attribute | Detail |
|-----------|--------|
| Document title | Technical Requirements Document (TRD) — Agentic AI Strategic Governance Platform for RPM 2026–2035 |
| Document ID | D3-TRD |
| Version | **1.0 (FROZEN — APPROVED TECHNICAL BASELINE)** |
| Date | 2026-06-27 |
| Frozen on | 2026-06-27 by user approval — **Freeze Gate 2 PASSED** |
| Status | Audited (T6) → Refined → **APPROVED · FROZEN ✅** |
| Change control | Reopened only via an explicit, logged change request (CHANGE_LOG.md). |
| Classification | Government — Official (final confirmation vs MOE data-classification policy pending Q-017) |
| Owner | Solution Architecture / AI Solution Design team |
| Traceability | Implements BRD v1.0 (D2) per RTM v1.0 (R1). Introduces **no new business requirements**. |
| Approved stack | AD-007 / TR-009…014 (see §6 Technical Scope). |
| Precedence | Subordinate to frozen HMW/BRD/RTM and the B2A Authoritative Decisions. |

### 1.1 Approval & Sign-off
| Role | Name | Responsibility | Signature | Date |
|------|------|----------------|-----------|------|
| Solution Architect | User (suzila@iegcampus.com) | Endorse technical design | **Approved** | 2026-06-27 |
| AI Solution Designer | User (suzila@iegcampus.com) | Endorse AI architecture | **Approved** | 2026-06-27 |
| Backend/Frontend Leads | _TBC_ | Confirm feasibility | | |
| Security / Compliance | _TBC_ | Confirm security & residency | | |
| Business Owner (JPN) | _TBC_ | Confirm alignment to BRD | | |

### 1.2 Change Control
The TRD follows the project freeze discipline (Draft → Audit → Revise → Freeze). Once frozen (Freeze Gate 2),
it is reopened only via an explicit, logged change request (CHANGE_LOG.md). It must remain consistent with
the frozen BRD/RTM; any conflict is resolved in favour of the business baseline (or via a logged change).

---

# 2. Version History

| Version | Date | Author | Part(s) | Summary |
|---------|------|--------|---------|---------|
| 0.1 | 2026-06-27 | Architecture team | Part 1 | Doc Control … Technical Constraints. |
| 0.2–0.5 | 2026-06-27 | Architecture team | Parts 2–5 | Solution/Layered/Frontend/Backend; Data/Model/Dual-Plane/Import/Workflow; AI/Agents/Skills/RAG/FDS/Chatbot/Copilot; Dashboard/Auth/API/Config/Env/Integration/Notification/Audit/Security/Logging/Errors/NFR/Backup/Deploy/Testing/Risks/Assumptions/Traceability/Appendices. |
| 0.6 | 2026-06-27 | Architecture team | All | T6 audit (overall 94%); applied refinements: LLM/embedding separation, JWT auth, custom orchestrator, config profiles, AI provider strategy, prod at-rest encryption. |
| **1.0** | **2026-06-27** | **Architecture team** | **All** | **APPROVED & FROZEN as the official technical baseline (Freeze Gate 2 passed).** |

---

# 3. Executive Technical Overview

The platform is a **layered, agentic-AI web application** implementing the frozen BRD across six layers:
**Presentation (L1)**, **Application (L2)**, **AI (L3)**, **Knowledge (L4)**, **Data (L5)** and
**Infrastructure (L6)**.

- **Presentation (L1):** a **React + Vite + Tailwind + ShadCN UI** single-page application; **Recharts**
  renders the Teras 1–7 dashboard analytics.
- **Application (L2):** a **Python + FastAPI** backend exposes REST services; **SQLAlchemy** is the ORM. It
  hosts the monthly KPI workflow, one-time Excel import, RBAC enforcement, notification/email engine and the
  **human-in-the-loop (HITL) approval workflow** that gates every formal action.
- **AI (L3):** a **capability-driven multi-agent layer** with a reusable **Skills Layer**, fronted by a
  **provider-abstraction** module that selects **Groq (dev)** or **OpenAI/Anthropic (prod)** via
  `config.md` + `.env`. **Financial Decision Support (FDS)** lives here (Budget Intelligence, Low Cost High
  Impact Analysis, Intervention, Executive Financial Insight). All AI is **advisory**; humans approve.
- **Knowledge (L4):** a **RAG** subsystem ingesting uploaded documents and **administrator-validated live
  links**; **Chroma or pgvector** for vector search with a **keyword-search fallback** for V1; answers are
  **source-cited** with an honest fallback string.
- **Data (L5):** strict **operational/knowledge plane separation**. Operational data in **SQLite (dev) /
  PostgreSQL (prod)**; an append-only **audit trail** records all changes and decisions.
- **Infrastructure (L6):** configuration, secrets, logging/monitoring, deployment; **local for dev**,
  **cloud/government-approved for prod** (subject to compliance confirmation).

The design is **portable** (SQLAlchemy enables SQLite→PostgreSQL; pgvector consolidates vector search into
PostgreSQL in production) and **provider-agnostic** (AI vendor is a config decision, not a code change),
supporting the 10-year horizon and government governance requirements.

---

# 4. Technical Objectives

Technical goals implementing the business objectives (OBJ-01…12) — no new requirements introduced.

| # | Technical Objective | Implements | RTM |
|---|--------------------|-----------|-----|
| TOBJ-01 | Provide a single operational system of record with one-time Excel import. | OBJ-01 | FRQ-003, DATQ-002 |
| TOBJ-02 | Deliver an in-system monthly KPI workflow with validation and audit. | OBJ-02 | FRQ-007, FRQ-024 |
| TOBJ-03 | Enforce KPI ownership and structured KPI data model. | OBJ-03 | FRQ-004/005 |
| TOBJ-04 | Implement amendment-window control and append-only audit trail. | OBJ-04 | FRQ-010/024 |
| TOBJ-05 | Build Financial Decision Support (FDS) with Low Cost High Impact analysis. | OBJ-05 | FRQ-014/029, §17 |
| TOBJ-06 | Provide AI risk detection and early-warning. | OBJ-06 | FRQ-009 |
| TOBJ-07 | Deliver Teras 1–7 dashboard + AI/executive summary + Executive Copilot. | OBJ-07 | FRQ-011/012/023 |
| TOBJ-08 | Implement KPI–RPM alignment via RAG. | OBJ-08 | FRQ-022 |
| TOBJ-09 | Automate human-approved monthly report generation. | OBJ-09 | FRQ-016 |
| TOBJ-10 | Provide notification/reminder engine with approval-gated distribution. | OBJ-10 | FRQ-018/019 |
| TOBJ-11 | Enforce HITL and advisory-only AI across all formal actions. | OBJ-11, ASM-11 | FRQ-017, AIRQ-011 |
| TOBJ-12 | Build a maintainable, portable, provider-agnostic platform for a 10-yr horizon. | OBJ-12 | NFRQ-003/009, AIRQ-012 |

---

# 5. Technical Scope

### 5.1 In technical scope
- React/Vite/Tailwind/ShadCN/Recharts SPA (L1); Python/FastAPI/SQLAlchemy backend (L2).
- One-time Excel import pipeline; monthly KPI workflow; completeness validation; amendment-window control.
- SQLite (dev) / PostgreSQL (prod) operational store; append-only audit trail.
- Capability-driven multi-agent AI layer + Skills Layer; provider abstraction (Groq/OpenAI/Anthropic).
- FDS (Budget Intelligence, Low Cost High Impact Analysis, Intervention, Executive Financial Insight).
- RAG knowledge layer (uploaded docs + admin-validated live links; Chroma/pgvector + keyword fallback).
- Teras 1–7 dashboard; KPI chatbot; Executive Copilot.
- MOE-domain auth + RBAC; notification/email engine; reporting & archive.
- Config (`config.md`) + environment (`.env`) management; logging/monitoring; deployment.

### 5.2 Out of technical scope
- External finance-system write-back (no integration in V1; in-platform entry — ASM-10).
- Autonomous AI actions (excluded — advisory + HITL only).
- Native mobile apps; public (non-MOE) access.
- Production hosting build-out beyond architecture recommendation (pending compliance confirmation).

### 5.3 V1 vs phased (aligns BRD §6.4)
- **V1 (Must):** auth/RBAC, import, KPI master, monthly update, validation, Teras dashboard, status/risk, audit, HITL, monthly report, notifications, Budget Intelligence/Low Cost High Impact, RAG foundation (keyword fallback acceptable).
- **Phase 2 (Should):** chatbot, KPI–RPM alignment, Executive Copilot, full vector RAG + live-link ingestion.
- **Later (Could/Future):** OBB refinement, localisation, SharePoint integration.

---

# 6. Technical Assumptions

| ID | Assumption | Classification | Source |
|----|-----------|----------------|--------|
| TASM-01 | Frontend = React + Vite + Tailwind + ShadCN UI + Recharts. | Approved | TR-009/AD-007 |
| TASM-02 | Backend = Python + FastAPI + SQLAlchemy. | Approved | TR-010/AD-007 |
| TASM-03 | DB = SQLite (dev) / PostgreSQL (prod). | Approved | TR-011/AD-007 |
| TASM-04 | Vector store = Chroma or pgvector; **keyword-search fallback** acceptable for V1. | Approved | TR-012/AD-007 |
| TASM-05 | AI provider = Groq (dev) / OpenAI·Anthropic (prod) via `config.md` + `.env`. | Approved | TR-013/BR-044 |
| TASM-06 | Dev hosting = local environment; prod = cloud/government-approved. | Approved (dev) | TR-014 |
| TASM-07 | Risk scoring & alignment-strength are **rule-based initially**, AI-assisted later; formulas defined in TRD body. | Technical Assumption | ASM-07 (Q-020/Q-021) |
| TASM-08 | OBB method specified in the FDS section (TRD §17). | Technical Assumption | ASM-08 (Q-025) |
| TASM-09 | Identity mechanism (true SSO vs email verification) defined in §Auth. | Technical Assumption | TR-008 (Q-015) |
| TASM-10 | Expected scale sized to Perak pilot; revisit if national. | Technical Assumption | Q-016 |

### 6.1 Requires User Confirmation (before production)
- **RUC-01** Hosting / cloud / government-approved environment + **data residency**. (Q-014)
- **RUC-02** Data classification & compliance regime (e.g. government ISMS). (Q-017)
- **RUC-03** Teras 5–7 source data location for complete import. (GAP-002)
- **RUC-04** Knowledge corpus & live-link list for RAG. (Q-019)

---

# 7. Technical Constraints

| ID | Constraint | Source |
|----|-----------|--------|
| TCON-01 | Excel used for initial import only; database is the working source thereafter. | BR-001/018 |
| TCON-02 | Monthly updates entered in-system by the PIC. | BR-002 |
| TCON-03 | Login restricted to `@moe.gov.my` or `@moe-dl.edu.my`. | BR-003 |
| TCON-04 | KPI statement/indicator/target editable only July/October. | BR-008 |
| TCON-05 | All amendments & consequential AI/human decisions audited (append-only). | BR-009/029 |
| TCON-06 | Human approval required before formal action/report/email. | BR-015/ASM-11 |
| TCON-07 | AI advisory only; cited; honest fallback string on no-result. | BR-025/027/028 |
| TCON-08 | Operational data → DB; knowledge data/links → RAG (separate planes). | BR-017 |
| TCON-09 | Dashboard must summarise & map KPIs by Teras 1–7. | BR-020 |
| TCON-10 | AI provider switchable via config without code change. | BR-044/TR-003 |
| TCON-11 | Live links are RAG sources subject to administrator validation. | BR-024 (Q-022) |
| TCON-12 | Build layer-by-layer in VS Code, testing each layer before the next. | TR-004/006 |

---

## Self-Review — TRD Part 1

| Check | Finding | Action |
|-------|---------|--------|
| Traceable to baselines? | Technical objectives mapped to OBJ + RTM IDs; no new business requirements. | OK |
| Stack reflected? | Approved stack (AD-007/TR-009…014) embedded in overview, scope, assumptions. | OK |
| Open items handled? | Resolved items adopted; remaining classified as Technical Assumption or Requires-User-Confirmation (RUC-01…04). | OK |
| Consistency with frozen docs? | Constraints mirror BRD CON-01…10 + BR refs; no contradiction. | OK |
| Layer framing established? | 6 layers introduced (overview §3) for use in later parts. | OK |

---

**— END OF PART 1 — (APPROVED 2026-06-27)**
*Part 1 covers: Document Control · Version History · Executive Technical Overview · Technical Objectives · Technical Scope · Technical Assumptions · Technical Constraints.*

---

# 8. Overall Solution Architecture

The platform is a layered, agentic-AI web application. The frozen six-layer enterprise architecture
(AD-008) is the organising principle used **consistently throughout this TRD**. Operational and knowledge
data are kept on **separate planes** (BR-017); all AI is **advisory + human-gated** (BR-015/028/ASM-11);
the AI provider is **config-driven** (BR-044).

### 8.1 System context (text diagram)
```
                         ┌──────────────────────────────────────────┐
   MOE Users             │   AGENTIC AI STRATEGIC GOVERNANCE          │        External
 (JPN/PPD/Sector/        │            PLATFORM                        │        Services
  PIC/Finance/Exec)      │                                            │
        │  HTTPS         │  L1 Presentation (React SPA)               │   ┌── LLM Providers
        ├───────────────►│  L2 Application (FastAPI services + HITL)  │──►│   Groq / OpenAI / Anthropic
        │   (MOE login)  │  L3 AI (agents · skills · FDS · copilot)   │   └── (config.md/.env)
        │                │  L4 Knowledge (RAG · vector store)         │   ┌── Email/SMTP (approved sends)
 Admin / IT Ops ────────►│  L5 Data (SQLite/PostgreSQL · audit)       │──►│   Live Knowledge Links
                         │  L6 Infrastructure (config·logging·deploy) │   └── (admin-validated)
                         └──────────────────────────────────────────┘
   Inputs: Pelan Taktikal Excel (one-time import) · Knowledge docs/links (RAG)
```

### 8.2 Architecture principles
- **Layered & modular** (AD-008) — clear boundaries, dependencies flow downward (L1→L6).
- **Plane separation** — operational store (L5) vs knowledge/vector store (L4) never mix (BR-017).
- **Advisory AI + HITL** — agents propose; humans approve formal actions (BR-015/ASM-11).
- **Provider-agnostic** — vendor selected by config; abstraction layer in L3/L6 (BR-044/AD-001).
- **Portable** — SQLAlchemy ORM (SQLite→PostgreSQL); pgvector consolidates vectors into PostgreSQL in prod.
- **Traceable** — every component implements a BRD/RTM requirement; no orphan components.

### 8.3 Request lifecycle (typical, text diagram)
```
User → [L1 React UI] → HTTPS → [L2 FastAPI API + Auth/RBAC] → Business Service
   → (reads/writes) [L5 Operational DB] → (optional) [L3 AI agent via Skills]
   → (grounding) [L4 RAG/Vector] → result → HITL gate (if formal action) → [L1 UI]
   All writes & AI/human decisions → [L5 Audit Trail]
```

---

# 9. Layered System Architecture

The six layers (AD-008), their responsibilities, key technologies and the BRD/RTM elements they realise.

### 9.1 Layer stack (text diagram)
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ L1 PRESENTATION  React · Vite · Tailwind · ShadCN UI · Recharts               │
│    Dashboard (Teras 1–7) · KPI update forms · Chatbot UI · Copilot UI · Admin │
├─────────────────────────────────────────────────────────────────────────────┤
│ L2 APPLICATION   FastAPI · Business Services · Auth/RBAC · REST APIs ·         │
│    Workflow/HITL · Import pipeline · Notification engine                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ L3 AI            Multi-Agent · Skills Layer · FDS · Executive Copilot ·        │
│    KPI Chatbot · AI Orchestration · Provider Abstraction                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ L4 KNOWLEDGE     RAG · Knowledge Repository · Uploaded Docs · Live Links ·     │
│    Embeddings · Vector Store (Chroma/pgvector) + keyword fallback              │
├─────────────────────────────────────────────────────────────────────────────┤
│ L5 DATA          SQLite (dev) / PostgreSQL (prod) · Operational DB ·           │
│    Audit Trail · (pgvector in prod)                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ L6 INFRASTRUCTURE  config.md · .env · AI Provider Switching · Logging ·        │
│    Monitoring · Deployment · Security                                          │
└─────────────────────────────────────────────────────────────────────────────┘
         dependencies flow downward; L3↔L4 collaborate; L5/L6 underpin all
```

### 9.2 Layer responsibilities & traceability
| Layer | Responsibilities | Key tech | Realises (RTM modules) |
|-------|------------------|---------|------------------------|
| **L1 Presentation** | UI, dashboard, forms, chat/copilot surfaces, role-scoped views | React, Vite, Tailwind, ShadCN, Recharts | M5 (dashboard), parts of M3/M9 |
| **L2 Application** | Services, REST APIs, auth/RBAC, workflow/HITL, import, notifications | FastAPI, SQLAlchemy | M1, M2(import), M3, M10, M11, M12(HITL) |
| **L3 AI** | Agents, skills, FDS, copilot, chatbot logic, orchestration, provider abstraction | Python AI libs, provider SDKs | M6, M7, parts of M9 |
| **L4 Knowledge** | RAG ingestion/retrieval, embeddings, vector store, citation | Chroma/pgvector, embeddings | M8 |
| **L5 Data** | Operational store, audit trail, reference/master data, vectors (prod) | SQLite/PostgreSQL, pgvector | M2(data), M12(audit) |
| **L6 Infrastructure** | Config, secrets, provider switching, logging, monitoring, deploy, security | config.md, .env, CI/CD | M13 |

### 9.3 Cross-layer concerns
- **Security/RBAC** spans L2↔L6; **Audit** spans L2/L3→L5; **HITL** spans L1↔L2; **Provider switching** L6→L3.

---

# 10. Frontend Architecture (L1 — Presentation)

### 10.1 Stack & rationale
- **React + Vite** — fast SPA dev/build; **Tailwind CSS + ShadCN UI** — consistent, accessible component
  system; **Recharts** — Teras 1–7 dashboard charts (bar, stacked, heatmap-style, trends).

### 10.2 Component architecture (text diagram)
```
App (router, auth context, role guard)
├── AuthLayout
│     └── LoginPage (MOE-domain login → AuthService)
└── AppLayout (role-scoped nav)
      ├── DashboardModule (M5)
      │     ├── TerasSummaryCards (DSH-01/03/05/06/07)
      │     ├── KpiByTerasChart (Recharts) (DSH-02/09)
      │     ├── RiskHeatmap / RiskTable (DSH-04/10)
      │     ├── ExecutiveAISummary (DSH-08)
      │     └── KpiMappingTable (DSH-11) + AlignmentIndicator (DSH-12)
      ├── KpiModule (M2/M3)
      │     ├── KpiList / KpiDetail
      │     └── MonthlyUpdateForm (achievement·finance·evidence·remarks)
      ├── FinanceModule (M6) — allocation status · FDS recommendations view
      ├── ChatbotPanel (M9) — cited answers · fallback
      ├── CopilotPanel (M7) — executive insight
      ├── ApprovalsModule (M12) — HITL review/approve queues
      └── AdminModule (M13) — users/roles · knowledge links · config
```

### 10.3 State, data flow & UX rules
- **State:** server state via a data-fetching layer (e.g. React Query-style) over REST; minimal global UI state (auth/role).
- **Role-scoped rendering:** components honour RBAC scope (state/district/sector/own) per BRD §14.
- **HITL UX:** AI outputs shown as **drafts/recommendations** with explicit Approve/Reject; never auto-acted (ASM-11).
- **Citations & fallback:** chatbot/copilot surfaces source citations; renders the fixed fallback string when no answer (BR-025/027).
- **Phasing:** cards/tables first, charts progressively (BR-045).
- **Language:** English primary UI; structure ready for future localisation (NFRQ-012).

### 10.4 Frontend ↔ backend contract
- Communicates only via **REST APIs** (L2, §11/API section); no direct DB/AI access from L1.
- Auth via bearer token/session from AuthService; all calls role-checked server-side.

---

# 11. Backend Architecture (L2 — Application)

### 11.1 Stack & structure
- **Python + FastAPI** (async REST), **SQLAlchemy** ORM (SQLite dev / PostgreSQL prod). Layered modules
  with clear separation: API router → service → repository (ORM) → DB.

### 11.2 Service architecture (text diagram)
```
[FastAPI App]
  ├── Routers (REST endpoints, request/response schemas, RBAC dependency)
  ├── Business Services
  │     ├── AuthService (MOE-domain login, RBAC)        → M1
  │     ├── ImportService (one-time Excel pipeline)     → M2
  │     ├── KpiService (KPI master, PIC, structure)     → M2
  │     ├── UpdateService (monthly update, validation)  → M3/M4
  │     ├── DashboardService (Teras roll-ups)           → M5
  │     ├── FinanceService (allocation, FDS interface)  → M6
  │     ├── AgentOrchestrationService (calls L3)        → M7
  │     ├── KnowledgeService (calls L4 RAG)             → M8
  │     ├── ChatbotService / CopilotService             → M9/M7
  │     ├── ReportService (generation, archive)         → M10
  │     ├── NotificationService (reminders, email queue)→ M11
  │     ├── WorkflowService (HITL approval state machine)→ M12
  │     ├── AuditService (append-only audit writes)     → M12
  │     └── AdminConfigService (users, config, links)   → M13
  ├── Repositories (SQLAlchemy models & queries)        → L5
  └── Integrations (L6): ProviderAdapter, EmailAdapter, LinkFetcher
```

### 11.3 Workflow & HITL (text diagram)
```
AI/agent output ─► [draft] ─► WorkflowService ─► [pending review]
                                   │ human (authorised role)
                          ┌────────┴────────┐
                       Approve            Reject
                          │                  │
                   [approved] ──► action   [returned] ──► revise
                          │ (send email / issue report / formal action)
                          └──► AuditService logs decision + actor + timestamp
```
No formal action executes without passing the HITL gate (BR-015/FRQ-017/ASM-11).

### 11.4 Backend cross-cutting
- **AuthN/AuthZ:** MOE-domain auth; RBAC enforced as a FastAPI dependency on every protected route.
- **Validation:** request schemas (Pydantic) + business validation (completeness, amendment-window).
- **Amendment window:** UpdateService rejects statement/indicator/target edits outside July/October (BR-008).
- **Audit:** AuditService writes append-only entries for all writes and AI/human decisions (BR-009/029).
- **Error envelope:** consistent error responses (detailed in Error Handling section, later part).
- **Provider/config:** services obtain the active LLM provider from L6 abstraction (never hard-coded).

### 11.5 Backend ↔ data/AI/knowledge
- L2 → L5 via SQLAlchemy repositories (operational data + audit).
- L2 → L3 via AgentOrchestrationService (advisory outputs).
- L2 → L4 via KnowledgeService (RAG retrieval, cited).

---

## Self-Review — TRD Part 2

| Check | Finding | Action |
|-------|---------|--------|
| Six-layer principle applied? | AD-008 layers used in §8/§9 and mapped to modules/tech consistently. | OK |
| Diagrams included? | Context, lifecycle, layer stack, FE component tree, BE service map, HITL workflow (text). | OK |
| Stack reflected? | React/Vite/Tailwind/ShadCN/Recharts (L1); FastAPI/SQLAlchemy (L2). | OK |
| Traceable? | Layers/components mapped to RTM modules M1–M13; no orphan components. | OK |
| No new requirements? | Architecture only; all elements trace to existing BRD/RTM. | Confirmed |
| Governance reflected? | HITL workflow, RBAC, audit, amendment-window embedded in L2. | OK |

---

**— END OF PART 2 — (APPROVED 2026-06-27)**
*Part 2 covers: Overall Solution Architecture · Layered System Architecture · Frontend Architecture · Backend Architecture.*

> **Data design rules applied in Part 3 (from frozen baselines):** Excel = initial input only (BR-001/018);
> KPI records live in the operational DB post-import; monthly updates entered in-system by PIC, never via
> monthly Excel (BR-002); knowledge docs/links stored & processed separately (BR-017/019); strict
> Operational vs Knowledge plane separation; dashboard summarises by Teras 1–7 (BR-020); data model supports
> FDS incl. budget status, OBB, Low Cost High Impact & resource-optimisation (BR-010/011/046); audit captures
> KPI/updates/finance/approvals/reports (BR-009/029); amendment control (Jul/Oct) reflected in model +
> workflow (BR-008); **Teras 5–7 availability = Requires User Confirmation (RUC-03), not a blocker.**

---

# 12. Database Architecture (L5 — Data)

### 12.1 DBMS strategy
- **Development:** **SQLite** — zero-config local file DB for fast iteration.
- **Production:** **PostgreSQL** — concurrent, robust, supports **pgvector** (consolidating vector search
  into the prod database).
- **ORM:** **SQLAlchemy** provides a single data-access layer; the same models run on SQLite and
  PostgreSQL, giving **dev→prod portability** with migrations (e.g. Alembic).

### 12.2 Schema strategy
- **Operational schema** (this section) holds all transactional KPI/finance/governance data.
- **Knowledge data** lives on a **separate plane** (§14) — relational metadata + a vector store; it is
  **not** mixed into operational tables.
- **Append-only audit** table is write-once (no updates/deletes) for tamper-evidence (BR-009).
- **Reference/master data** (Teras, object codes, Bahagian, sectors) is seeded and read-mostly.

### 12.3 Integrity, transactions, indexing
- Foreign keys enforce KPI→Teras→Prakarsa hierarchy; transactions wrap multi-row writes (e.g. import, monthly update + audit).
- Indexes on `kpi.code`, `kpi.teras_id`, `monthly_update.(kpi_id, period)`, `finance_allocation.kpi_id`, `audit_log.(entity_type, entity_id)` to support Teras roll-ups and dashboards.
- Amendment-window state enforced at service layer (§16) backed by an `amendment_window` reference table.

### 12.4 Vector store placement
- **Dev:** Chroma (standalone) **or** keyword-search fallback if vectors not yet ready (V1).
- **Prod:** **pgvector** inside PostgreSQL (single managed store) — recommended; Chroma remains an option.

---

# 13. Data Model (L5)

### 13.1 Entity groups
- **Operational core:** Teras, Strategi/Enabler, Prakarsa, KPI, Activity, PIC, MonthlyUpdate, Evidence.
- **Finance / FDS:** FinanceAllocation, ObjectCode, Recommendation (LCHI/Intervention/Resource-Opt/OBB), RiskAssessment, AlignmentScore.
- **Governance / Audit:** AmendmentWindow, KpiAmendment, AuditLog, ApprovalRecord, Report, Notification.
- **Access:** User, Role.
- **Reference/master:** Bahagian, Sector, ObjectCode.
- **Knowledge plane (separate, §14):** KnowledgeSource, LinkRegistry, DocumentChunk, Embedding(vector store).
- **Infrastructure:** ProviderConfig.

### 13.2 Entity-relationship (text diagram — operational plane)
```
Teras (1..7) ──< Strategi/Enabler ──< Prakarsa ──< KPI ──< Activity
                                                   │         │
                                                   │         └──< FinanceAllocation >── ObjectCode
                                                   │                   (OS21000…OS42000, status, monthly Jan–Dec)
                              PIC >──assigned──────┤
                              (name,email,sector)  ├──< MonthlyUpdate ──< Evidence
                                                   │       (period, achievement, finance_status, remarks)
                                                   ├──< RiskAssessment (period, risk_level, method)
                                                   ├──< AlignmentScore (rpm_ref, strength)
                                                   ├──< Recommendation (type: LCHI|Intervention|ResourceOpt|OBB,
                                                   │                     content, rationale, priority, status)
                                                   └──< KpiAmendment >── AmendmentWindow (year, Jul|Oct, open)

User >──has──< Role         ApprovalRecord (item_type,item_id,decision,actor,ts)   ← HITL (§11.3)
Report (period,type,status,approved_by)     Notification (type,recipient,status,approved_by,sent_at)
AuditLog (entity_type, entity_id, action, actor, timestamp, before, after, reason)   ← append-only
```

### 13.3 Key entities & fields (selected)
| Entity | Key fields | Notes / rules |
|--------|-----------|---------------|
| **KPI** | id, code (`TSx.Sy.Pz.KPIn`), teras_id, prakarsa_id, statement, indicator, tov, tov_type (value/"KPI Baharu"), target_2026, keberhasilan, bahagian, sector, pic_id, quick_win, year_assigned, status, risk_level, alignment_score | statement/indicator/target are **amendment-controlled** (BR-008); status/risk derived | 
| **PIC** | id, name, email, sector | mandatory per KPI (BR-004) |
| **MonthlyUpdate** | id, kpi_id, period (YYYY-MM), achievement, finance_status, evidence_ref, remarks, submitted_by, submitted_at | **in-system entry only** (BR-002); one per KPI per period |
| **FinanceAllocation** | id, kpi_id, object_code, amount, allocation_status {received, will be received, pending, not received, not required, insufficient}, warrant, expenditure, frequency, jan…dec, jumlah | six-value status (BR-010); supports FDS |
| **Recommendation** | id, kpi_id/activity_id, type, content, rationale, priority, status, reviewed_by | FDS outputs; advisory + HITL (BR-046/015) |
| **RiskAssessment** | id, kpi_id, period, risk_level, method | rule-based initially (TASM-07) |
| **AlignmentScore** | id, kpi_id, rpm_ref, strength, computed_at | KPI–RPM alignment (BR-012) |
| **KpiAmendment** | id, kpi_id, field, old_value, new_value, window_id, actor, timestamp, reason | only in Jul/Oct (BR-008); audited |
| **AuditLog** | id, entity_type, entity_id, action, actor, timestamp, before, after, reason | append-only (BR-009/029) |
| **User / Role** | id, email, name, role, scope; role, permissions | MOE-domain (BR-003), RBAC (BR-031/032) |
| **Report / Notification** | id, …, status (draft/approved/sent), approved_by | HITL before issue/send (BR-015/040) |

### 13.4 Dashboard support (Teras 1–7)
The model enables Teras roll-ups (DSH-01…12): aggregate `KPI` by `teras_id` joined to `MonthlyUpdate`
(achievement/submission), `RiskAssessment` (risk), `FinanceAllocation` (budget), `AlignmentScore`
(alignment), `Recommendation` (Low Cost High Impact). Reference `Teras` always carries the 1–7 set even
where data is partial (see RUC-03).

---

# 14. Operational vs Knowledge Data — Dual Plane (L5 ↔ L4)

The platform enforces **two strictly separate data planes** (BR-017/AD-004). No record crosses planes.

### 14.1 Dual-plane diagram (text)
```
┌────────────────────────── OPERATIONAL PLANE (L5) ──────────────────────────┐
│  SQLite (dev) / PostgreSQL (prod)                                           │
│  KPI · Teras/Strategi/Prakarsa · PIC · Activity · MonthlyUpdate · Evidence  │
│  FinanceAllocation · Recommendation · RiskAssessment · AlignmentScore       │
│  AmendmentWindow · KpiAmendment · AuditLog · ApprovalRecord · Report ·       │
│  Notification · User · Role · reference/master data                         │
│  → System of record · transactional · audit-grade · import-once source      │
└─────────────────────────────────────────────────────────────────────────── ┘
                         ▲ (IDs/links only for citation context; no doc text stored as KPI data)
┌────────────────────────── KNOWLEDGE PLANE (L4) ────────────────────────────┐
│  Knowledge Repository (metadata) + Vector Store (Chroma dev / pgvector prod)│
│  KnowledgeSource (static docs) · LinkRegistry (live links) ·                │
│  DocumentChunk · Embedding                                                  │
│  → RAG retrieval source · chunked/embedded · admin-validated · cited        │
└─────────────────────────────────────────────────────────────────────────── ┘
```

### 14.2 Plane rules
- **Operational data** (Pelan Taktikal-derived KPI/finance/governance) → operational DB only.
- **Knowledge data** (RPM 2026–2035, guidelines, circulars, notes, **live links**) → knowledge plane only,
  ingested via RAG; **never** treated as KPI input (BR-019).
- **Live links** are **administrator-validated** before use (BR-024/Q-022 resolution).
- **No cross-contamination:** the chatbot/copilot may *cite* knowledge alongside operational figures at
  query time, but the two stores remain physically/logically separate (NFRQ-010).
- In production, pgvector may co-reside in PostgreSQL but in a **separate schema/namespace** from
  operational tables to preserve the logical boundary.

---

# 15. Data Ingestion & Import Pipeline (one-time) (L2 → L5)

Realises FRQ-003 / INTQ-001 / DATQ-001 via the **Data Integration Agent** + Excel-parsing skill.
**Excel is initial input only** (BR-001/018); the pipeline runs at onboarding, then the DB is authoritative.

### 15.1 Import flow (text diagram)
```
[Admin uploads Pelan Taktikal JPN/PPD .xlsx]
        │
        ▼
[ImportService] → [Data Integration Agent: parse per Teras sheet]
        │   extract: Teras, Strategi/Enabler, Prakarsa, KPI(code, TOV, target,
        │            activities, Bahagian/PIC, OS object codes, monthly Jan–Dec)
        ▼
[Validation Agent: structure + completeness]
        │   ├─ valid rows → staged
        │   └─ issues → import report (missing PIC/sector/email/target → warnings)
        ▼
[Map to entities] → Teras/Strategi/Prakarsa/KPI/Activity/FinanceAllocation/PIC
        ▼
[Write to Operational DB] (transactional) + [AuditLog: import batch]
        ▼
[Import-once lock] → further changes go through in-system workflow (no re-upload as working source)
```

### 15.2 Import rules
- **Import-once:** subsequent monthly changes are **in-system only** (BR-002); re-import is an admin-only,
  audited exception, not the monthly path.
- **Completeness at import:** missing mandatory fields raise warnings (BR-005/006) surfaced per KPI/Teras.
- **Idempotency & traceability:** each import is a batch with an audit entry; KPI `code` is the natural key.
- **Teras 5–7:** the JPN working file contains Teras 1&2 and 3&4 sheets; **Teras 5–7 source data is a known
  follow-up — RUC-03 (Requires User Confirmation), not a blocker.** The model already supports all 7 Teras.

---

# 16. Monthly KPI Workflow (L2 → L5)

Realises FRQ-007/010/024; the recurring operational backbone. **PICs key updates in-system; no monthly
Excel uploads** (BR-002).

### 16.1 Monthly update flow (text diagram)
```
[PIC login: @moe.gov.my / @moe-dl.edu.my] → RBAC (own KPIs)
        ▼
[Open KPI → MonthlyUpdateForm for current period]
        │  enter: achievement · finance_status(6-value) · evidence · remarks
        ▼
[UpdateService: validate completeness + period rules]
        ▼
[Save] → MonthlyUpdate + Evidence (operational DB)  →  [AuditLog: who/what/when]
        ▼
[Recompute] KPI status (KPI Analysis) · RiskAssessment (Risk) · FinanceAllocation roll-up
        ▼
[Dashboard refresh] (Teras 1–7)   +   [Submission tracking] (DSH-06)
        ▼
[If gaps/late] → Notification Agent drafts reminder → HITL approve → send (audited)
```

### 16.2 Amendment-window control (text diagram)
```
Edit request on KPI.statement / indicator / target
        ▼
[UpdateService checks AmendmentWindow]
   ├─ month ∈ {July, October} & window open → allow → KpiAmendment(old,new,reason) + AuditLog
   └─ otherwise → REJECT ("amendments allowed only in July/October", BR-008)
Routine monthly fields (achievement, finance, evidence, remarks) are editable any month.
```

### 16.3 Workflow rules
- Monthly fields editable each period; **definitional fields (statement/indicator/target) locked except Jul/Oct** (BR-008).
- Every save is **audited** (BR-009); amendments capture before/after + reason (BR-036).
- AI status/risk/FDS outputs are **advisory**; any formal action (report/email/intervention) passes the
  **HITL gate** (BR-015/ASM-11) before execution.
- Finance status uses the **six-value vocabulary**; feeds FDS (Budget Intelligence, Low Cost High Impact, OBB).

---

## Self-Review — TRD Part 3

| Check | Finding | Action |
|-------|---------|--------|
| 10 data rules applied? | All reflected: import-once, in-system updates, dual plane, FDS data, audit scope, amendment control, Teras 1–7 roll-up, Teras 5–7 = RUC-03. | OK |
| Entity diagrams included? | ER (operational), dual-plane, import flow, monthly + amendment-window diagrams (text). | OK |
| Plane separation explicit? | §14 defines two planes, no cross-contamination, pgvector separate schema. | OK |
| FDS data supported? | FinanceAllocation, Recommendation (LCHI/Intervention/ResourceOpt/OBB), RiskAssessment in model. | OK |
| Traceable / no new requirements? | Entities map to RTM DB entities; all trace to BRD/RTM; nothing new added. | OK |
| Teras 5–7 handled? | Recorded as RUC-03 in §15.2; model supports all 7 Teras. | OK |

---

**— END OF PART 3 — (APPROVED 2026-06-27)**
*Part 3 covers: Database Architecture · Data Model · Operational vs Knowledge Dual Plane · Data Ingestion & Import Pipeline · Monthly KPI Workflow.*

> **AI design rules applied in Part 4 (from frozen baselines):** capability-driven architecture, not fixed
> by agent count (BR-041); AI advisory only + human review for official decisions (BR-015/028/ASM-11);
> provider abstracted via `config.md` + `.env` (BR-044); Groq (dev) / OpenAI·Anthropic (prod); skills are
> reusable, not separate agents (BR-042); RAG uses RPM 2026–2035 as main reference plus supporting docs &
> live links (BR-012/023); chatbot grounded in KPI data + knowledge, with honest fallback (BR-025/027);
> FDS is a top-level AI capability incl. Low Cost High Impact (BR-046); Executive Copilot synthesises KPI/
> Risk/FDS/RAG/Report/Notification; all AI output logged (BR-029); no agent approves/amends/deletes/sends
> without human approval (BR-015/ASM-11).

---

# 17. AI Architecture (L3)

The AI layer is **capability-driven**: capabilities (BCM) and rules are the stable contract; the agent set
realises them and **may evolve without changing the architecture** (BR-041). All AI is **advisory**;
formal actions pass the HITL gate (L2 WorkflowService). The provider is **abstracted** and config-selected.

### 17.1 AI layer architecture (text diagram)
```
            ┌──────────────────────── L3 AI LAYER ────────────────────────────┐
 L2 calls → │  AI Orchestration (request routing, context assembly, logging)   │
            │        │                                   │                      │
            │        ▼                                   ▼                      │
            │  Multi-Agent Set ───uses──► Skills Layer (reusable capabilities)  │
            │  (capability-driven)        (validation, scoring, retrieval,      │
            │                              drafting, roll-up, audit, HITL gate) │
            │        │ grounding                                                │
            │        ▼                                                          │
            │  Provider Abstraction ──► [Groq | OpenAI | Anthropic] (per config)│
            └───────────────┬───────────────────────────────┬──────────────────┘
                            ▼ (grounding via L4)             ▼ (advisory outputs)
                     RAG / Knowledge (L4)            HITL gate (L2) → action / audit (L5)
```

### 17.2 Provider abstraction — separate LLM and Embedding providers (text diagram)
The **LLM provider** and the **Embedding provider** are **independent** (a key refinement: Groq has no
embeddings API). The Provider Adapter exposes two independent operations: **`chat()`** and **`embedding()`**.
```
config.md (mode, llm_provider, llm_model, embedding_provider, embedding_model)   .env (API keys)
        └───────────────────────────────┬───────────────────────────────────────┘
                                         ▼
                            [ProviderAdapter interface]
                      ┌──────────────────┴───────────────────┐
                 chat()                                   embedding()
            ┌───────┼─────────┐                    ┌──────────┴───────────┐
            ▼       ▼         ▼                     ▼                      ▼
        Groq    OpenAI   Anthropic            Local SentenceTransformer  OpenAI Embeddings
        (dev)   (prod)   (prod)               (dev option)               (dev option / prod)
  Switching either provider = config change only; NO code change (BR-044/TR-003/AD-001).
```
**Approved provider matrix:**
| Environment | LLM (`chat()`) | Embeddings (`embedding()`) |
|-------------|----------------|-----------------------------|
| Development | **Groq** | **Local Sentence Transformer** or **OpenAI Embeddings** |
| Production / Golive | **OpenAI or Anthropic** | **OpenAI Embeddings** (or another approved provider) |

> This LLM/Embedding separation is reflected in both the AI Architecture (here) and the RAG Architecture (§20.3).

### 17.3 AI governance
- **Advisory-only:** agents output drafts/recommendations; **no approve/amend/delete/send** without human approval (BR-015/ASM-11).
- **Logging:** every AI request/response and human decision is logged for traceability/audit (BR-029) via AuditService (L5).
- **Grounding & honesty:** knowledge answers are cited; honest fallback when unavailable (BR-025/027).

### 17.4 AI Provider Strategy
- **Provider abstraction:** business logic depends only on the `ProviderAdapter` interface (`chat()`,
  `embedding()`) — never a concrete vendor (BR-044/AD-001). LLM and embedding providers are independent (§17.2).
- **Provider selection:** chosen per environment via `config.md` (+ keys in `.env`): dev LLM=Groq,
  embeddings=local/OpenAI; prod LLM=OpenAI/Anthropic, embeddings=OpenAI (or approved).
- **Provider failover:** on provider error/outage, the adapter applies retry-with-backoff and may fail over
  to a configured secondary provider of the same kind; failures are logged (BR-029); on total failure the
  system returns a safe error / fixed fallback — **never fabricated output**.
- **Cost optimisation:** prefer the configured cost-appropriate model per task (e.g. smaller models for
  classification/summarisation, larger only where needed); cache stable AI summaries; batch embeddings;
  cap tokens. Cost/model choices are configuration, not code.
- **Provider-agnostic guarantee:** adding/replacing a provider requires only an adapter implementation +
  config change; no change to agents, skills or business logic.

### 17.5 Agent orchestration framework (V1)
- **V1 uses a custom Agent Orchestrator** (lightweight, in-house) — **no mandatory dependency** on
  LangChain, LlamaIndex or any orchestration framework.
- Rationale: minimal dependencies, full control over HITL gating and audit logging, easier government
  review. **Future versions may migrate** to a specialised orchestration framework if required (documented
  as a future enhancement); the capability-driven design (BR-041) makes this non-breaking.

---

# 18. Multi-Agent Architecture (L3)

Capability-driven agents; the current primary set is below (count may evolve, BR-041). Agents are
orchestrated; world-affecting outputs route to the HITL gate.

### 18.1 Agent orchestration (text diagram)
```
[Trigger: monthly update / schedule / user request]
        ▼
[AI Orchestration] assembles context (operational data L5 + knowledge L4)
        ▼  (advisory pipeline)
 Validation ─► KPI Analysis ─► Risk ─► Financial Monitoring ─► Budget Intelligence(FDS)
                                          │                         │
                                          ▼                         ▼
                                   Intervention(FDS)          Low Cost High Impact(FDS)
        ▼
 Knowledge Alignment   Notification(draft)   Report Generation(draft)   AI Summary
        ▼                      ▼                       ▼
   (display)           HITL gate (L2) ───approve───► send/issue ──► AuditLog (L5)
                              └───reject──► revise
 Audit Agent: logs every agent output + decision (cross-cutting)
```

### 18.2 Current primary agents (capability-driven; not a fixed cap)
| Agent | Capability | Advisory output | Human review |
|-------|-----------|-----------------|:------------:|
| Data Integration | CAP-K1 | structured records | No (admin verifies) |
| Validation/Completeness | CAP-M2 | warnings | No |
| KPI Analysis | CAP-AI1 | status | No |
| Risk | CAP-AI2 | risk ratings | No (Yes if acts) |
| Financial Monitoring | CAP-B1 | budget status | No |
| Budget Intelligence (FDS) | CAP-B2/B5 | LCHI/OBB recommendations | **Yes** |
| Intervention (FDS) | CAP-AI3 | intervention drafts | **Yes** |
| Notification & Reminder | CAP-N1/N2 | draft emails | **Yes (send)** |
| Audit | CAP-G2 | audit entries | n/a |
| Report Generation | CAP-R1 | report drafts | **Yes** |
| KPI Chatbot | CAP-AI4 | cited answers | No |
| Knowledge Alignment | CAP-AI5 | alignment scores | No |
| Executive Copilot | CAP-AI6 | executive insight | Yes (before acting) |
| AI Summary | CAP-AI7 | dashboard summary | No |

> Adding/removing/merging agents does not change the business architecture (capabilities + rules are the contract).

---

# 19. Skills Architecture (L3)

**Skills are reusable capabilities** invoked by multiple agents — **not counted as agents** (BR-042).
A Skill Registry exposes deterministic, independently-testable functions.

### 19.1 Agent ↔ Skill binding (text diagram)
```
SKILL REGISTRY (reusable)                used by AGENTS
─────────────────────────────────────   ──────────────────────────────
excel_parsing ........................   Data Integration
completeness_validation ..............   Validation, KPI Analysis
kpi_status_classification ............   KPI Analysis, AI Summary
risk_scoring .........................   Risk, AI Summary, Intervention
budget_status_classification (6-value)   Financial Monitoring, Budget Intelligence
low_cost_high_impact_scoring .........   Budget Intelligence, Intervention
obb_value_for_money ..................   Budget Intelligence
teras_aggregation ....................   AI Summary, Dashboard, KPI Analysis
rag_retrieval_and_citation ...........   Chatbot, Knowledge Alignment, Executive Copilot
link_fetch_refresh ...................   (knowledge ingestion)
alignment_scoring ....................   Knowledge Alignment
email_notification_drafting ..........   Notification, Report Generation
report_templating ....................   Report Generation
audit_logging ........................   Audit (all action agents)
hitl_gating ..........................   all action-taking agents
```

### 19.2 Skill principles
- **Reusable & composable:** one skill serves many agents; agents orchestrate, skills compute.
- **Deterministic where possible & independently testable** (supports the testing strategy).
- **Versioned:** skill changes are tracked; agents bind to skill interfaces, not implementations.

---

# 20. RAG / Knowledge Architecture (L4)

RAG grounds AI answers in **RPM 2026–2035 (main reference)** plus **supporting documents** and
**administrator-validated live links** (BR-012/023/024). Vector search via **Chroma (dev)/pgvector (prod)**
with a **keyword-search fallback** for V1.

### 20.1 RAG pipeline (text diagram)
```
INGEST                          INDEX                      RETRIEVE & GROUND
[RPM 2026–2035 (main)]          chunk → embed →            query → retrieve top-k →
[Supporting docs] ───────────►  [Vector Store]   ───────►  assemble context (cited) →
[Live links (admin-validated)]  (Chroma/pgvector)          LLM (via provider abstraction) →
   │ LinkRegistry: title,                                  cited answer
   │ url, category, last_checked                           │
   └─ refresh (admin)            keyword-search fallback ◄──┘ (if vectors not ready / V1)
   If a source is inaccessible → clear message (never guess, BR-026)
   If no grounding found → fixed fallback string (BR-027)
```

### 20.2 RAG rules
- **Main reference:** RPM 2026–2035 always in the knowledge corpus (BR-012).
- **Sources:** uploaded documents + live links; live links **admin-validated** before use (BR-024/Q-022).
- **Citation:** retrieved sources are cited in answers (BR-025).
- **Fallback:** `"I cannot find this information in the available KPI data or knowledge sources."` (BR-027).
- **Separation:** knowledge plane only; never mixed with operational data (BR-017/019).

### 20.3 Embeddings & Vectorisation (independent of the LLM provider)
The **embedding provider is separate from the LLM provider** (§17.2). The RAG pipeline calls the Provider
Adapter's **`embedding()`** operation for both ingestion (chunk embedding) and query embedding.
| Environment | Embedding provider | Vector store |
|-------------|--------------------|--------------|
| Development | **Local Sentence Transformer** or **OpenAI Embeddings** (config) | Chroma, **or keyword-search fallback** for V1 |
| Production | **OpenAI Embeddings** (or another approved provider) | **pgvector** in PostgreSQL (separate schema) |
- **V1 fallback:** if vector search is not ready, keyword search serves retrieval (TR-012); embeddings can
  be enabled later without architectural change.
- **Re-indexing:** documents/links re-embedded on change/refresh; ingestion is idempotent.
- **Consistency:** the same embedding model must be used for a given index (re-embed on model change).

---

# 21. Financial Decision Support (FDS) Architecture (L3 — top-level AI capability)

**FDS is a top-level AI capability** (BR-046), not a sub-feature. It is realised by the Budget Intelligence
and Intervention agents + finance skills, surfaced via Dashboard and Executive Copilot.

### 21.1 FDS architecture (text diagram)
```
                         ┌──────────────── FDS (top-level) ────────────────┐
 Operational data (L5):  │  1) Budget Intelligence                          │
  FinanceAllocation,     │       budget status · funding-gap · budget-risk  │
  KPI, RiskAssessment ──►│  2) Low Cost High Impact Analysis                │──► Recommendations
                         │       activities · expected impact · alternatives│    (advisory)
 Knowledge (L4): RPM,    │       · resource optimisation · collaboration    │     │
  guidelines ───────────►│  3) Intervention Recommendation                  │     ▼
                         │       alt. programmes · strategies · prioritise  │  HITL gate (L2)
                         │  4) Executive Financial Insight                  │     │
                         │       recommendations + rationale ──────────────►│──► Dashboard (DSH-05/08)
                         └──────────────────────────────────────────────────┘    Executive Copilot (§23)
   Resource-optimisation strategies: collaboration · programme consolidation ·
   shared resources · digital alternatives · other low-cost high-impact approaches.
```

### 21.2 FDS rules
- Components: Budget Intelligence, **Low Cost High Impact Analysis**, Intervention, Executive Financial Insight (+ resource optimisation).
- All FDS outputs **advisory**; require human review before implementation (BR-037/046/ASM-11).
- OBB value-for-money assessed within FDS (BR-038); method = Technical Assumption (TASM-08).
- All FDS recommendations logged (BR-029) and traceable to KPI/finance entities.

---

# 22. KPI Chatbot Architecture (L3 ↔ L4)

### 22.1 Grounding flow (text diagram)
```
[User question] → ChatbotService
        ▼ grounding order (BR-013/AIR-070):
   1) KPI database (operational, role-scoped)
   2) Monthly updates
   3) Uploaded knowledge documents (RAG)
   4) RPM 2026–2035 (RAG)
   5) Live links (RAG, admin-validated)
        ▼
   [Assemble cited context] → Provider Abstraction → LLM → answer + citations
        ▼
   If nothing found → fixed fallback string (BR-027)
   Inaccessible source → clear message, never guess (BR-026)
        ▼  (log Q&A + sources for audit, BR-029)
```

### 22.2 Chatbot rules
- Answers **grounded** in KPI data + knowledge; **role-scoped** (a user sees only permitted KPI data).
- **Cites sources**; informational only (no formal action) — no approval needed to answer, but cannot act.

---

# 23. Executive Copilot Architecture (L3)

The Executive Copilot synthesises **operational + knowledge signals** for leadership; advisory, reviewed
before acting (BR-043/015/ASM-11).

### 23.1 Copilot synthesis (text diagram)
```
   INPUTS (per rule 13)                       EXECUTIVE COPILOT
 ┌─ KPI module (status, Teras roll-up) ─┐
 ├─ Risk module (at-risk/critical) ─────┤
 ├─ FDS (budget, LCHI, financial insight)│──► [synthesise + ground via RAG]
 ├─ RAG (RPM, guidelines, links) ───────┤        │
 ├─ Report module (monthly outputs) ────┤        ▼
 └─ Notification module (gaps/alerts) ──┘   Executive insight + rationale (cited)
                                                  │
                                            (advisory) → management decision (human)
                                                  │
                                            feeds Dashboard exec summary (DSH-08); logged (BR-029)
```

### 23.2 Copilot rules
- Consumes outputs from **KPI, Risk, FDS, RAG, Report and Notification** modules (rule 13).
- Provides **recommendations + rationale**; **final approval remains with authorised officers** (ASM-11).
- All interactions logged for audit/traceability (BR-029).

---

## Self-Review — TRD Part 4

| Check | Finding | Action |
|-------|---------|--------|
| Capability-driven (not agent-count)? | §17/§18 state capabilities+rules are the contract; agents may evolve. | OK |
| Advisory + HITL everywhere? | §17.3, §18 orchestration, §21/§22/§23 all route formal actions to HITL. | OK |
| Provider abstraction (config.md/.env)? | §17.2 diagram; Groq dev / OpenAI·Anthropic prod. | OK |
| Skills reusable, not agents? | §19 registry + binding; explicitly not counted as agents. | OK |
| RAG: RPM main + docs + live links + fallback? | §20 pipeline + rules; citation + fallback string. | OK |
| FDS top-level incl. Low Cost High Impact? | §21 top-level capability, 4 components + resource-opt. | OK |
| Copilot uses KPI/Risk/FDS/RAG/Report/Notification? | §23 inputs diagram per rule 13. | OK |
| AI output logged; no agent acts alone? | §17.3/§18 logging + HITL; rules 14/15 honoured. | OK |
| Diagrams included? | AI layer, provider abstraction, orchestration, skills, RAG, FDS, chatbot, copilot (text). | OK |
| No new requirements? | Maps to existing BRD/RTM AIRQ/FRQ/BR; nothing new. | Confirmed |

---

**— END OF PART 4 — (APPROVED 2026-06-27)**
*Part 4 covers: AI Architecture · Multi-Agent · Skills · RAG/Knowledge · FDS · KPI Chatbot · Executive Copilot.*

---

# 24. Dashboard Architecture (L1 ↔ L2)

The Teras 1–7 dashboard (BR-020) is served by **DashboardService** (L2) aggregating operational data and
AI outputs; rendered with **Recharts** (L1). Charts may be phased (cards/tables first, BR-045).

### 24.1 Dashboard service (text diagram)
```
[L1 Dashboard UI] ──REST──► [DashboardService (L2)]
                                 ├─ KPI summary by Teras 1–7      (KPI + MonthlyUpdate roll-up)
                                 ├─ Achievement summary           (status classification)
                                 ├─ Risk summary                  (RiskAssessment)
                                 ├─ Budget status summary         (FinanceAllocation, 6-value)
                                 ├─ Financial Decision Support summary (FDS recommendations)
                                 ├─ Submission summary            (MonthlyUpdate by period)
                                 ├─ Missing information summary   (completeness flags)
                                 ├─ Alignment strength            (AlignmentScore)
                                 ├─ Executive summary             (Executive Copilot / Exec Financial Insight)
                                 └─ AI-generated insights         (AI Summary Agent — 7 questions)
   Aggregations roll up by teras_id; role-scoped; drill-down Teras → KPI → detail.
```

### 24.2 Dashboard rules
- Backend services support all required summaries (rule 4): KPI-by-Teras, FDS, budget, risk, executive, AI insights.
- Role-scoped per RBAC (§25); reads operational DB + cached AI outputs; no AI auto-actions.
- Components map to DSH-01…12 (BRD §15).

---

# 25. Authentication & Role-Based Access Control (L2/L6)

### 25.1 Auth & RBAC flow (text diagram)
```
[User] → Login (email) → [AuthService]
     ├─ domain check: email ∈ {@moe.gov.my, @moe-dl.edu.my} ? else REJECT (BR-003)
     ├─ identity verification (SSO vs email-verification — TASM-09 / Q-015)
     └─ issue session/token (role + scope)
[Every protected API] → RBAC dependency → check role+scope → allow/deny → audit (login/logout, BR-029)
```

### 25.2 Auth/RBAC rules
- **Only** `@moe.gov.my` / `@moe-dl.edu.my` accounts (BR-003); RBAC applied **consistently across all modules** (rule 1).
- Roles & scopes per BRD §14 (Super Admin, JPN/Sector/PPD Admin, PIC, Finance, Executive, Read-only, Audit).
- Enforcement is **server-side** (FastAPI dependency) on every route; UI scoping is convenience only.
- Login/logout events audited (§31).

### 25.3 JWT-based authentication (default implementation)
**JWT is the default auth mechanism.** Single Sign-On (SSO) is a **future enhancement** (not V1).
| Element | Specification |
|---------|---------------|
| **Access Token** | Short-lived JWT (e.g. ~15 min) carrying user id, role, scope; sent as `Authorization: Bearer`. |
| **Refresh Token** | Longer-lived (e.g. ~7 days), HttpOnly secure cookie; used to mint new access tokens; revocable. |
| **Token Expiry** | Access expires quickly; refresh rotates; logout invalidates refresh; expiry configurable per environment. |
| **CORS** | Restrict allowed origins to the approved SPA origin(s) per environment; credentials only for trusted origins. |
| **CSRF** | For cookie-based refresh, apply CSRF protection (e.g. double-submit token / SameSite=strict). |
| **HTTPS** | **Required in production** (transport security); tokens never sent over plain HTTP. |
- **SSO (future):** the design allows replacing the credential step with MOE SSO/IdP without changing RBAC.
- Identity-mechanism assumption TASM-09 is hereby resolved to **JWT default; SSO future**.

---

# 26. API Architecture (L2)

### 26.1 Principles
- RESTful FastAPI; resource-oriented endpoints; Pydantic request/response schemas; **RBAC dependency** on every protected route; consistent **error envelope** (§34); **versioned** (`/api/v1`).

### 26.2 Service/endpoint catalogue (selected, → RTM modules)
| Service | Example endpoints | Module |
|---------|-------------------|--------|
| AuthService | `POST /auth/login`, `POST /auth/logout`, `GET /me` | M1 |
| ImportService | `POST /import/pelan-taktikal` | M2 |
| KpiService | `GET/POST/PUT /kpis`, `GET /kpis/{id}` | M2 |
| UpdateService | `POST /kpis/{id}/monthly-updates` | M3 |
| ValidationService | `GET /kpis/{id}/completeness` | M4 |
| DashboardService | `GET /dashboard/teras`, `GET /dashboard/summary` | M5 |
| FinanceService | `GET/POST /kpis/{id}/finance`, `GET /fds/recommendations` | M6 |
| AgentService | `POST /ai/analyze`, `POST /ai/recommend` | M7 |
| KnowledgeService | `POST /knowledge/sources`, `POST /knowledge/links`, `POST /knowledge/refresh` | M8 |
| ChatbotService | `POST /chatbot/query` | M9 |
| CopilotService | `POST /copilot/insight` | M7 |
| ReportService | `POST /reports/generate`, `GET /reports` | M10 |
| NotificationService | `POST /notifications`, `GET /notifications/queue` | M11 |
| WorkflowService | `POST /approvals/{id}/approve|reject` | M12 |
| AuditService | `GET /audit` (read, scoped) | M12 |
| AdminConfigService | `GET/PUT /admin/config`, `GET/POST /admin/users` | M13 |

### 26.3 API rules
- All AI/finance/report/notification **actions** return **drafts**; execution only after HITL approval (BR-015).
- No endpoint lets an agent approve/amend/delete/send official outputs without human approval (rule 15 / ASM-11).

---

# 27. Configuration Strategy (L6 → L3)

### 27.1 Config & provider switching (text diagram)
```
config.md (declarative)                         .env (secrets only)
  mode: dev | prod                              GROQ_API_KEY=...
  provider: groq | openai | anthropic           OPENAI_API_KEY=...
  model: <model-id>                             ANTHROPIC_API_KEY=...
        │                                       (NEVER commit .env)
        ▼
 [Config Loader] → [ProviderAdapter] → selects client at runtime
        dev → Groq        prod/golive → OpenAI or Anthropic
 Business logic depends ONLY on ProviderAdapter interface (never a concrete provider). (BR-044/AD-001)
```

### 27.2 Environment-specific configuration profiles
The configuration strategy supports **per-environment profiles**, selected by `mode`:
| Profile | LLM | Embeddings | DB | Vector | Notes |
|---------|-----|-----------|----|--------|-------|
| **development** | Groq | Local ST / OpenAI | SQLite | Chroma / keyword fallback | local; verbose logging |
| **testing** | Groq (or mock) | mock/local | SQLite (test) | in-memory / keyword | CI test profile; deterministic mocks |
| **production** | OpenAI / Anthropic | OpenAI (approved) | PostgreSQL | pgvector | HTTPS; secrets manager; at-rest encryption |
- **`config.md` remains the primary business configuration reference**; profiles are declarative settings,
  secrets stay in `.env` (per-environment).

### 27.3 Configuration rules
- AI providers configured **only** via `config.md` (rule 2); **API keys only in `.env`** (rule 2).
- **Dev = Groq; Prod/Golive = OpenAI or Anthropic** (BR-044); embedding provider configured independently (§17.2).
- **Business logic must never depend directly on a specific provider** — provider-agnostic via the adapter.
- Configuration changes are **audited** (§31; rule 5).

---

# 28. Environment Configuration (.env) (L6)

- `.env` holds **secrets/keys** (LLM provider keys, DB URL, SMTP creds, session secret); excluded from VCS (`.gitignore`); a committed **`.env.example`** documents required vars without values.
- Separate `.env` per environment (dev/prod); production secrets via a secrets manager where available.
- Non-secret, declarative settings (mode/provider/model) live in `config.md`; secrets never in `config.md`.

---

# 29. Integration Architecture (L6/L2)

| Integration | Direction | Notes | RTM |
|-------------|-----------|-------|-----|
| Excel import | inbound (one-time) | Pelan Taktikal .xlsx → import pipeline | INTQ-001 |
| Live knowledge links | inbound (admin-validated) | fetched/refreshed for RAG | INTQ-002 |
| Email/SMTP | outbound | approved notifications/reports only | INTQ-003 |
| LLM provider APIs | outbound | Groq/OpenAI/Anthropic via adapter | INTQ-004 |
| SharePoint / doc source | inbound (future) | additional knowledge source | INTQ-005 (Future) |

All outbound actions that affect the world (email) are **HITL-gated**; external fetches (links) are admin-validated (BR-024).

---

# 30. Notification & Email Architecture (L2)

### 30.1 Notification engine (text diagram)
```
[Triggers] monthly-reminder · missing-info · approval · monthly-report · escalation(overdue)
        ▼
[Notification Agent drafts content] → [WorkflowService: HITL approve] (BR-015)
        ▼ approved
[Email Queue] ──send──► SMTP ──► recipient
   │ retry on failure (backoff); status: queued→sent→failed→retry
   └─ delivery logged (BR-029; rule 5)
 Channel abstraction: email now; future channels (SMS/in-app) pluggable (rule 3).
```

### 30.2 Notification rules (rule 3)
- Supports: monthly update reminders, missing-information reminders, approval notifications, monthly report
  notifications, **escalation for overdue updates**, **email queue with retry**, and **future channels**.
- Nothing sends without human approval (BR-015/040); all deliveries logged.

---

# 31. Audit Trail & Version History (L5)

### 31.1 Audited events (rule 5)
User **login/logout**; KPI updates; financial updates; AI recommendations; human approvals; report
generation; notification delivery; configuration changes; KPI amendments (before/after + reason).

### 31.2 Audit design
- **Append-only** `AuditLog` (no update/delete) — tamper-evident (BR-009/029); `(entity_type, entity_id, action, actor, timestamp, before, after, reason)`.
- **Version history:** KPI amendments tracked via `KpiAmendment` (Jul/Oct only, BR-008); reports/notifications carry status history.
- Audit is **queryable** by Internal Audit / oversight (BR-030), role-scoped.

---

# 32. Security Architecture (L6)

| Control | Approach | Rule |
|---------|----------|------|
| Authentication | MOE-domain login (BR-003) | rule 6 |
| Authorisation | RBAC, server-side, all modules | rule 6 |
| API protection | auth on every route, RBAC, schema validation | rule 6 |
| Secret management | `.env` / secrets manager; never in code/`config.md` | rule 6 |
| Audit logging | append-only audit (§31) | rule 6 |
| Input validation | Pydantic + business validation (incl. completeness, amendment window) | rule 6 |
| Rate limiting | per-user/IP throttling on APIs (esp. auth, AI, chatbot) | rule 6 |
| Transport | **HTTPS assumed for production** | rule 6 |
| **Encryption at rest (prod)** | **Sensitive data must be encrypted at rest in production** (DB/storage-level encryption; encrypted backups; secrets in a managed store). | NFRQ-001 |
| Data protection | plane separation (BR-017); least privilege | NFRQ-001/010 |
| Knowledge trust | admin-validated live links (BR-024) | TCON-11 |
| Compliance/residency | government policy | **RUC-01/02** (Q-014/Q-017) |

---

# 33. Logging & Monitoring (L6)

- **Application logs:** structured request/error logs (correlation IDs).
- **AI logs:** prompts/responses/provider/model/latency (for traceability + audit, BR-029).
- **Monitoring:** health checks, error rates, queue depth (email), AI latency/failures; alerting on thresholds.
- **Separation:** audit trail (§31, business/governance) is distinct from operational logs (technical).

---

# 34. Error Handling Strategy (L2/L6)

- **Consistent error envelope:** `{ code, message, details, correlation_id }`; appropriate HTTP status.
- **Graceful AI/RAG failure:** inaccessible knowledge source → clear message, never guess (BR-026); no grounding → fixed fallback string (BR-027); provider error → safe failure, logged, no fabricated output.
- **Validation errors:** field-level messages (completeness, amendment-window rejection).
- **Email failure:** queue retry with backoff (§30); surfaced if exhausted.
- **No silent failures:** all errors logged with correlation ID.

---

# 35. Non-Functional & Performance/Scalability (L6/all)

| Attribute | Approach | RTM |
|-----------|----------|-----|
| Performance | indexed Teras roll-ups; cache AI summaries; async FastAPI | NFRQ-006 |
| Scalability | stateless API (horizontal scale); PostgreSQL for prod concurrency; pgvector | NFRQ-007 |
| Availability | suitable uptime for monthly cycle; health checks | NFRQ-008 |
| Maintainability | layered/modular (AD-008), documented, provider-agnostic | NFRQ-009 |
| Data integrity | plane separation, transactions, FKs | NFRQ-010 |
> Scale sized to **Perak pilot** (TASM-10); revisit for national rollout.

---

# 36. Backup, Retention & Disaster Recovery (L6/L5)

- **Backup:** regular DB backups (PostgreSQL prod) + audit-log backup; vector store rebuildable from sources.
- **Retention:** records retained across the **2026–2035 horizon** (NFRQ-013); retention policy = **RUC** (confirm with government policy).
- **DR:** documented restore procedure; RPO/RTO targets set with hosting decision (RUC-01).
- **Knowledge plane:** re-ingestable from source documents/links (idempotent ingestion).

---

# 37. Deployment Architecture (L6)

### 37.1 Environments (text diagram)
```
DEVELOPMENT (local)                 PRODUCTION (cloud / government-approved — RUC-01)
 React+Vite dev server               built SPA (static hosting / reverse proxy)
 FastAPI (uvicorn)                    FastAPI (ASGI server) behind HTTPS
 SQLite + Chroma/keyword              PostgreSQL + pgvector
 provider: Groq (config.md)           provider: OpenAI/Anthropic (config.md)
 .env (dev keys)                      .env (prod secrets via secrets manager)
        └────── build layer-by-layer, test each layer (TR-006/TCON-12) ──────┘
```

### 37.2 Deployment rules (rule 7)
- Support **local development**, **future cloud deployment**, **government-approved hosting**, and strict
  **environment separation (dev/prod)**.
- CI/CD builds and tests each layer; production hosting/compliance = **RUC-01/02**.

---

# 38. Technical Testing Strategy (all layers)

### 38.1 Test pyramid (text diagram, rule 8)
```
              ▲  UAT (business scenarios; JPN/PPD/PIC/Exec)
             ╱ ╲  Security Testing · Performance Testing
            ╱   ╲  AI Response Validation · RAG Validation (grounding, citation, fallback)
           ╱     ╲  API Testing (contracts, RBAC, error envelope)
          ╱       ╲  Integration Testing (services + DB + provider adapter)
         ╱_________╲  Unit Testing (skills deterministic, services, models)
```

### 38.2 Testing coverage
- **Unit:** skills (deterministic), services, ORM models.
- **Integration:** service↔DB, agent↔skill, provider adapter (mocked).
- **API:** endpoint contracts, RBAC enforcement, error handling.
- **AI Response Validation:** advisory outputs sane; HITL gating verified (no auto-action).
- **RAG Validation:** retrieval relevance, **citation present**, **fallback string** on no-result, inaccessible-source message.
- **UAT:** real workflows (import, monthly update, dashboard, approvals).
- **Security:** auth/RBAC, input validation, rate limiting, secret handling.
- **Performance:** dashboard/query latency at pilot scale.
- Test cases trace to RTM `TC-*` references (§40 / RTM).

---

# 39. Technical Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|-----------|
| TRSK-01 | Vector RAG not ready for V1 | Med | **Keyword-search fallback** (TR-012) until vectors ready. |
| TRSK-02 | Provider API change / outage | Med | Provider abstraction; switch via config; retry/backoff. |
| TRSK-03 | Import data quality (messy Excel) | Med-High | Validation agent + completeness warnings; admin review. |
| TRSK-04 | AI hallucination / ungrounded answer | High | RAG grounding + citation + fallback; advisory + HITL. |
| TRSK-05 | Hosting/compliance unconfirmed | Med | RUC-01/02; local dev acceptable; prod gated on confirmation. |
| TRSK-06 | SQLite→PostgreSQL migration drift | Low-Med | SQLAlchemy + migrations; test on PostgreSQL early. |
| TRSK-07 | Secret leakage | High | `.env` excluded from VCS; secrets manager in prod; rate limiting. |
| TRSK-08 | Performance at scale (if national) | Med | Stateless API, indexing, caching; revisit scale (TASM-10). |

---

# 40. Technical Assumptions

Carried from Part 1 §6 (TASM-01…10) + RUC-01…04. Highlights: approved stack (TASM-01…06); rule-based
risk/alignment initially (TASM-07); OBB method in FDS (TASM-08); pilot scale (TASM-10).
**Resolved in v1.0 refinements (T6):**
- **TASM-09 (identity)** → **JWT-based auth is the default**; SSO is a future enhancement (§25.3).
- **Embeddings** → embedding provider is **separate** from the LLM provider; dev = local Sentence
  Transformer/OpenAI, prod = OpenAI (or approved) (§17.2/§20.3).
- **Agent framework** → **custom Agent Orchestrator for V1**; orchestration frameworks are a future option (§17.5).
- **Config profiles** → development / testing / production profiles; `config.md` primary (§27.2).
- **At-rest encryption** → required in production (§32).

**Requires User Confirmation before production:** hosting/residency (RUC-01), data classification/
compliance (RUC-02), Teras 5–7 data (RUC-03), knowledge corpus & link list (RUC-04).

---

# 41. Technical Traceability

Every technical component traces to the frozen **RTM v1.0** and **BRD v1.0** (rule 9). Mapping:
- **Layers → modules:** AD-008 §9.2 (L1–L6 → M1–M13).
- **Services/APIs → modules → requirements:** §26.2 (service → module → RTM FRQ/AIRQ).
- **Agents/Skills → capabilities → requirements:** §18/§19 (→ CAP-* → RTM).
- **Data entities → RTM DB column:** §13 (KPI, MonthlyUpdate, FinanceAllocation, AuditLog, etc.).
- **Test cases → requirements:** §38 (TC-* per RTM).
- **No orphan components:** every module/service/agent/skill/entity implements ≥1 RTM requirement; **no new
  business requirements introduced** by the TRD.
The RTM will be **expanded** (not reopened) with final TRD §, API, entity and test-case IDs during build/test.

---

# 42. Appendices

- **App A — Layer→Module map:** §9.2. · **App B — Service/API catalogue:** §26.2.
- **App C — Data entities:** §13 (operational) + §14 (knowledge plane). · **App D — Agent roster & skills:** §18/§19.
- **App E — config.md schema:** mode/provider/model (§27); **`.env.example`** vars (§28).
- **App F — Provider abstraction interface:** `chat()`, `embed()` (§17.2).
- **App G — Open technical items:** RUC-01…04; TASM-07/08/09.
- **App H — Reference baselines:** HMW v1.0, BRD v1.0, RTM v1.0, ADRs AD-001…008.

---

## Self-Review — TRD Part 5

| Check | Finding | Action |
|-------|---------|--------|
| 9 implementation rules applied? | Auth/RBAC (§25), Config/provider (§27/§28), Notification engine incl. escalation+retry+future channels (§30), Dashboard services incl. FDS (§24), Audit events all 8 (§31), Security all 8 controls (§32), Deployment envs (§37), Testing all 8 types (§38), Traceability (§41). | OK |
| Diagrams included? | Dashboard, auth/RBAC, config/provider, notification, deployment, test pyramid (text). | OK |
| Traceable / no new requirements? | §41 maps all components to RTM/BRD; nothing new. | OK |
| Open items handled? | RUC-01…04, TASM, TRSK captured — classified, not blocking. | OK |
| Consistent with Parts 1–4 & frozen docs? | Stack, layers, HITL, plane separation, provider abstraction consistent. | OK |

---

**— END OF PART 5 — (TRD DRAFT COMPLETE)**
*Part 5 covers: Dashboard · Auth & RBAC · API · Configuration · Environment · Integration · Notification/Email · Audit & Version History · Security · Logging/Monitoring · Error Handling · NFR/Performance · Backup/Retention/DR · Deployment · Testing · Risks · Assumptions · Traceability · Appendices.*

---

## FREEZE RECORD — Technical Baseline (Freeze Gate 2)
- **Baseline:** D3 — Technical Requirements Document, **v1.0 FROZEN** on 2026-06-27 (**Freeze Gate 2 PASSED**).
- **Approved by:** User (suzila@iegcampus.com).
- **Scope of baseline:** §1–§42 + Appendices A–H — six-layer architecture (AD-008); frontend/backend/data/
  AI/knowledge/infrastructure designs; capability-driven multi-agent + skills; RAG (LLM/embedding separation);
  FDS (top-level); dashboard; JWT auth + RBAC; API catalogue; config profiles + provider abstraction/strategy;
  notification engine; audit & version history; security (incl. prod at-rest encryption); logging/monitoring;
  error handling; NFR/performance; backup/retention/DR; deployment; testing strategy; risks; assumptions;
  technical traceability.
- **T6 audit:** overall technical quality 94%; six refinements applied (LLM/embedding separation, JWT auth,
  custom orchestrator, config profiles, AI provider strategy, prod at-rest encryption); AD-009 / TR-015…019.
- **Traceability:** implements BRD v1.0 per RTM v1.0; **0 orphan components; no new business requirements.**
- **Carry-forward (Requires User Confirmation before production):** hosting/residency (RUC-01), data
  classification/compliance (RUC-02), Teras 5–7 data (RUC-03), knowledge corpus & link list (RUC-04).
- **Reopen policy:** changes only via explicit, logged change request (CHANGE_LOG.md).

---
*End of Technical Requirements Document v1.0 — FROZEN APPROVED TECHNICAL BASELINE. Foundation for Solution Architecture & Development.*
