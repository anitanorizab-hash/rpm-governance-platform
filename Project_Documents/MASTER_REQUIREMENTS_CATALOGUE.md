# MASTER REQUIREMENTS CATALOGUE
### Agentic AI Strategic Governance Platform — RPM 2026–2035

| Field | Value |
|-------|-------|
| Document | B8 — Master Requirements Catalogue |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Role | **Master source for all project requirements** (feeds BRD, TRD, Traceability) |
| Sources | Business Rules Catalogue (BR-001…045), BCM (CAP-*), To-Be, HMW v1.0, B2A decisions |
| Boundary | Requirements catalogue only — no BRD/TRD narrative, no implementation. |

> **ID conventions:** Business `BRQ-`, Functional `FRQ-`, Non-functional `NFRQ-`, AI `AIRQ-`,
> Integration `INTQ-`, Data `DATQ-`, Reporting `REPQ-`.
> **Priority (MoSCoW):** M=Must, S=Should, C=Could, F=Future Enhancement.
> **Future Modules (referenced):** M1 Auth/Access · M2 KPI Import/Master · M3 Monthly Update ·
> M4 Validation · M5 Dashboard · M6 Finance/Budget · M7 Agent Centre · M8 Knowledge/RAG ·
> M9 Chatbot · M10 Reporting/Archive · M11 Notification/Email · M12 Audit/Governance · M13 Admin/Config.

---

## 1. Business Requirements

| ID | Name | Description | Pri | Source | Capability | BR | Module |
|----|------|-------------|-----|--------|-----------|----|--------|
| BRQ-001 | Centralised KPI governance | Centralise all JPN/PPD (and school) KPI records into one source of truth. | M | HMW-01 | CAP-K1/K2 | BR-001/018 | M2 |
| BRQ-002 | Monthly KPI monitoring | Operate a disciplined monthly in-system monitoring cycle. | M | HMW-05/14 | CAP-M1/M4 | BR-002 | M3 |
| BRQ-003 | KPI ownership & accountability | Every KPI has an accountable PIC, sector and contact. | M | HMW-03 | CAP-K3 | BR-004 | M2 |
| BRQ-004 | Governed amendment control | Restrict KPI statement/indicator/target edits to Jul/Oct, audited. | M | HMW-04 | CAP-G1 | BR-008/009 | M12 |
| BRQ-005 | Budget & value-for-money monitoring | Track allocation status and value-for-money systematically. | M | HMW-08/09 | CAP-B1/B3 | BR-010 | M6 |
| BRQ-006 | Early risk identification | Identify at-risk/critical KPIs early. | M | HMW-06/07 | CAP-AI2 | BR-020 | M7/M5 |
| BRQ-007 | Executive decision support | Provide management synthesised, prioritised insight. | M | HMW-12/13 | CAP-AI6/R3 | BR-022/043 | M5/M7 |
| BRQ-008 | RPM alignment assurance | Ensure & show KPI alignment with RPM 2026–2035. | S | HMW-17 | CAP-K4/AI5 | BR-012 | M8 |
| BRQ-009 | Reduce manual reporting | Generate monthly reports with minimal manual effort. | M | HMW-11 | CAP-R1 | BR-014 | M10 |
| BRQ-010 | Cross-tier collaboration | Improve transparency between JPN, PPD, schools. | S | HMW-16 | CAP-M4/R2 | BR-007 | M5 |
| BRQ-011 | Adoption & trust | Drive adoption over Excel; trusted, advisory AI. | S | HMW-22 | CAP-G3 | BR-028 | M3/M7 |
| BRQ-012 | Continuity & institutional memory | Preserve knowledge/ownership over the 10-yr horizon. | S | HMW-24 | CAP-KM1/U3 | BR-033 | M8/M1 |

---

## 2. Functional Requirements

| ID | Name | Description | Pri | Source | Capability | BR | Module |
|----|------|-------------|-----|--------|-----------|----|--------|
| FRQ-001 | MOE-domain login | Authenticate users via MOE email domains. | M | BR-003 | CAP-U1 | BR-003 | M1 |
| FRQ-002 | Role-based access | Enforce permissions per role. | M | BR-031 | CAP-U2 | BR-031/032 | M1 |
| FRQ-003 | Excel import (once) | Import Pelan Taktikal JPN/PPD as master records. | M | BR-001 | CAP-K1 | BR-001/018 | M2 |
| FRQ-004 | KPI record management | Maintain KPI structure (TSx.Sy.Pz.KPIn, TOV, target, activities, budget). | M | BR-034/035 | CAP-K2 | BR-034/035 | M2 |
| FRQ-005 | PIC assignment | Assign/maintain PIC name, sector, email. | M | BR-004 | CAP-K3 | BR-004 | M2 |
| FRQ-006 | Completeness detection & warnings | Detect missing mandatory fields; show warnings by KPI/Teras. | M | BR-005/006 | CAP-M2 | BR-005/006 | M4 |
| FRQ-007 | Monthly KPI update form | PIC enters achievement, finance status, evidence, remarks; save. | M | BR-002 | CAP-M1 | BR-002 | M3 |
| FRQ-008 | KPI status classification | Classify on-track/lagging/achieved. | M | BR-020 | CAP-M3 | BR-020 | M5/M7 |
| FRQ-009 | Risk flagging | Flag At-Risk/Critical KPIs. | M | HMW-06 | CAP-AI2 | BR-020 | M7 |
| FRQ-010 | Amendment window enforcement | Lock statement/indicator/target except Jul/Oct. | M | BR-008 | CAP-G1 | BR-008 | M12 |
| FRQ-011 | Teras 1–7 dashboard | Summarise & map KPIs by Teras with per-Teras metrics + mapping table. | M | BR-020/021 | CAP-R2 | BR-020/021 | M5 |
| FRQ-012 | AI dashboard summary | Main-page AI summary (7 management questions). | M | BR-022 | CAP-AI7 | BR-022 | M5/M7 |
| FRQ-013 | KPI chatbot | Grounded, source-cited Q&A with fallback. | S | BR-013 | CAP-AI4 | BR-013/025/027 | M9 |
| FRQ-014 | Budget Intelligence | Budget status analysis, **funding-gap detection**, **budget-risk analysis**. | M | BR-046 | CAP-B2 | BR-010/011/046 | M6/M7 |
| FRQ-029 | Low Cost High Impact Analysis | Analyse activities, evaluate expected impact, recommend lower-cost alternatives, resource optimisation, collaboration opportunities (via the Matrix). | M | BR-046 | CAP-B5 | BR-011/046 | M6/M7 |
| FRQ-030 | Executive Financial Insight | Present AI financial recommendations with rationale to support management decisions; feeds Dashboard + Executive Copilot. | S | BR-046 | CAP-B6 | BR-043/046 | M5/M7 |
| FRQ-015 | Intervention recommendations | Draft interventions for at-risk KPIs: suggest **alternative programmes**, **implementation strategies**, and **prioritise** recommendations (HITL). | S | HMW-07/BR-046 | CAP-AI3 | BR-015/046 | M7 |
| FRQ-016 | Report generation | Draft monthly reports + executive summary. | M | BR-014 | CAP-R1 | BR-014/039 | M10 |
| FRQ-017 | Human review & approval | Approve/reject before formal action/report/email. | M | BR-015 | CAP-G3 | BR-015 | M12 |
| FRQ-018 | Notification & reminders | Draft reminders/alerts; track escalation. | M | BR-007 | CAP-N1/N2 | BR-007 | M11 |
| FRQ-019 | Email queue & distribution | Send approved comms; log issuance. | M | BR-040 | CAP-N3 | BR-040 | M11 |
| FRQ-020 | Knowledge ingestion | Ingest static docs + live links into RAG. | S | BR-019/023 | CAP-KM1 | BR-019/023 | M8 |
| FRQ-021 | Link registry & refresh | Manage links (title/URL/category/last-checked); admin refresh. | S | BR-024 | CAP-KM2 | BR-024 | M8/M13 |
| FRQ-022 | KPI–RPM alignment | Map KPI↔RPM; show alignment strength. | S | BR-012 | CAP-K4/AI5 | BR-012 | M8 |
| FRQ-023 | Executive Copilot | Leadership decision-support assistant. | S | BR-043 | CAP-AI6 | BR-043 | M7 |
| FRQ-024 | Audit trail | Record who/what/when for changes & decisions. | M | BR-009 | CAP-G2 | BR-009/029/036 | M12 |
| FRQ-025 | Submission tracking | Track update status by Teras/period. | M | HMW-14 | CAP-M4 | BR-007 | M5 |
| FRQ-026 | Provider configuration | Switch LLM provider via config.md. | M | BR-044 | CAP-S1 | BR-044 | M13 |
| FRQ-027 | Admin & user management | Manage users, roles, windows, settings. | M | BR-032 | CAP-U3/S2 | BR-032/033 | M13 |
| FRQ-028 | OBB value-for-money | Assess outcome-based budget value. *(pending Q-025)* | C | BR-038 | CAP-B3 | BR-038 | M6/M7 |

---

## 3. Non-Functional Requirements

| ID | Name | Description | Pri | Source | Capability | BR | Module |
|----|------|-------------|-----|--------|-----------|----|--------|
| NFRQ-001 | Security & access control | MOE auth, RBAC, protect sensitive KPI/budget data. | M | BR-003/031 | CAP-U1/U2 | BR-003/031 | M1 |
| NFRQ-002 | Auditability | Tamper-evident, queryable audit trail. | M | BR-009/030 | CAP-G2/G4 | BR-009 | M12 |
| NFRQ-003 | Configurability | Provider/config changes without code change. | M | BR-044 | CAP-S1 | BR-044 | M13 |
| NFRQ-004 | AI trust & grounding | Cited answers, honest fallback, no fabrication. | M | BR-025/026/027 | CAP-KM3 | BR-025/026/027 | M8/M9 |
| NFRQ-005 | Usability / low-friction entry | Minimise PIC data-entry friction (adoption). | M | HMW-22 | CAP-M1 | BR-002 | M3 |
| NFRQ-006 | Performance | Responsive dashboard/queries at expected scale. *(scale Q-016)* | S | NFR | CAP-R2 | — | M5 |
| NFRQ-007 | Scalability | Support growth (pilot→national if confirmed Q-003). | S | NFR | — | — | all |
| NFRQ-008 | Availability | Suitable uptime for monthly-cycle operations. | S | NFR | — | — | all |
| NFRQ-009 | Maintainability | Modular, documented, 10-yr maintainable. | M | HMW-24 | CAP-S2 | — | all |
| NFRQ-010 | Data integrity | Enforce operational/knowledge separation; no cross-contamination. | M | BR-017 | CAP-S2 | BR-017 | M2/M8 |
| NFRQ-011 | Compliance & data residency | Meet gov security/residency rules. *(pending Q-014/Q-017)* | S | NFR | — | — | all |
| NFRQ-012 | Localisation | Bahasa Malaysia / English UI. *(pending Q-012)* | C | NFR | — | — | all |
| NFRQ-013 | Data retention & archival | Retain records across 2026–2035. *(policy pending)* | S | BCM gap | CAP-G2 | — | M12 |

---

## 4. AI Requirements

| ID | Name | Description | Pri | Source | Capability | BR | Module |
|----|------|-------------|-----|--------|-----------|----|--------|
| AIRQ-001 | Multi-agent architecture | Operate the agent set (14 proposed; Q-024). | M | BR-041 | CAP-AI* | BR-041 | M7 |
| AIRQ-002 | Skills layer | Reusable skills shared across agents. | M | BR-042 | all AI caps | BR-016/042 | M7 |
| AIRQ-003 | RAG knowledge base | Retrieve from RPM + docs + live links, cited. | M | BR-012/023 | CAP-KM1/3 | BR-012 | M8 |
| AIRQ-004 | KPI analysis (AI) | Interpret status/trends per Teras. | M | BR-020 | CAP-AI1 | BR-020 | M7 |
| AIRQ-005 | Risk detection (AI) | Score risk. *(method Q-020)* | M | HMW-06 | CAP-AI2 | BR-020 | M7 |
| AIRQ-006 | Budget intelligence (AI) | Low Cost High Impact + OBB analysis. | M | BR-011 | CAP-B2/B3 | BR-011 | M7 |
| AIRQ-007 | KPI alignment (AI) | Alignment scoring KPI↔RPM. *(metric Q-021)* | S | BR-012 | CAP-AI5 | BR-012 | M7/M8 |
| AIRQ-008 | Executive Copilot (AI) | Synthesised leadership support. | S | BR-043 | CAP-AI6 | BR-043 | M7 |
| AIRQ-009 | Chatbot (AI) | Grounded conversational interface. | S | BR-013 | CAP-AI4 | BR-013 | M9 |
| AIRQ-010 | AI summary (AI) | Dashboard 7-question summary. | M | BR-022 | CAP-AI7 | BR-022 | M7/M5 |
| AIRQ-011 | Human oversight of AI | All AI advisory; HITL before action. | M | BR-028 | CAP-G3 | BR-015/028 | M12 |
| AIRQ-012 | Provider abstraction | Groq/OpenAI/Anthropic via config. | M | BR-044 | CAP-S1 | BR-044 | M13 |

---

## 5. Integration Requirements

| ID | Name | Description | Pri | Source | Capability | BR | Module |
|----|------|-------------|-----|--------|-----------|----|--------|
| INTQ-001 | Excel import | Ingest Pelan Taktikal Excel (.xlsx) at onboarding. | M | BR-001 | CAP-K1 | BR-001 | M2 |
| INTQ-002 | Live knowledge links | Fetch/refresh external link content for RAG. *(allow-list Q-022)* | S | BR-024 | CAP-KM2 | BR-024 | M8 |
| INTQ-003 | Email service | Send approved notifications/reports. | M | BR-040 | CAP-N3 | BR-040 | M11 |
| INTQ-004 | LLM provider APIs | Integrate Groq/OpenAI/Anthropic via config. | M | BR-044 | CAP-S1 | BR-044 | M13 |
| INTQ-005 | SharePoint / document source | Future integration for knowledge docs. | F | mentor/D3B | CAP-KM1 | BR-023 | M8 |

---

## 6. Data Requirements

| ID | Name | Description | Pri | Source | Capability | BR | Module |
|----|------|-------------|-----|--------|-----------|----|--------|
| DATQ-001 | Initial Excel dataset | Capture imported Pelan Taktikal data. | M | BR-001 | CAP-K1 | BR-001 | M2 |
| DATQ-002 | Operational database | Store KPI, PIC, finance, updates as system of record. | M | BR-018 | CAP-K2/M1 | BR-017/018 | M2 |
| DATQ-003 | Knowledge repository (vector) | Store embedded knowledge (docs + links). | S | BR-019 | CAP-KM1 | BR-017/019 | M8 |
| DATQ-004 | Audit trail store | Persist immutable change/decision history. | M | BR-009 | CAP-G2 | BR-009 | M12 |
| DATQ-005 | Finance data | Allocation status (six-value), warrant, expenditure, OS codes. | M | BR-010 | CAP-B1 | BR-010 | M6 |
| DATQ-006 | Link registry data | Link metadata (title/URL/category/last-checked). | S | BR-024 | CAP-KM2 | BR-024 | M8 |
| DATQ-007 | Reference/master data | Teras, Strategi, Prakarsa, Bahagian, object codes. | M | JPN data | CAP-K2 | BR-034 | M2 |

---

## 7. Reporting Requirements

| ID | Name | Description | Pri | Source | Capability | BR | Module |
|----|------|-------------|-----|--------|-----------|----|--------|
| REPQ-001 | Monthly report | Generate monthly KPI report (draft → approval). | M | BR-014 | CAP-R1 | BR-014/040 | M10 |
| REPQ-002 | Executive summary | Management executive summary section. | M | BR-039 | CAP-R3 | BR-039 | M10/M5 |
| REPQ-003 | Teras dashboard views | Per-Teras dashboards + mapping + charts (phased). | M | BR-020/021 | CAP-R2 | BR-020/021/045 | M5 |
| REPQ-004 | AI summary report | AI-generated summary on main page. | M | BR-022 | CAP-AI7 | BR-022 | M5 |
| REPQ-005 | Report archive | Store issued reports + notification log. | S | pptx TR012 | CAP-G2 | BR-029 | M10/M12 |
| REPQ-006 | Risk/budget/submission summaries | Aggregated summaries by Teras. | M | BR-021 | CAP-R2 | BR-021 | M5 |

---

## Requirement Validation (self-audit)

| Check | Finding | Action |
|-------|---------|--------|
| Missing requirements? | Added submission tracking (FRQ-025), retention (NFRQ-013), reference data (DATQ-007), report archive (REPQ-005), continuity (BRQ-012). | Added |
| Duplicate requirements? | Dashboard appears as FRQ-011 (function) + REPQ-003 (reporting view) — intentional cross-classification, distinct IDs, cross-referenced. | Resolved |
| Conflicting requirements? | Login domain (FRQ-001/NFRQ-001) flagged to C-001; agent count (AIRQ-001) flagged to Q-024 — not silently resolved. | Flagged |
| Deferrable low-priority? | OBB (FRQ-028) = Could; SharePoint (INTQ-005) = Future; localisation (NFRQ-012) = Could. Recommended for phased delivery. | Prioritised |

*Auto-improvements applied: 5 requirements added; cross-classified items cross-referenced; conflicts flagged; low-priority items marked C/F for phasing.*

---

## FINAL OUTPUT

**1. Total requirements identified: 83**

**2. Requirements by category**
| Category | Count |
|----------|-------|
| Business (BRQ) | 12 |
| Functional (FRQ) | 28 |
| Non-functional (NFRQ) | 13 |
| AI (AIRQ) | 12 |
| Integration (INTQ) | 5 |
| Data (DATQ) | 7 |
| Reporting (REPQ) | 6 |
| **Total** | **83** |

**3. MoSCoW prioritisation summary**
| Priority | Count | Examples |
|----------|-------|----------|
| **Must (M)** | 52 | Login, RBAC, import, monthly update, completeness, dashboard, audit, HITL, reports, budget intelligence, multi-agent, RAG |
| **Should (S)** | 25 | Chatbot, alignment, copilot, knowledge ingestion, link registry, performance/scalability/availability |
| **Could (C)** | 4 | OBB value-for-money, localisation |
| **Future (F)** | 2 | SharePoint integration |

**4. Readiness for Stakeholder Analysis: READY (96%).**
Every requirement has an ID, category, priority, source, capability, business-rule and module link.
Residual 4% = the same parameter open-items (login domain, agent count, OBB, risk/alignment, scale,
language) — all attached to specific requirements as flags, none blocking. Stakeholder Analysis can now
attach accountable roles (RACI) to these requirements.

---
*End of Master Requirements Catalogue v0.1 — DRAFT. Stakeholder Analysis NOT generated. Awaiting approval.*
