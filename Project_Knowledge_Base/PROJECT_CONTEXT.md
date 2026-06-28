# PROJECT_CONTEXT.md

> **Single Source of Truth — Project Overview**
> Status: `LIVING DOCUMENT` · Version: 0.1 (DRAFT) · Last updated: 2026-06-27
> Owner: Solution Architecture / Business Analysis

---

## 1. Purpose of this document
Holds the **overall, evolving understanding** of the project: what it is, who it serves,
why it exists, and the high-level shape of the solution. This is the orientation document a
new team member or stakeholder reads first. It is narrative and explanatory — detailed rules
live in the dedicated registers (`BUSINESS_RULES.md`, `TECHNICAL_RULES.md`, `AI_RULES.md`).

## 2. When this document is updated
- After every project document is analysed (Discovery phase).
- Whenever a freeze (BRD/TRD baseline) changes the shared understanding.
- Whenever a confirmed answer closes an item in `QUESTIONS_AND_GAPS.md`.

## 3. Relationship with other documents
- **Feeds:** HMW, BRD, TRD (this is the context they are written against).
- **Draws from:** every analysed source document, `BUSINESS_RULES.md`, `AI_RULES.md`.
- **Cross-checks with:** `QUESTIONS_AND_GAPS.md` (open items) and `CHANGE_LOG.md`.

---

## 4. Project identity
- **Project name:** Agentic AI Strategic Governance Platform for RPM 2026–2035 — KPI Monitoring,
  Monthly Update, Budget Intelligence, Intervention, Notification, Reporting & Executive Decision Support.
- **Domain:** Government education governance (Malaysia, Ministry of Education / Kementerian Pendidikan).
- **Strategic frame:** RPM (Rancangan Pendidikan Malaysia) 2026–2035, structured around **7 Teras Strategik**.
- **Governance tiers:** JPN (state) → PPD (district) → School.
- **Initial data scope observed:** State = **PERAK**; 12 PPD districts; KPI plans organised by Teras 1–7.

## 5. One-line understanding
A decade-long, audit-grade governance backbone that uses **agentic AI to assist — never replace —**
human decision-makers in executing RPM 2026–2035, with the spreadsheet deliberately demoted to a
**one-time input** and **human approval gating every consequential action**.

## 6. Current understanding (evolving)
> _Seeded from confirmed context on 2026-06-27. Expanded as documents are analysed._
- Purpose, users, workflow, risks, technical direction and AI direction captured in Discovery Step 1.
- Authoritative latest KPI source = Google Drive set "TERKINI 19 DISEMBER 2025" (PT PPPM 2026-2035 Teras 1–7),
  used as the **chatbot/RAG knowledge source**.
- Local `Data/` Excel files (PELAN TAKTIKAL JPN + 12 PPD) are the working analysis set.

## 6a. Data governance — two planes (D3A)
- **Operational Data → database:** Pelan Taktikal JPN/PPD (import-once), monthly KPI updates, PIC info,
  budget status, audit trail, reports.
- **Knowledge Data → RAG/knowledge base:** RPM 2026–2035, guidelines, circulars, notes, supporting
  documents, and links (recorded as references, processed by RAG where possible).
- The `Data/` folder currently mixes both classes; they must be routed to the correct plane.

## 6b. Primary view — Teras-centric main dashboard (D3A)
- The main page summarises and maps **all KPIs by the 7 Teras** of RPM 2026–2035 (BR-020).
- Includes per-Teras metrics, a KPI mapping table, charts (cards/tables first, charts later), and an
  **AI summary** answering 7 management questions grounded on operational + knowledge data.
- This requirement must be carried into HMW, BRD, TRD and all architecture documents.

## 6c. CONFIRMED AUTHORITATIVE DECISIONS (B2A — precedence baseline)
> Synchronised 2026-06-27. **These 10 decisions take precedence over any future document
> unless the user explicitly changes them.** Each maps to existing KB rules (no new scope).
1. Main dashboard must **summarise & map all KPIs by Teras 1–7**. → BR-020/021, AD-005
2. Pelan Taktikal JPN & PPD are **initial operational input only**. → BR-001/018, AD-002
3. **Monthly KPI updates entered by KPI PIC through the system**. → BR-002
4. Other documents & **live links are knowledge sources** for RAG, Chatbot, KPI Alignment, Executive Copilot. → BR-019/023, AIR-013/070, AIR-033/034
5. **Operational Data ≠ Knowledge Data** — handled differently (DB vs RAG). → BR-017, AD-004
6. **Budget Intelligence Agent** analyses allocation status & recommends **Low Cost High Impact** alternatives. → BR-010/011, AIR-031
7. **Skills are reusable capabilities used by multiple agents**. → BR-016, AIR-020/021
8. **Groq (dev); OpenAI/Anthropic (prod) via `config.md`**. → TR-001/002/003, AD-001
9. **Human review mandatory** before reports, approvals & official decisions. → BR-015, AIR-001/002, AD-003
10. Process discipline: **Prompt Engineering → HMW → BRD → TRD → Enterprise SDLC before development**. → TR-005, AIR-050

## 7. Out of scope (to be confirmed)
- _Placeholder — confirm during BRD scoping._

## 8. Open context items
- See `QUESTIONS_AND_GAPS.md`.
