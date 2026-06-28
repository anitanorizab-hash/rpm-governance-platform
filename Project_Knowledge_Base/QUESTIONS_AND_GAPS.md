# QUESTIONS_AND_GAPS.md

> **Single Source of Truth — Open Questions & Missing Information**
> Status: `LIVING DOCUMENT` · Version: 0.1 (DRAFT) · Last updated: 2026-06-27

---

## Purpose
A cumulative register of everything **unknown, unconfirmed, or contradictory**. Nothing is guessed:
open items live here until answered. Each item is tracked to closure so no gap is silently lost
before the BRD.

## When updated
- Every Discovery analysis adds new questions.
- Items are closed (with the answer + date) when the user confirms.

## Relationship with other documents
- **Feeds:** BRD scoping, `REQUIREMENTS_REGISTER.md`.
- **Cross-checks:** `BUSINESS_RULES.md`, `PROJECT_CONTEXT.md`.

## ID convention
`Q-NNN` (question) / `GAP-NNN` (missing info). Status: Open / Answered / Deferred.

---

| ID | Item | Category | Status | Answer / Notes |
|----|------|----------|--------|----------------|
| Q-001 | Full official expansion of **RPM**, and its relationship to **PPPM** (file names say "PT PPPM 2026-2035"). | Scope | Open | |
| Q-002 | Is **school level** a data/reporting level only, or do school users log in and key data? (drives scale) | Users | Open | |
| Q-003 | Geographic scope: nationwide, or **Perak pilot** first? (data observed = Perak, 12 PPD) | Scope | **RESOLVED (CL-026):** Adopt the latest approved scope (PROJECT_CONTEXT/BRD §6): JPN/PPD with schools as reporting tier; Perak as initial working set. **National rollout = Future Enhancement.** | |
| Q-004 | Full **role list** and the **approval hierarchy** — who approves reports/actions/emails? | Users | Open | |
| Q-005 | Who is the **system/governance administrator** (manages users, amendment windows, audit trail)? | Users | Open | |
| Q-006 | Exact definition of **"incomplete"** that triggers warnings (which fields, what thresholds). | Rules | Open | |
| Q-007 | Reminder rules: timing, frequency, **escalation** path for non-response. | Rules | Open | |
| Q-008 | Exact mechanics of the **Low Cost High Impact Matrix** (what is "cost", what is "impact", thresholds, data source). | AI/Finance | Open | |
| Q-009 | How do **budget/allocation figures** enter — manual entry or finance-system integration? | Data/Integration | Open | |
| Q-010 | Monthly report **format, recipients, approval flow**; must it match an official template? | Reporting | Open | |
| Q-011 | Form of **RPM 2026–2035** corpus for RAG (single PDF / many docs / bilingual?). | AI/RAG | Open | |
| Q-012 | **Language** requirement for UI, chatbot, reports (Bahasa Malaysia / English / both). Source data is Bahasa Malaysia. | UX | **RESOLVED (CL-026):** UI & reports support **English as primary development language**; **future localisation** (e.g. Bahasa Malaysia) allowed. Source KPI/knowledge content remains in its original language. | |
| Q-013 | Target **technology stack**. | Technical | **RESOLVED (CL-031):** see AD-007 / TR-009…014 (full stack approved). | |
| Q-014 | **Hosting** model and data residency (gov cloud / on-prem). | Technical | Open | |
| Q-015 | **Identity** mechanism behind the email-domain restriction (SSO vs. verification). | Security | **RESOLVED (CL-036):** **JWT-based authentication** is the default (access+refresh, expiry, CORS, CSRF, HTTPS prod); **SSO = future enhancement** (TRD §25.3, AD-009). | |
| Q-016 | Expected **scale** (KPIs, PICs, offices, schools). | Technical | Open | |
| Q-017 | Security/compliance regime and **data classification** of KPI & budget data. | Security | Open | |
| Q-018 | Definition and scope of the **Executive Copilot**. | AI | Open | |
| GAP-001 | Drive files (latest KPI content) not yet locally readable; using local `Data/` set for analysis. | Data | Open | |
| GAP-002 | JPN workbook contains only **Teras 1&2** and **Teras 3&4** sheets — Teras 5–7 location unknown. | Data | Open | |
| Q-019 | Which specific `Data/` files/links are **Knowledge sources** (beyond RPM 2026–2035)? Guidelines, circulars, notes not yet seen locally. | Data/RAG | Open | D3A §1B |
| Q-020 | Source of **risk** rating per KPI (computed by AI, entered by PIC, or rule-based?) — needed for dashboard risk summary/heatmap. | Rules/AI | Open | D3A §2,§3 |
| Q-021 | Definition of **"RPM alignment strength"** and how it is measured per Teras. | AI/Metric | Open | D3A §2 item 10 |
| Q-022 | **Trust / allow-list policy for live links:** which domains/sources are approved for RAG fetching; who approves them; how "official/trusted" is enforced; and is outbound fetching of external URLs permitted under the government data-egress/security policy? | Security/RAG | **RESOLVED (CL-026):** Live knowledge links are **supported RAG sources subject to administrator validation** (admin approves/validates each link before/at ingestion; prefer official/trusted per BR-024). Detailed allow-list mechanics → TRD. | D3B (BR-024) |
| Q-023 | **Login domain contradiction:** user rule BR-003 says login allowed for BOTH `moe.gov.my` AND `moe-dl.edu.my`; `project_structure.pptx` TR002 says validate `@moe.gov.my` only. Which is authoritative? | Security | **RESOLVED (CL-026):** BOTH `@moe.gov.my` and `@moe-dl.edu.my` (BR-003 authoritative; pptx superseded). | CONTRADICTION C-001 |
| Q-024 | **Agent count reconciliation.** | AI | **RESOLVED (CL-026):** Architecture is **capability-driven**. The current primary agents (see To-Be §6 / BRD §17) plus the reusable Skills Layer implement the capabilities; the **agent count may evolve without changing the business architecture**. No fixed number is mandated. | To-Be §6, BRD §17 |
| Q-025 | **OBB** (Outcome-Based Budgeting): confirm full meaning, how "OBB value for money" is calculated, and its relationship to the Low Cost High Impact Matrix. | Finance/AI | **RESOLVED (CL-026):** OBB recognised as **part of the Financial Decision Support capability and the budget-governance process** (BR-038/046). Calculation method to be detailed in TRD (Technical Assumption). | pptx |
| Q-026 | Is the tech stack **React + Vite + Tailwind** (pptx TR001) confirmed/authoritative? Backend, database and RAG/vector store still unspecified. | Technical | **RESOLVED (CL-031):** Full stack approved — FE React/Vite/Tailwind/ShadCN/Recharts; BE Python/FastAPI/SQLAlchemy; DB SQLite(dev)/PostgreSQL(prod); vector Chroma/pgvector + keyword fallback; provider Groq/OpenAI/Anthropic via config.md+.env. See AD-007/TR-009…014. | pptx TR001 |
| Q-027 | Is `project_structure.pptx` an **authoritative baseline** to build on, or an earlier draft to be superseded by our gated BRD/TRD process? | Process | Open | pptx |

---

## Contradictions log
| ID | Contradiction | Sources | Status |
|----|---------------|---------|--------|
| C-001 | Login domains: **both** `moe.gov.my` + `moe-dl.edu.my` (BR-003) vs **only** `@moe.gov.my` (pptx TR002). | User context vs pptx | **RESOLVED (CL-026):** BOTH `@moe.gov.my` and `@moe-dl.edu.my` allowed (BR-003 stands). pptx TR002 superseded. |
| C-002 | Agent count: pptx states **14 agents** but lists 10; other clarifications add ≥4 more → totals don't reconcile. | pptx vs D3A/D3B | **RESOLVED (CL-026):** Architecture is **capability-driven**; current primary agents + reusable Skills Layer; agent count may evolve without changing the business architecture. No fixed count required. |
| C-003 | Possible terminology drift: **RPM** (user) vs **PPPM** (file names) vs pptx using neither in BR/TR text. | All sources | Open (see Q-001) |
