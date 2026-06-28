# ARCHITECTURE_DECISIONS.md

> **Single Source of Truth — Architecture Decision Records (ADR)**
> Status: `LIVING DOCUMENT` · Version: 0.1 (DRAFT) · Last updated: 2026-06-27

---

## Purpose
Records every significant **design decision** with its context, the decision, alternatives
considered, and consequences. Gives the team a durable rationale across a 10-year horizon.

## When updated
- Whenever a design decision is agreed (architecture, AI, data, integration).
- Superseded decisions are kept (status = Superseded) and linked to their replacement.

## Relationship with other documents
- **Feeds:** System Architecture, AI Agent Architecture, TRD.
- **Draws from:** `TECHNICAL_RULES.md`, `AI_RULES.md`, `BUSINESS_RULES.md`.

## ADR template
```
### AD-NNN — <title>
- Status: Proposed | Accepted | Superseded
- Date:
- Context:
- Decision:
- Alternatives considered:
- Consequences:
- Related: BR-/TR-/AIR- ids
```

---

### AD-001 — LLM provider abstraction layer
- Status: Accepted
- Date: 2026-06-27
- Context: Dev uses Groq; prod may use OpenAI or Anthropic via `config.md` (TR-001/002).
- Decision: Provider selection is config-driven behind an abstraction; no code change to switch.
- Alternatives: Hard-code a single provider (rejected — fails the requirement and 10-yr longevity).
- Consequences: Requires a uniform internal interface for chat/embeddings across providers.
- Related: TR-001, TR-002, TR-003, AIR-040, AIR-041

### AD-002 — Excel is import-once; system is the record thereafter
- Status: Accepted
- Date: 2026-06-27
- Context: BR-001/BR-002.
- Decision: A one-time ingestion pipeline imports Pelan Taktikal; all later updates are in-system.
- Alternatives: Continuous Excel sync (rejected — breaks audit trail and single source of truth).
- Consequences: Need import validation, completeness detection, and a clean cut-over.
- Related: BR-001, BR-002, BR-005, TR-007

### AD-003 — Human-in-the-loop as an architectural control
- Status: Accepted
- Date: 2026-06-27
- Context: BR-015.
- Decision: Every outbound/formal action passes through a human approval gate by design.
- Alternatives: Fully autonomous agents (rejected — governance/political risk).
- Consequences: Workflow engine must model "drafted → reviewed → approved → executed" states.
- Related: BR-015, AIR-001, AIR-002

### AD-004 — Dual data plane: Operational DB vs. Knowledge/RAG base
- Status: Accepted
- Date: 2026-06-27
- Context: D3A §1/§5 — the `Data/` folder holds two file classes with different lifecycles.
- Decision: Maintain **two distinct stores**. (a) **Operational store (database):** Pelan Taktikal
  JPN/PPD imports, monthly KPI updates, PIC info, budget status, audit trail, reports — structured,
  transactional, audit-grade. (b) **Knowledge store (RAG/vector + references):** RPM 2026–2035,
  guidelines, circulars, notes, supporting docs and **links** — chunked/embedded for retrieval.
- Alternatives: Single store mixing operational rows and documents (rejected — different access
  patterns, governance, and update cadence; would blur audit trail and RAG grounding).
- Consequences: Need an ingestion path per plane (import-once for operational; RAG pipeline for
  knowledge); knowledge links recorded as references for later processing.
- Related: BR-017, BR-018, BR-019, AD-002, AIR-010, AIR-011

### AD-005 — Teras-centric main dashboard as the primary view
- Status: Accepted
- Date: 2026-06-27
- Context: D3A §2/§3/§4/§6.
- Decision: The main page is organised around the **7 Teras of RPM 2026–2035** — per-Teras summaries,
  charts, a KPI mapping table, and an AI summary section. Phasing allowed: **cards/tables first,
  charts later** if needed for V1.
- Alternatives: Flat KPI list without Teras grouping (rejected — fails BR-020 and executive need).
- Consequences: Data model and aggregation queries must roll up by Teras; AI summary depends on
  operational DB + monthly updates + budget + RPM/knowledge.
- Related: BR-020, BR-021, BR-022

### AD-006 — Knowledge base supports static + live/link sources
- Status: Accepted
- Date: 2026-06-27
- Context: D3B — some chatbot knowledge comes from links that change over time, not just uploads.
- Decision: The RAG/knowledge base supports **Static sources** (uploaded docs, manual notes) and
  **Live/Updated sources** (URLs/links). Links are stored with metadata (title, URL, category,
  last-checked date), are admin **refreshable/reprocessable**, and content is ingested when accessible.
  Answers cite sources; inaccessible sources yield a clear message; absent info yields the fixed
  fallback string. Official/trusted sources preferred.
- Alternatives: Upload-only knowledge base (rejected — misses current/online information).
- Consequences: Need a link registry + fetch/refresh pipeline, source-citation in answers, access-
  failure handling, and a freshness ("last checked") concept.
- Related: BR-023, BR-024, BR-025, BR-026, BR-027, AIR-014–017, AIR-070, AIR-071

### AD-007 — Approved technology stack (TRD default)
- Status: Accepted
- Date: 2026-06-27
- Context: TRD authoring (T1) requires a confirmed stack.
- Decision: **Frontend** React + Vite + Tailwind + ShadCN UI + Recharts; **Backend** Python + FastAPI +
  SQLAlchemy; **DB** SQLite (dev) / PostgreSQL (prod); **Vector/RAG** Chroma or pgvector with keyword-search
  fallback for V1; **AI provider** Groq (dev) / OpenAI|Anthropic (prod) via `config.md` + `.env`;
  **Hosting** local (dev), cloud/government-approved (prod, subject to compliance confirmation).
- Alternatives: Node/TS backend (rejected — Python better fits agentic/RAG ecosystem and team default).
- Consequences: ORM via SQLAlchemy enables SQLite→PostgreSQL portability; provider abstraction required
  (AD-001); pgvector aligns with PostgreSQL prod (single store) vs Chroma as standalone in dev.
- Related: TR-009…014, AD-001, BR-044; resolves Q-013/Q-026.

### AD-008 — Six-layer enterprise architecture (binding)
- Status: Accepted
- Date: 2026-06-27
- Context: TRD requires a consistent layered model used throughout.
- Decision: Adopt six layers, each with assigned technologies:
  1. **Presentation** — React, Vite, Tailwind, ShadCN UI, Recharts.
  2. **Application** — FastAPI, Business Services, Authentication, REST APIs, Workflow Management.
  3. **AI** — Multi-Agent Architecture, Skills Layer, Executive Copilot, KPI Chatbot, Financial Decision
     Support, AI Orchestration.
  4. **Knowledge** — RAG, Knowledge Repository, Uploaded Documents, Live Knowledge Links, Embeddings, Vector Store.
  5. **Data** — SQLite (dev), PostgreSQL (prod), Chroma/pgvector, Audit Trail, Operational Database.
  6. **Infrastructure** — config.md, .env, AI Provider Switching, Logging, Monitoring, Deployment, Security.
- Consequences: every TRD section maps to ≥1 layer; layer boundaries define module ownership and
  dependencies; AI (L3) and Knowledge (L4) are distinct from Data (L5) to preserve operational/knowledge
  plane separation (BR-017/AD-004).
- Related: AD-007, TR-009…014, BR-016/017/041/044.

### AD-009 — TRD v1.0 technical refinements (T6)
- Status: Accepted
- Date: 2026-06-27
- Context: T6 audit refinements before TRD Freeze Gate 2.
- Decisions:
  1. **LLM/Embedding separation** — Provider Adapter exposes `chat()` and `embedding()` independently;
     dev LLM=Groq + embeddings=local ST/OpenAI; prod LLM=OpenAI/Anthropic + embeddings=OpenAI (approved).
  2. **JWT authentication** default (access+refresh, expiry, CORS, CSRF, HTTPS prod); **SSO = future**.
  3. **Custom Agent Orchestrator** for V1; orchestration frameworks optional in future.
  4. **Config profiles** development/testing/production; `config.md` primary; secrets in `.env`.
  5. **AI Provider Strategy** — abstraction, selection, failover (retry/secondary), cost optimisation; provider-agnostic.
  6. **At-rest encryption** required in production.
- Consequences: provider-agnostic across both chat and embeddings; auth/build unambiguous; minimal V1 deps.
- Related: TR-015…019, AD-001/007/008, BR-044; resolves Q-015/TASM-09 and audit gaps G-1…G-4.

> Further ADRs to be added during TRD and Architecture phases.
