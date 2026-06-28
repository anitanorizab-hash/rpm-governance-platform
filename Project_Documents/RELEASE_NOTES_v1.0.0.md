# Release Notes — Agentic AI Strategic Governance Platform

**Version:** v1.0.0
**Release type:** Demonstration / UAT build
**Date:** 2026-06-28
**Programme:** RPM 2026–2035 (JPN → PPD → School)

> AI outputs are **advisory only** and never replace authorised management decisions. A human
> officer approves every formal action, report and email (ASM-11 / BR-015).

---

## 1. New Features

**Operational KPI governance**
- One-time Excel import (Pelan Taktikal JPN/PPD) → system of record; **no monthly Excel**.
- KPI management with completeness detection and an **amendment window** (statement/indicator/target editable in July & October only, Super Admin override).
- In-system **monthly updates**; deterministic achievement-status + risk derivation; full amendment history.

**Dashboards & analytics**
- **Teras 1–7** dashboard: overview, risk, budget, submission summaries, high-risk list, KPI mapping, deterministic executive summary (Recharts).

**Financial Decision Support (FDS)**
- Budget Intelligence, **OBB** (outcome-based budgeting), **Low Cost / High Impact** matrix, resource-optimisation notes, and advisory strategic recommendations.

**Advisory AI layer (capability-driven)**
- Skills Layer (S1–S15) + 11 agents + custom Agent Orchestrator.
- **RAG chatbot** — role-scoped, grounded, **cited**, with a fixed fallback when ungrounded.
- **Executive Copilot** — briefing, strategic Q&A, recommendation drafting.

**Governance & workflow**
- **Human-in-the-loop** approval engine (draft → pending review → approved/rejected; final states immutable).
- **Append-only audit trail** for every official action and decision.
- Report generation and notification/email queue — **dry-run** send unless production SMTP is configured.

**Security & administration**
- JWT auth (access + refresh); MOE-domain restriction (`@moe.gov.my` / `@moe-dl.edu.my`).
- Server-side **RBAC** across 9 roles; Admin module for users/roles, knowledge sources, live links, audit, import history, and provider/system health.

## 2. Architecture Summary
Six layers (AD-008): **L1** React/Vite/Tailwind/ShadCN/Recharts · **L2** FastAPI/SQLAlchemy/Alembic · **L3** advisory AI (skills/agents/orchestrator, provider-agnostic adapter) · **L4** knowledge/RAG (keyword V1 → embeddings) · **L5** SQLite (dev)/PostgreSQL (prod) · **L6** infrastructure. Operational and knowledge planes are kept separate; L1 talks only to `/api/v1`; agents reach data only through services.

## 3. Known Limitations
- **LLM provider not configured in dev** → AI narrative uses deterministic placeholders; chatbot/Copilot ground via **keyword** retrieval (embeddings/Chroma deferred post-V1).
- Imported Pelan Taktikal JPN populates **Teras 1–4**; Teras 5–7 await source data (GAP-002).
- Email sending is **dry-run** until production SMTP is set.
- Live-link content is registered/validated but not auto-crawled in V1.
- Readiness endpoint reports component checks as `pending` (deep checks are a prod hardening item).

## 4. Future Enhancements
- Embeddings + vector store (Chroma/pgvector) for semantic RAG.
- Live Groq/OpenAI/Anthropic narrative via config switch.
- Teras 5–7 data onboarding; PPD/School tier rollout.
- SSO, production SMTP, at-rest encryption, deep readiness probes, CI/CD.

## 5. Deployment Notes
- **Dev:** `uvicorn app.main:app --port 8000` + `npm run dev` (Vite @ 5173); SQLite `app_dev.db`; `alembic upgrade head`.
- **Prod (RUC):** PostgreSQL, real provider keys in `.env` (never in `config.md`/code), HTTPS, CORS to approved origins, at-rest encryption. Provider switching is **config-only** via the Provider Adapter.
- Secrets live only in `.env`; configuration profiles (development/testing/production) in `config.md`.

## 6. Demo Notes
- Seed the demo dataset: `cd backend && python scripts/seed_demo.py` (idempotent on a migrated DB).
- Demo users share password **`Demo@2026`** (see `DEMO_GUIDE.md` for the per-role list and 15-minute flow).
- Demonstrates both **grounded + cited** RAG answers and the **fixed fallback** message.
