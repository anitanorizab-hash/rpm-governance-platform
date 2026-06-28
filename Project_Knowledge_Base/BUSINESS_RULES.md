# BUSINESS_RULES.md

> **Single Source of Truth — Confirmed Business Rules**
> Status: `LIVING DOCUMENT` · Version: 0.1 (DRAFT) · Last updated: 2026-06-27

---

## Purpose
Records every **confirmed business rule** — the non-negotiable policy/process constraints the
system must enforce. Each rule has a stable ID for traceability into BRD, TRD, user stories and tests.

## When updated
- When a new rule is confirmed by the user or discovered in a source document and verified.
- When a rule is amended (record change in `CHANGE_LOG.md`, keep the ID).

## Relationship with other documents
- **Feeds:** BRD (each rule → requirement), `REQUIREMENTS_REGISTER.md`, `TRACEABILITY_REGISTER.md`.
- **Constrains:** TRD, AI behaviour (`AI_RULES.md`), data model.

## ID convention
`BR-NNN`. Status: Confirmed / Proposed / Superseded.

---

| ID | Rule | Status | Source |
|----|------|--------|--------|
| BR-001 | Excel files are used for **initial input only**. | Confirmed | User context |
| BR-002 | After initial import, all monthly KPI updates must be **keyed in by the KPI PIC inside the system** (no further Excel). | Confirmed | User context |
| BR-003 | Login is allowed **only** with `moe.gov.my` and `moe-dl.edu.my` email accounts. | Confirmed | User context |
| BR-004 | Every KPI must have **PIC name, sector and PIC email**. | Confirmed | User context |
| BR-005 | The system must **detect incomplete information** from the initial Pelan Taktikal JPN and PPD. | Confirmed | User context |
| BR-006 | The system must **show warnings** for missing information. | Confirmed | User context |
| BR-007 | PIC must **receive reminders** for incomplete data and monthly updates. | Confirmed | User context |
| BR-008 | KPI **statement, indicator and target may only be amended in July and October**. | Confirmed | User context |
| BR-009 | **All amendments must be saved in an audit trail**. | Confirmed | User context |
| BR-010 | Finance section must record allocation status as one of: **received / will be received / pending / not received / not required / insufficient**. | Confirmed | User context |
| BR-011 | Budget Intelligence must use the **Low Cost High Impact Matrix**. | Confirmed | User context |
| BR-012 | System must support **RAG using RPM 2026–2035 as the main reference document**. | Confirmed | User context |
| BR-013 | System must provide a **KPI chatbot**. | Confirmed | User context |
| BR-014 | System must **generate monthly reports**. | Confirmed | User context |
| BR-015 | **Human review is required before** formal action, report approval and email sending. | Confirmed | User context |
| BR-016 | The system must include an **agents and skills layer**. | Confirmed | User context |
| BR-017 | **Two data classes** must be kept separate: **Operational Data** (Pelan Taktikal JPN/PPD, monthly updates, PIC info, budget status, audit trail, reports) goes to the **database**; **Knowledge Data** (RPM 2026–2035, guidelines, circulars, notes, supporting docs, links) goes to the **RAG/knowledge base**. | Confirmed | D3A §1, §5 |
| BR-018 | Pelan Taktikal JPN and PPD are **initial operational input only**; after import the database is the working source and Excel must not be the monthly source. | Confirmed | D3A §1A (reinforces BR-001/002) |
| BR-019 | Knowledge documents (and knowledge **links**) are processed **into RAG**, never treated as monthly KPI input. Links are recorded as knowledge references and processed by the RAG pipeline where possible. | Confirmed | D3A §1B |
| BR-020 | The **main dashboard must summarise and map all KPIs according to the 7 Teras of RPM 2026–2035**. (Carry into HMW, BRD, TRD, Architecture.) | Confirmed | D3A §2, §6 |
| BR-021 | The main dashboard must present the defined KPI/Teras summaries (totals, count/achievement/risk/completion/missing-info/submission/budget per Teras, Low Cost High Impact summary, RPM alignment strength, AI summary, distribution chart, KPI→Teras→PIC→Sector→Status→Risk→Budget table, executive summary). | Confirmed | D3A §2 (items 1–14) |
| BR-022 | The main page must include an **AI-generated summarisation section** answering the 7 management questions (overall status, highest-KPI Teras, highest-risk Teras, most-missing-info Teras, most-budget-issue Teras, KPI needing immediate attention, recommended monthly management focus). | Confirmed | D3A §4 |
| BR-023 | Knowledge sources are of **two types**: **Static** (RPM PDF, guidelines, circulars, meeting notes, uploaded docs) and **Live/Updated** (official links, online reference pages, shared updated docs, any link with current info). | Confirmed | D3B |
| BR-024 | For each **link** knowledge source the system must store: link as a source, **title, URL, category, last-checked date**; allow admin to **refresh/reprocess**; use content for chatbot/KPI mapping if accessible; **prefer official/trusted sources**. | Confirmed | D3B |
| BR-025 | The chatbot must **clearly show the source(s) used** in its answers. | Confirmed | D3B |
| BR-026 | If a link/source **cannot be accessed**, the system must show a clear message and **must not guess**. | Confirmed | D3B |
| BR-027 | If information is not in the KPI data or knowledge sources, the chatbot must reply exactly: **"I cannot find this information in the available KPI data or knowledge sources."** | Confirmed | D3B |

### Derived/observed rule candidates (await confirmation)
| ID | Candidate rule | Status | Source |
|----|----------------|--------|--------|
| BR-C01 | KPI identity follows the code scheme `TSx.Sy.Pz.KPIn`. | Proposed | JPN file inspection |
| BR-C02 | Budget is broken down by government object codes (OS21000…OS42000) with monthly projections Jan–Dec. | Proposed | JPN file inspection |
| BR-C03 | A KPI may be marked "KPI Baharu" (new, no TOV baseline) vs. having a TOV (2025 achievement). | Proposed | JPN file inspection |
| BR-C04 | Each KPI carries a delivery year ("Tahun KPI diturunkan kepada JPN") and may be a "Quick Win". | Proposed | JPN file inspection |
