# TECHNICAL_RULES.md

> **Single Source of Truth — Confirmed Technical Rules**
> Status: `LIVING DOCUMENT` · Version: 0.1 (DRAFT) · Last updated: 2026-06-27

---

## Purpose
Records confirmed **technical constraints and rules** governing how the system is built and run
(stack, environments, integration, build discipline). Distinct from business policy (`BUSINESS_RULES.md`)
and AI behaviour (`AI_RULES.md`).

## When updated
- When a technical constraint is confirmed or a technology decision is made (also log in `ARCHITECTURE_DECISIONS.md`).

## Relationship with other documents
- **Feeds:** TRD, System Architecture, `REQUIREMENTS_REGISTER.md` (NFRs).
- **Constrained by:** `BUSINESS_RULES.md`, security/compliance requirements.

## ID convention
`TR-NNN`. Status: Confirmed / Proposed / TBC.

---

| ID | Rule | Status | Source |
|----|------|--------|--------|
| TR-001 | **Development mode uses Groq** as the LLM provider. | Confirmed | User context |
| TR-002 | **Production/golive mode may use OpenAI or Anthropic**, selected via `config.md`. | Confirmed | User context |
| TR-003 | LLM provider selection must be a **configuration decision** (`config.md`), not a code change → requires a provider-abstraction layer. | Confirmed | Derived from TR-001/002 |
| TR-004 | Development is done **step by step in VS Code**. | Confirmed | User context |
| TR-005 | **No coding** begins until HMW, BRD, TRD and key architecture documents are completed, audited and frozen. | Confirmed | User context |
| TR-006 | Application is built **layer by layer**, with each layer tested before the next. | Confirmed | User context |
| TR-007 | Excel ingestion is an **import-once pipeline** used only at onboarding; thereafter records are system-native. | Confirmed | Derived from BR-001/002 |
| TR-008 | Authentication is restricted to MOE email domains (`moe.gov.my`, `moe-dl.edu.my`) — identity mechanism (true SSO vs. email verification) TBC. | Confirmed (mechanism TBC) | BR-003 |
| TR-009 | **Frontend stack:** React + Vite + Tailwind CSS + **ShadCN UI** + **Recharts**. | Confirmed (CL-031) | User (T1 approval) |
| TR-010 | **Backend stack:** Python + **FastAPI** + **SQLAlchemy**. | Confirmed (CL-031) | User |
| TR-011 | **Database:** **SQLite (development)**, **PostgreSQL (production)**. | Confirmed (CL-031) | User |
| TR-012 | **Vector store / RAG:** **Chroma or pgvector** (per architecture); **keyword-search fallback** if vector search not ready in V1. | Confirmed (CL-031) | User |
| TR-013 | **AI provider:** Groq (dev); OpenAI or Anthropic (prod/golive); controlled via `config.md` **and** `.env`. | Confirmed (CL-031) | User (reinforces TR-001/002) |
| TR-014 | **Hosting:** local environment acceptable for development; production = cloud or government-approved hosting **subject to compliance confirmation** (Requires User Confirmation before production). | Confirmed (dev) / RUC (prod) | User |
| TR-015 | **LLM and Embedding providers are independent.** Provider Adapter supports `chat()` and `embedding()` separately. Dev: LLM=Groq, Embeddings=local Sentence Transformer/OpenAI. Prod: LLM=OpenAI/Anthropic, Embeddings=OpenAI (or approved). | Confirmed (CL-036) | User (T6) |
| TR-016 | **Authentication = JWT** (access + refresh tokens, expiry, CORS, CSRF, HTTPS prod). **SSO = future enhancement.** | Confirmed (CL-036) | User (T6) |
| TR-017 | **V1 uses a custom Agent Orchestrator** — no mandatory LangChain/LlamaIndex; frameworks optional in future. | Confirmed (CL-036) | User (T6) |
| TR-018 | **Environment configuration profiles:** development / testing / production; `config.md` primary; secrets in `.env`. | Confirmed (CL-036) | User (T6) |
| TR-019 | **Sensitive data encrypted at rest in production** (DB/storage encryption, encrypted backups, managed secrets). | Confirmed (CL-036) | User (T6) |

### Proposed from project_structure.pptx (await confirmation as authoritative — Q-026/Q-027)
| ID | Item | Status | Source |
|----|------|--------|--------|
| TR-P01 | Frontend: **React + Vite + Tailwind**. | Proposed | pptx TR001 |
| TR-P02 | Excel import as **master records**; structured KPI data model. | Proposed (aligns BR-001/TR-007) | pptx TR003/004 |
| TR-P03 | Dashboard with summary cards + charts; monthly KPI update form; financial section. | Proposed (aligns BR-020/021) | pptx TR005/006/007 |
| TR-P04 | **Rule-based** KPI status classification + risk detection (vs AI-based — clarify with Q-020). | Proposed | pptx TR008/009 |
| TR-P05 | **Agent Centre** hosting **14 AI agents**; email trigger engine; report archive + notification log. | Proposed | pptx TR010/011/012 |

### To be confirmed
| ID | Item | Status |
|----|------|--------|
| TR-T01 | Primary backend language/stack. | **RESOLVED (CL-031):** Python/FastAPI/SQLAlchemy (TR-010). |
| TR-T02 | Hosting model (gov cloud / on-prem / MyGovCloud) and data residency. | TBC |
| TR-T03 | Database technology. | **RESOLVED (CL-031):** SQLite (dev) / PostgreSQL (prod) (TR-011); vector Chroma/pgvector (TR-012). |
| TR-T04 | Expected scale (number of KPIs, PICs, offices, schools). | TBC |
| TR-T05 | Security/compliance regime and data classification. | TBC |
