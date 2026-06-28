# BUSINESS REQUIREMENTS DOCUMENT (BRD)
## Agentic AI Strategic Governance Platform for RPM 2026–2035
### KPI Monitoring · Monthly Update · Budget Intelligence · Intervention · Notification · Reporting · Executive Decision Support

> **Build status:** ✅ **COMPLETE — FROZEN APPROVED BASELINE v1.0** (all parts §1–§30 authored, audited
> [B11-Full], refined, and frozen on 2026-06-27). Reopened only via an explicit, logged change request.

---

# 1. Document Control

| Attribute | Detail |
|-----------|--------|
| Document title | Business Requirements Document (BRD) — Agentic AI Strategic Governance Platform for RPM 2026–2035 |
| Document ID | D2-BRD |
| Version | **1.0 (FROZEN — APPROVED BASELINE)** |
| Date | 2026-06-27 |
| Frozen on | 2026-06-27 by user approval (Freeze Gate 1) |
| Status | **APPROVED · FROZEN** — Draft → Audited (B11-Full) → Refined → **FROZEN ✅** |
| Classification | Government — Official (final confirmation vs MOE data-classification policy pending Q-017) |
| Change control | Reopened only via an explicit, logged change request (CHANGE_LOG.md). |
| Owner | Business Analysis / Solution Architecture team |
| Prepared for | Ministry of Education Malaysia (Kementerian Pendidikan Malaysia) — JPN / PPD |
| Foundation artefacts | HMW v1.0 (frozen), As-Is (B4), To-Be (B5), Business Capability Model (B6), Business Rules Catalogue (B7), Master Requirements Catalogue (B8), BRD Outline (B9) |
| Precedence | Subordinate to the B2A Authoritative Decisions; consistent with the frozen HMW. |

### 1.1 Approval & Sign-off
| Role | Name | Responsibility | Signature | Date |
|------|------|----------------|-----------|------|
| Project Sponsor | _TBC_ | Approve business intent & funding | | |
| Business Owner (JPN) | User (suzila@iegcampus.com) | Approve business requirements | **Approved** | 2026-06-27 |
| Solution Architect | _TBC_ | Endorse feasibility & traceability | | |
| AI Solution Designer | _TBC_ | Endorse AI scope & governance | | |
| Quality / Audit | _TBC_ | Confirm governance & auditability | | |

### 1.2 Distribution List
JPN management; PPD administrators; sector heads; project steering committee; AI/solution team;
internal audit/oversight. *(Final list to be confirmed.)*

### 1.3 Change Control
This BRD follows the project freeze discipline: **Draft → Audit → Revise → Freeze**. Once frozen, it is
reopened only via an explicit, logged change request recorded in `CHANGE_LOG.md`. All downstream
documents (TRD, architecture) must remain consistent with the frozen BRD.

---

# 2. Version History

| Version | Date | Author | Part(s) | Summary of change |
|---------|------|--------|---------|-------------------|
| 0.1 | 2026-06-27 | BA/Architecture team | Part 1 | Initial draft: Document Control … Project Scope. |
| 0.2–0.5 | 2026-06-27 | BA/Architecture team | Parts 2–5 | Stakeholders, As-Is/To-Be, Capabilities, Rules, Functional/Non-Functional, Roles, Dashboard, AI Features/Agents/Skills/RAG, FDS, Reporting, Notifications, Security, Constraints, Assumptions, Risks, Success Criteria, Traceability, Glossary, Appendices. |
| 0.6 | 2026-06-27 | BA/Architecture team | All | B11-Full audit + adopted resolutions (Appendix H); FDS consistency; ASM-11 added. |
| **1.0** | **2026-06-27** | **BA/Architecture team** | **All** | **Finalised, Approved and FROZEN as the official Business Requirements Baseline.** |

---

# 3. Executive Summary

The Ministry of Education Malaysia is executing **RPM 2026–2035**, a ten-year national education roadmap
structured around **seven strategic pillars (Teras Strategik)** and delivered through tactical plans
(**Pelan Taktikal**) at State (**JPN**) and District (**PPD**) levels, cascading to schools. Today, this
roadmap is monitored through fragmented Excel files exchanged by email, with manual consolidation,
checking, follow-up and reporting. This approach is slow, error-prone, difficult to audit, and provides
limited real-time visibility to management — a significant risk for a strategic programme spanning a
decade of staff and leadership change.

This document specifies the business requirements for an **Agentic AI Strategic Governance Platform** that
replaces the spreadsheet-and-email process with a **single, audit-grade system of record** augmented by an
**agentic AI layer**. The platform centralises KPI data (imported once from the tactical plans),
enforces disciplined **monthly in-system updates by each KPI's Person-in-Charge (PIC)**, detects missing
information, monitors performance and budget, and surfaces risks and recommendations — while keeping
**humans in control of every formal action, report approval and communication** (AI is advisory only).

A **Teras 1–7 dashboard** provides the primary management view, complemented by an **AI-generated
executive summary**. A **knowledge layer (RAG)** grounded in RPM 2026–2035 and supporting documents and
links powers a **KPI chatbot**, **KPI–RPM alignment**, and an **Executive Copilot** for decision support.
A **Budget Intelligence** capability applies the **Low Cost High Impact Matrix** to guide value-for-money
decisions. Operational data and knowledge data are kept on **strictly separate planes**, and the LLM
provider is **configuration-driven** (Groq for development; OpenAI or Anthropic for production).

The solution is defined by **83 requirements** across seven categories and governed by **45 business
rules**, all traceable to the frozen **How-Might-We** problem framing. Delivery is incremental and
prioritised (MoSCoW), enabling a focused first release followed by phased enhancements. The expected
outcomes are: a single source of truth, enforced data completeness, real-time Teras-level visibility,
early risk detection, systematic budget oversight, reduced manual reporting effort, assured RPM
alignment, and trustworthy, auditable AI-assisted decision support.

---

# 4. Project Background

### 4.1 Strategic context
RPM 2026–2035 is organised into **7 Teras Strategik**, each decomposed into strategies/enablers
(*Strategi/Enabler*), initiatives (*Prakarsa*) and KPIs. Each KPI is identified by a structured code
(`TSx.Sy.Pz.KPIn`) and carries a baseline (**TOV / Pencapaian 2025**, or a "KPI Baharu" marker for new
KPIs), a target (**Sasaran 2026**), main and supporting activities, a responsible division (**Bahagian**)
and PIC, and a budget broken down by government object codes (**OS21000…OS42000**) with monthly
projections (Jan–Dec).

### 4.2 Organisational context
Delivery spans three governance tiers — **JPN (state) → PPD (district) → School**. The working data set
analysed for this project covers the **State of Perak** (one JPN tactical plan and twelve PPD district
plans, each covering Teras 1–7). *Working assumption: initial deployment targets Perak as a pilot ahead
of potential national rollout — to be confirmed (Q-003).*

### 4.3 Problem context (As-Is summary)
The current process relies on distributing Excel templates, manual completion by PICs/PPDs, email
submission, manual consolidation into a master workbook, manual completeness checks, manual follow-up,
and manual monthly report compilation for management review. The detailed current-state analysis is in
the approved **As-Is Business Process (B4)**; its principal pain points are fragmented/duplicate data, missing
information, late submission, no audit trail, limited executive visibility, unsystematic budget
monitoring, difficult RPM alignment, and absence of intelligent recommendations.

### 4.4 Rationale for the project
A ten-year strategic roadmap requires continuity, auditability and real-time governance that a
spreadsheet-based process cannot sustain. The platform is needed to institutionalise disciplined,
transparent, AI-assisted execution of RPM 2026–2035 across JPN, PPD and schools, with governance and
human oversight appropriate to a government environment.

### 4.5 Reference documents
This BRD consolidates and must remain consistent with: the frozen **HMW (D1)**, **As-Is (B4)**,
**To-Be (B5)**, **Business Capability Model (B6)**, **Business Rules Catalogue (B7)** and **Master
Requirements Catalogue (B8)**, governed by the **B2A Authoritative Decisions**.

---

# 5. Business Objectives

The platform shall achieve the following confirmed business objectives (traced to HMW success criteria
and Business Requirements BRQ-001…012):

| # | Objective | Traces to |
|---|-----------|-----------|
| OBJ-01 | Establish a single, authoritative source of truth for all JPN/PPD (and school) KPI data. | BRQ-001, HMW-01 |
| OBJ-02 | Enforce disciplined monthly KPI monitoring entered in-system by PICs. | BRQ-002, HMW-05/14 |
| OBJ-03 | Ensure every KPI has clear ownership (PIC, sector, contact). | BRQ-003, HMW-03 |
| OBJ-04 | Govern KPI amendments (July/October only) with a complete audit trail. | BRQ-004, HMW-04 |
| OBJ-05 | Monitor budget allocation status and value-for-money systematically. | BRQ-005, HMW-08/09 |
| OBJ-06 | Identify at-risk and critical KPIs early to enable timely intervention. | BRQ-006, HMW-06/07 |
| OBJ-07 | Provide management with synthesised, prioritised executive decision support. | BRQ-007, HMW-12/13 |
| OBJ-08 | Ensure and demonstrate KPI alignment with RPM 2026–2035. | BRQ-008, HMW-17 |
| OBJ-09 | Reduce manual reporting effort through automated, human-approved monthly reports. | BRQ-009, HMW-11 |
| OBJ-10 | Improve transparency and collaboration across JPN, PPD and schools. | BRQ-010, HMW-16 |
| OBJ-11 | Drive adoption of the platform over Excel through trusted, advisory AI. | BRQ-011, HMW-22 |
| OBJ-12 | Preserve institutional knowledge and continuity over the 10-year horizon. | BRQ-012, HMW-24 |

### 5.1 Measurable success indicators (high-level)
Single source of truth established; near-zero missing-information warnings; on-time monthly submission
rate; early-risk detection before target slippage; systematic budget status coverage; reduced report
compilation time; demonstrable RPM alignment. *(Detailed success criteria appear in Part 5, §27.)*

---

# 6. Project Scope

### 6.1 Scope statement
The project shall deliver an Agentic AI Strategic Governance Platform that imports the Pelan Taktikal
(once), stores KPI data as the system of record, enables monthly in-system KPI updates by PICs, detects
incomplete information, monitors performance and budget, applies AI-assisted analysis/risk/budget
intelligence, provides a Teras 1–7 dashboard and AI/executive summaries, offers a RAG-grounded chatbot,
KPI–RPM alignment and an Executive Copilot, generates human-approved monthly reports, and issues
human-approved notifications — all under role-based access restricted to MOE accounts, with a complete
audit trail and configuration-driven AI provider selection.

### 6.2 In Scope
- One-time Excel import of Pelan Taktikal JPN and PPD (BR-001/018).
- Operational database as the system of record; in-system monthly KPI updates by PIC (BR-002).
- Completeness detection and warnings; PIC reminders (BR-005/006/007).
- Governed amendment windows (July/October) with audit trail (BR-008/009).
- Finance allocation status (six-value vocabulary) and Budget Intelligence via Low Cost High Impact (BR-010/011).
- Teras 1–7 dashboard with per-Teras summaries, KPI mapping table, charts (phased), and AI summary (BR-020/021/022).
- Knowledge layer (RAG) over RPM 2026–2035 + static documents + live links; KPI chatbot; KPI–RPM alignment; Executive Copilot (BR-012/013/019/023–027/043).
- Multi-agent + skills layer (BR-016; up to 14 agents — roster pending Q-024).
- Human-in-the-loop approval before formal action/report/email (BR-015).
- MOE-domain login + RBAC (BR-003/031/032).
- Monthly report generation; notifications and approved distribution (BR-014/040).
- Configuration-driven LLM provider — Groq (dev), OpenAI/Anthropic (prod) via `config.md` (BR-044).

### 6.3 Out of Scope (for confirmation in Part 5)
- Replacement of upstream national planning systems that originate the RPM/PPPM roadmap.
- Automated write-back to external finance systems (allocation figures entered/managed in-platform unless integration is later confirmed, Q-009).
- Fully autonomous AI actions (explicitly excluded — AI is advisory only, BR-028).
- Public/external (non-MOE) user access (BR-003).
- Mobile-native applications (unless later prioritised).

### 6.4 Release & phasing (MoSCoW-aligned)
- **Release 1 (Must):** auth/RBAC, Excel import, KPI master records, monthly update, completeness/warnings, Teras dashboard, KPI status/risk, audit trail, human review, monthly report, notifications, Budget Intelligence (Low Cost High Impact), core agents, RAG foundation.
- **Release 2 (Should):** chatbot, KPI–RPM alignment, Executive Copilot, live-link knowledge ingestion + link registry, submission analytics.
- **Later (Could/Future):** OBB value-for-money, localisation, SharePoint integration.

### 6.5 Scope assumptions & constraints
Scope is bounded by the project **Constraints (CON-01…10)** and **Assumptions** detailed in Part 5.
Key working assumptions: Perak pilot scope (Q-003), schools as a reporting tier in Release 1 (Q-002),
RPM ≡ PPPM terminology (Q-001), Bahasa Malaysia as primary content language (Q-012).

---

## Self-Review — Part 1

| Check | Finding | Action |
|-------|---------|--------|
| Missing requirements? | Scope §6.2 cross-checked against B8 categories; all Must/Should items represented; Could/Future placed in §6.4. | OK |
| Duplicate content? | Detailed success criteria deferred to Part 5 (only high-level here); As-Is summarised, not reproduced (full in B4). | Avoided duplication |
| Inconsistencies? | Objectives, scope and rules cross-referenced to BR/BRQ/HMW IDs; consistent with B2A decisions. | None found |
| Missing business rules? | Scope cites the governing BRs; full catalogue appears in Part 3. | OK |
| Missing AI features? | AI scope (agents, skills, RAG, chatbot, alignment, copilot, budget intelligence) included in §6.2; detail in Parts 4–5. | OK |
| Open parameters | Login domain, agent roster, OBB, risk/alignment, pilot/school, naming, language — flagged inline as assumptions, not guessed. | Flagged |

*Improvements applied: phasing added to scope; classification flagged to Q-017; out-of-scope items made explicit to prevent scope creep.*

---

**— END OF PART 1 — (APPROVED 2026-06-27)**
*Part 1 covers: Document Control · Version History · Executive Summary · Project Background · Business Objectives · Project Scope.*

---

# 7. Stakeholder Analysis

This section identifies the stakeholders and user roles of the platform, their interests, influence and
desired outcomes, and assigns accountability for key processes. It consolidates HMW §3 (frozen) and the
roles defined in the Business Capability Model (B6). Role permissions are specified in Part 4 (§User
Roles & Permissions); this section establishes the stakeholder landscape and RACI.

### 7.1 Stakeholder register
| ID | Stakeholder / Role | Tier | Interest | Influence | Desired outcome |
|----|--------------------|------|----------|-----------|-----------------|
| ST-01 | **Super Admin / Governance Admin** | Platform | Govern users, windows, links, config, audit | High | Controlled, auditable, well-governed platform |
| ST-02 | **JPN Administrator** | State | State-wide KPI oversight & consolidation | High | Real-time state Teras view; less manual effort |
| ST-03 | **Sector Administrator / Bahagian** | State/National | KPIs for their sector/division | Medium-High | Clear sector ownership and early intervention |
| ST-04 | **PPD Administrator** | District | District KPI accuracy & oversight | Medium | Accurate district KPIs; visibility of gaps |
| ST-05 | **KPI PIC** | Operational | Own & update assigned KPI | Medium (high volume) | Simple guided updates; clarity on what's due |
| ST-06 | **Finance Officer** | State/District | Budget/OBB monitoring | Medium | Systematic allocation & value-for-money view |
| ST-07 | **Executive / State Management** | Executive | Strategic decisions | High | Synthesised insight; faster decisions |
| ST-08 | **Ministry (MOE) Leadership** | National | Roadmap accountability | High | Auditable, aligned roadmap progress |
| ST-09 | **Implementing Divisions (Bahagian Pelaksana)** | National | KPI delivery accountability | Medium-High | Clear division-level ownership/visibility |
| ST-10 | **Internal Audit / Oversight** | Assurance | Governance & compliance | Medium | Built-in, queryable audit trail |
| ST-11 | **IT / Platform Operations** | Support | Run & maintain the platform | Medium | Stable, configurable, maintainable platform |
| ST-12 | **Schools** *(reporting tier; scope Q-002)* | School | Provide delivery evidence | Low-Medium | Low-effort, clear contribution |

### 7.2 Stakeholder influence / interest summary
- **High influence + high interest (manage closely):** Super Admin, JPN Admin, Executive/State Management, Ministry Leadership.
- **Medium influence (keep satisfied/informed):** Sector Admin, PPD Admin, Finance, Implementing Divisions, Internal Audit, IT Ops.
- **High volume operational (enable & support):** KPI PIC — adoption-critical (OBJ-11).

### 7.3 RACI for key processes
*(R=Responsible, A=Accountable, C=Consulted, I=Informed)*

| Process | Super Admin | JPN Admin | Sector/PPD Admin | PIC | Finance | Executive | Audit |
|---------|-------------|-----------|------------------|-----|---------|-----------|-------|
| Initial Excel import | A/R | C | I | I | I | I | I |
| PIC assignment | A | R | R | I | – | I | I |
| Monthly KPI update | I | I | C | **A/R** | C | I | I |
| Completeness/warnings response | I | C | C | **R** | – | I | I |
| KPI amendment (Jul/Oct) | A | R | C | C | – | I | C |
| Budget intelligence review | I | C | C | C | **R** | A | I |
| Monthly report approval | I | R | C | I | C | **A** | I |
| Notification/email sending | I | A/R | C | I | – | C | I |
| Knowledge link management | **A/R** | C | – | – | – | I | I |
| Provider/config change | **A/R** | I | – | – | – | I | I |
| Audit review | C | I | I | I | I | I | **A/R** |

> Note: every "approve/send" cell with **A** is a **human-in-the-loop gate** (BR-015); no agent holds an A or R for a formal action.

---

# 8. Current Business Process (As-Is)

*This section summarises the approved As-Is Business Process Analysis (B4). The full analysis is the
authoritative reference; it is not reproduced in full here to avoid duplication.*

### 8.1 Summary
KPI monitoring for RPM 2026–2035 is currently a **manual, spreadsheet-and-email process** across
JPN → PPD → School. The Pelan Taktikal Excel workbooks serve simultaneously as template, data store and
reporting source. JPN prepares and distributes templates; PICs/PPDs complete them manually; returns are
emailed back and consolidated by hand into a master workbook; completeness is checked visually; gaps are
chased manually; monthly reports are compiled by hand for management review.

### 8.2 Key As-Is characteristics
- Excel is the system of record; many copies and versions circulate (no single source of truth).
- Monthly updates overwrite prior values (no inherent history/audit).
- Completeness depends on individual reviewer diligence.
- Risk, budget and alignment assessed subjectively, if at all.
- Reporting is periodic and backward-looking; figures are not traceable to source.

### 8.3 Principal pain points (ref. B4 AS-PP01–14, mapped to HMW PP01–18)
Manual effort; fragmented/duplicate data; missing information; late submission; difficult progress
tracking; no audit trail; limited executive visibility; difficult RPM alignment; budget-monitoring
challenges; no intelligent recommendations; manual reminders; weak access control; continuity risk;
inconsistent completeness checks.

### 8.4 Principal risks (ref. B4 AS-R01–10)
Data integrity (version/copy errors); no audit trail; late/incomplete data; key-person dependency;
security exposure; delayed intervention; budget mismanagement; RPM misalignment; audit/compliance
findings; reporting inconsistency.

---

# 9. Future Business Process (To-Be)

*This section summarises the approved To-Be Business Process Design (B5) — the master workflow blueprint.
The full design is the authoritative reference.*

### 9.1 Future operational model
The platform imports the Pelan Taktikal once, stores KPI data in an **operational database** (single
source of truth), and runs all subsequent activity in-system. An **agentic AI layer** monitors,
analyses, recommends and drafts; a **knowledge layer (RAG)** grounds a chatbot, KPI–RPM alignment and an
Executive Copilot; a **Teras 1–7 dashboard** provides the primary management view; and **humans approve
every formal action, report and communication**. Operational and knowledge data are kept on separate
planes; the LLM provider is configuration-driven (Groq dev; OpenAI/Anthropic prod).

### 9.2 Seven-phase target workflow (ref. B5)
1. **Phase 1 — Import & Validation:** Excel (JPN+PPD) → Data Integration Agent → Validation Agent → operational database (Excel becomes input-only).
2. **Phase 2 — PIC Assignment & Completeness:** assign PIC (name/sector/email); Completeness Agent detects missing fields and raises warnings; PICs complete; KPIs become "ready for monitoring."
3. **Phase 3 — Monthly KPI Update:** PIC logs in (MOE auth, RBAC) → updates achievement, finance status (six-value), evidence, remarks → saves (audited). Statement/indicator/target locked except July/October.
4. **Phase 4 — AI Processing (advisory):** Validation → KPI Analysis → Risk → Financial Monitoring → Budget Intelligence (Low Cost High Impact / OBB) → Intervention → Notification (draft) → Audit.
5. **Phase 5 — Knowledge Layer (RAG):** documents + RPM + live links → chunk → embed → vector DB → Chatbot (cited) / Knowledge Alignment / Executive Copilot.
6. **Phase 6 — Dashboard:** per-Teras count, achievement, risk, missing info, budget, submission, Low Cost High Impact summary, alignment strength, AI summary, mapping table, executive summary.
7. **Phase 7 — Monthly Report & Distribution:** Report Generation Agent drafts → Human Review → Approval → Email Queue → Distribution (audited).

### 9.3 Cross-cutting controls
Human-in-the-loop gate before every formal action; RBAC on MOE domains; complete audit trail; governed
amendment windows; configuration-driven provider; strict operational/knowledge data separation.

### 9.4 Benefits vs As-Is
Each As-Is pain point (AS-PP01–14) is addressed by a To-Be capability — single source of truth, enforced
completeness, real-time Teras visibility, audit trail, early risk detection, systematic budget oversight,
automated reminders, RAG-grounded knowledge, RBAC, and durable institutional memory. *(Full mapping in B5 §8.)*

---

## Self-Review — Part 2

| Check | Finding | Action |
|-------|---------|--------|
| Missing stakeholders? | All 12 from HMW/BCM included, incl. Implementing Divisions, Audit, IT Ops, Schools. | OK |
| Duplicate content? | As-Is/To-Be summarised with explicit reference to B4/B5; not reproduced in full. | Avoided |
| Inconsistencies? | RACI consistent with HITL (BR-015) — no agent holds A/R for formal actions; tiers consistent with Part 1 scope. | None |
| Missing business rules? | As-Is/To-Be reference governing BRs; full catalogue in Part 3. | OK |
| Missing AI features? | To-Be §9.2 lists all agents/skills/RAG; detail in Part 4. | OK |
| Open parameters | School tier (Q-002), pilot scope (Q-003) flagged; RACI uses confirmed roles. | Flagged |

*Improvements applied: added influence/interest classification and a full RACI; cross-referenced As-Is/To-Be to source documents to prevent duplication.*

---

**— END OF PART 2 — (APPROVED 2026-06-27)**
*Part 2 covers: Stakeholder Analysis · As-Is Business Process · To-Be Business Process.*

---

# 10. Business Capability Model

*Summarises the approved Business Capability Model (B6). Capabilities describe **what** the platform must
enable, independent of implementation. Full detail (purpose, value, users, I/O, dependencies, maturity)
is in B6.*

### 10.1 Capability domains
| Domain | Capabilities (IDs) |
|--------|--------------------|
| D1 Governance Management | CAP-G1 Amendment Control · CAP-G2 Audit Trail · CAP-G3 Human-in-the-Loop · CAP-G4 Compliance/Oversight |
| D2 KPI Management | CAP-K1 Import · CAP-K2 Definition/Structure · CAP-K3 Ownership · CAP-K4 RPM Alignment |
| D3 Monthly Monitoring | CAP-M1 In-System Update · CAP-M2 Completeness · CAP-M3 Status · CAP-M4 Submission Tracking |
| D4 Budget & Financial | CAP-B1 Allocation Status · CAP-B2 Budget Intelligence (Low Cost High Impact) · CAP-B3 OBB Value-for-Money |
| D5 Knowledge Management | CAP-KM1 Ingestion (static+live) · CAP-KM2 Link Registry/Freshness · CAP-KM3 Retrieval+Citation |
| D6 AI Decision Support | CAP-AI1 Analysis · AI2 Risk · AI3 Intervention · AI4 Chatbot · AI5 Alignment · AI6 Copilot · AI7 AI Summary |
| D7 Reporting & Analytics | CAP-R1 Monthly Report · CAP-R2 Teras Dashboard · CAP-R3 Executive Insight |
| D8 User & Security | CAP-U1 Authentication · CAP-U2 RBAC · CAP-U3 Access Governance |
| D9 Notification & Comms | CAP-N1 Reminders · CAP-N2 Alert/Escalation · CAP-N3 Approved Distribution |
| D10 System Administration | CAP-S1 Provider Config · CAP-S2 Platform/Data-Plane Admin |

### 10.2 Capability-to-objective alignment
Every business objective (OBJ-01…12) is served by one or more capabilities: e.g. OBJ-01 (single source of
truth) ← CAP-K1/K2; OBJ-05 (budget) ← CAP-B1/B2/B3; OBJ-07 (executive support) ← CAP-AI6/R3; OBJ-04
(governed amendment) ← CAP-G1/G2. Full capability traceability is maintained in `TRACEABILITY_REGISTER.md`.

---

# 11. Business Rules

The platform shall enforce the **45 confirmed business rules** consolidated in the approved Business Rules
Catalogue (B7). Rules are listed here by domain and ID; the catalogue remains the authoritative source.
Rules BR-028…045 are formalisations of decisions already confirmed across HMW/To-Be/BCM.

### 11.1 Governance rules
- **BR-015** Human review required before formal action, report approval and email sending.
- **BR-028** AI recommendations are advisory only; agents propose, humans dispose.
- **BR-009** All amendments saved in an audit trail (who/what/when).
- **BR-029** Every consequential AI output and human decision is logged.
- **BR-030** Platform supports audit/oversight querying for assurance.

### 11.2 User access rules
- **BR-003** Login restricted to `@moe.gov.my` and `@moe-dl.edu.my`. *(domain count pending C-001/Q-023)*
- **BR-031** Access governed by role-based access control (RBAC).
- **BR-032** Permissions differ by role (Super Admin … PIC … Executive … Audit).
- **BR-033** Access provisioning supports onboarding/offboarding and delegation/acting-officer.

### 11.3 KPI management rules
- **BR-001** Excel used for initial input only. · **BR-018** Import once; database is working source.
- **BR-002** Monthly updates entered only in-system by the PIC.
- **BR-004** Every KPI has PIC name, sector and email.
- **BR-005** Detect incomplete information. · **BR-006** Missing mandatory fields trigger warnings.
- **BR-034** KPI structured by Teras→Strategi/Enabler→Prakarsa→KPI (`TSx.Sy.Pz.KPIn`).
- **BR-035** Each KPI carries TOV (or "KPI Baharu"), target, activities, Bahagian/PIC, budget.

### 11.4 Amendment rules
- **BR-008** KPI Statement, Indicator and Target amendable only in July and October.
- **BR-009** All amendments audited. · **BR-036** All changes traceable (before/after, actor, time, reason).

### 11.5 Budget rules
- **BR-010** Allocation status ∈ {received, will be received, pending, not received, not required, insufficient}.
- **BR-011** Budget Intelligence must use the Low Cost High Impact Matrix.
- **BR-037** Budget Intelligence outputs advisory; human review before implementation.
- **BR-038** OBB value-for-money assessed where applicable. *(definition pending Q-025)*

### 11.6 Knowledge rules
- **BR-017** Operational Data and Knowledge Data are separate (DB vs RAG).
- **BR-019** Knowledge documents/links processed into RAG, never as KPI input.
- **BR-012** RAG uses RPM 2026–2035 as the main reference document.
- **BR-023** Two source types: Static + Live/Updated. · **BR-024** Link metadata + admin refresh; prefer trusted.
- **BR-025** Chatbot cites sources used. · **BR-026** Inaccessible source → clear message, never guess.
- **BR-027** Fixed fallback: "I cannot find this information in the available KPI data or knowledge sources."

### 11.7 Reporting rules
- **BR-014** Generate monthly reports. · **BR-039** Reports include executive summaries.
- **BR-040** Reports/comms follow draft → human review → approval → email queue → distribution.

### 11.8 AI rules
- **BR-016** Include an agents and skills layer. · **BR-041** Multi-agent architecture (14 proposed; Q-024).
- **BR-042** Skills are reusable across agents. · **BR-013** Provide a KPI chatbot (RAG-grounded).
- **BR-043** Executive Copilot provides leadership decision support.
- **BR-044** Provider switching via `config.md`: Groq (dev); OpenAI/Anthropic (prod).

### 11.9 Dashboard rules
- **BR-020** Main dashboard summarises & maps all KPIs by Teras 1–7.
- **BR-021** Per-Teras metrics + KPI mapping table + distribution chart.
- **BR-022** Main-page AI summary answering the 7 management questions.
- **BR-045** Charts may be phased (cards/tables first). · **BR-007** PIC reminders for incomplete data/updates.

> **Open contradictions flagged (not resolved here):** C-001 login domain (BR-003); C-002 agent count (BR-041).

---

# 12. Functional Requirements

The platform shall satisfy the following functional requirements (from the approved Master Requirements
Catalogue B8). Priority: M=Must, S=Should, C=Could. Each traces to a business rule and capability.

| ID | Requirement | Description | Pri | BR | Capability |
|----|-------------|-------------|-----|----|-----------|
| FRQ-001 | MOE-domain login | Authenticate users via MOE email domains only. | M | BR-003 | CAP-U1 |
| FRQ-002 | Role-based access | Enforce permissions per role (per §17 matrix). | M | BR-031/032 | CAP-U2 |
| FRQ-003 | Excel import (once) | Import Pelan Taktikal JPN/PPD as master records at onboarding. | M | BR-001/018 | CAP-K1 |
| FRQ-004 | KPI record management | Maintain KPI structure (code, TOV, target, activities, budget). | M | BR-034/035 | CAP-K2 |
| FRQ-005 | PIC assignment | Assign/maintain PIC name, sector, email per KPI. | M | BR-004 | CAP-K3 |
| FRQ-006 | Completeness detection & warnings | Detect missing mandatory fields; warn by KPI/Teras. | M | BR-005/006 | CAP-M2 |
| FRQ-007 | Monthly KPI update | PIC enters achievement, finance status, evidence, remarks; save (audited). | M | BR-002 | CAP-M1 |
| FRQ-008 | KPI status classification | Classify on-track / lagging / achieved. | M | BR-020 | CAP-M3 |
| FRQ-009 | Risk flagging | Flag At-Risk / Critical KPIs. *(method pending Q-020)* | M | BR-020 | CAP-AI2 |
| FRQ-010 | Amendment window enforcement | Lock statement/indicator/target except July/October. | M | BR-008 | CAP-G1 |
| FRQ-011 | Teras 1–7 dashboard | Summarise & map KPIs by Teras with per-Teras metrics + mapping table. | M | BR-020/021 | CAP-R2 |
| FRQ-012 | AI dashboard summary | Main-page AI summary (7 management questions). | M | BR-022 | CAP-AI7 |
| FRQ-013 | KPI chatbot | Grounded, source-cited Q&A with fixed fallback. | S | BR-013/025/027 | CAP-AI4 |
| FRQ-014 | Budget Intelligence **(FDS)** | Budget status analysis, funding-gap detection, budget-risk analysis. | M | BR-010/011/046 | CAP-B2 |
| FRQ-015 | Intervention Recommendation **(FDS)** | Draft interventions for at-risk KPIs: alternative programmes, implementation strategies, prioritisation (human-reviewed). | S | BR-015/046 | CAP-AI3 |
| FRQ-016 | Report generation | Draft monthly report + executive summary. | M | BR-014/039 | CAP-R1 |
| FRQ-017 | Human review & approval | Approve/reject before formal action/report/email. | M | BR-015 | CAP-G3 |
| FRQ-018 | Notification & reminders | Draft reminders/alerts; track escalation. | M | BR-007 | CAP-N1/N2 |
| FRQ-019 | Email queue & distribution | Send approved comms; log issuance. | M | BR-040 | CAP-N3 |
| FRQ-020 | Knowledge ingestion | Ingest static docs + live links into RAG. | S | BR-019/023 | CAP-KM1 |
| FRQ-021 | Link registry & refresh | Manage links (title/URL/category/last-checked); admin refresh. | S | BR-024 | CAP-KM2 |
| FRQ-022 | KPI–RPM alignment | Map KPI↔RPM; show alignment strength. *(metric pending Q-021)* | S | BR-012 | CAP-K4/AI5 |
| FRQ-023 | Executive Copilot | Leadership decision-support assistant. | S | BR-043 | CAP-AI6 |
| FRQ-024 | Audit trail | Record who/what/when for changes & decisions. | M | BR-009/029/036 | CAP-G2 |
| FRQ-025 | Submission tracking | Track update status by Teras/period. | M | BR-007 | CAP-M4 |
| FRQ-026 | Provider configuration | Switch LLM provider via `config.md`. | M | BR-044 | CAP-S1 |
| FRQ-027 | Admin & user management | Manage users, roles, windows, settings. | M | BR-032/033 | CAP-U3/S2 |
| FRQ-028 | OBB value-for-money **(FDS)** | Assess outcome-based budget value within FDS & budget governance (method in TRD). | C | BR-038/046 | CAP-B3 |
| FRQ-029 | Low Cost High Impact Analysis **(FDS)** | Analyse activities, evaluate impact, recommend lower-cost alternatives, resource optimisation, collaboration opportunities. | M | BR-011/046 | CAP-B5 |
| FRQ-030 | Executive Financial Insight **(FDS)** | Present AI financial recommendations with rationale; feeds Dashboard + Executive Copilot. | S | BR-043/046 | CAP-B6 |

---

# 13. Non-Functional Requirements

The platform shall meet the following non-functional requirements (quality attributes).

| ID | Requirement | Description | Pri | BR/Source | Capability |
|----|-------------|-------------|-----|-----------|-----------|
| NFRQ-001 | Security & access control | MOE auth, RBAC, protect sensitive KPI/budget data. | M | BR-003/031 | CAP-U1/U2 |
| NFRQ-002 | Auditability | Tamper-evident, queryable audit trail. | M | BR-009/030 | CAP-G2/G4 |
| NFRQ-003 | Configurability | Provider/config changes without code change. | M | BR-044 | CAP-S1 |
| NFRQ-004 | AI trust & grounding | Cited answers, honest fallback, no fabrication. | M | BR-025/026/027 | CAP-KM3 |
| NFRQ-005 | Usability / low-friction entry | Minimise PIC data-entry friction (adoption-critical). | M | OBJ-11 | CAP-M1 |
| NFRQ-006 | Performance | Responsive dashboard/queries at expected scale. *(scale Q-016)* | S | NFR | CAP-R2 |
| NFRQ-007 | Scalability | Support growth (pilot → national if confirmed, Q-003). | S | NFR | — |
| NFRQ-008 | Availability | Suitable uptime for monthly-cycle operations. | S | NFR | — |
| NFRQ-009 | Maintainability | Modular, documented, maintainable over 10-year horizon. | M | OBJ-12 | CAP-S2 |
| NFRQ-010 | Data integrity | Enforce operational/knowledge separation; no cross-contamination. | M | BR-017 | CAP-S2 |
| NFRQ-011 | Compliance & data residency | Meet government security/residency rules. *(pending Q-014/Q-017)* | S | NFR | — |
| NFRQ-012 | Language & localisation | UI & reports support **English as primary development language**; future localisation (e.g. Bahasa Malaysia) allowed (resolved Q-012). Source content remains in its original language. | M (English) / C (localisation) | NFR | — |
| NFRQ-013 | Data retention & archival | Retain records across 2026–2035. *(policy pending)* | S | BCM gap | CAP-G2 |

---

## Self-Review — Part 3

| Check | Finding | Action |
|-------|---------|--------|
| Missing requirements? | All 28 FRQ + 13 NFRQ from B8 represented; none dropped. | OK |
| Duplicate requirements? | Dashboard (FRQ-011) vs reporting view (REPQ, Part 5) cross-classified, distinct IDs. | Noted |
| Conflicting requirements? | Login domain (FRQ-001/NFRQ-001 ← C-001) and agent count (BR-041 ← C-002) flagged, not resolved. | Flagged |
| Missing business rules? | All 45 rules listed by domain & ID; catalogue (B7) authoritative. | OK |
| Missing AI features? | FRQ-013/014/015/022/023 + AI rules cover chatbot, budget intelligence, intervention, alignment, copilot; full AI detail in Part 4. | OK |
| Traceability | Every FRQ/NFRQ carries BR + capability; forward trace to TRD/test in §28. | OK |

*Improvements applied: rules grouped by domain for readability; each requirement given explicit BR + capability trace; open parameters flagged at requirement level.*

---

**— END OF PART 3 — (APPROVED 2026-06-27)**
*Part 3 covers: Business Capability Model · Business Rules (45) · Functional Requirements (28) · Non-Functional Requirements (13).*

---

# 14. User Roles and Permissions

Access is restricted to MOE accounts (BR-003) and governed by role-based access control (BR-031/032).
All roles operate under the human-in-the-loop principle (BR-015): no role — and no agent — may bypass an
approval gate for a formal action.

### 14.1 Role definitions
| Role | Description | Tier |
|------|-------------|------|
| **Super Admin** | Platform governance: users/roles, amendment windows, knowledge links, provider config, audit oversight. | Platform |
| **JPN Administrator** | State-level KPI oversight; consolidation; initiate state reports; send approved notifications. | State |
| **Sector Administrator** | Manage KPIs for their sector/Bahagian; assign PICs; act on at-risk alerts. | State/National |
| **PPD Administrator** | District-level KPI management; oversee district PICs; monitor district submission. | District |
| **KPI PIC** | Own assigned KPI(s): complete data, monthly updates, finance, evidence, remarks. | Operational |
| **Executive Management** | Consume dashboard/AI summary; approve reports and formal actions. | Executive |
| **Read-only User** | View dashboards/reports and use the chatbot; no edit rights. *(e.g. observers, auditors-view)* | Varies |
| *(Internal Audit)* | Read audit trail & assurance views (a specialised read-only profile). | Assurance |

### 14.2 Permission matrix
*Legend: ✓ = allowed · A = approves (human-in-the-loop gate) · own = own records only · – = not allowed.*

| Action / Capability | Super Admin | JPN Admin | Sector Admin | PPD Admin | KPI PIC | Exec Mgmt | Read-only |
|---------------------|:-----------:|:--------:|:------------:|:---------:|:-------:|:---------:|:---------:|
| View Teras dashboard & reports | ✓ | ✓ | ✓ | ✓ | ✓(scope) | ✓ | ✓ |
| Import Excel (one-time) | ✓ | ✓ | – | – | – | – | – |
| Manage KPI records | ✓ | ✓ | ✓(sector) | ✓(district) | – | – | – |
| Assign PIC | ✓ | ✓ | ✓ | ✓ | – | – | – |
| Monthly KPI update | – | – | – | – | ✓(own) | – | – |
| Amend KPI def. (Jul/Oct only) | ✓ | A | C | C | request | I | – |
| Enter/manage finance status | ✓ | ✓ | ✓ | ✓ | ✓(own) | – | – |
| Review/approve monthly report | – | ✓(prepare) | C | C | – | **A** | – |
| Approve/send notifications | – | **A** | C | C | – | C | – |
| Manage knowledge links | ✓ | C | – | – | – | – | – |
| Provider/config change | ✓ | – | – | – | – | – | – |
| Manage users/roles/windows | ✓ | C | – | – | – | – | – |
| View audit trail | ✓ | ✓(scope) | ✓(scope) | ✓(scope) | – | ✓ | ✓(audit) |
| Use KPI chatbot | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Use Executive Copilot | ✓ | ✓ | C | C | – | ✓ | – |

> Scope qualifiers: JPN Admin = state-wide; Sector/PPD Admin = their sector/district; PIC = own KPIs.
> **Login (resolved, C-001):** only authenticated users with `@moe.gov.my` **or** `@moe-dl.edu.my` may access the system (BR-003).

---

# 15. Dashboard Requirements

The main dashboard is the primary management view and **must summarise and map all KPIs by Teras 1–7**
(BR-020; B2A #1). It draws on the operational database and the latest AI outputs. Charts may be phased —
**cards/tables first, charts later** (BR-045).

### 15.1 Mandatory dashboard components (per Teras 1–7)
| # | Component | Description | BR/Req |
|---|-----------|-------------|--------|
| DSH-01 | KPI summary by Teras | Total KPIs and counts per Teras 1–7. | BR-020/021 |
| DSH-02 | KPI mapping by Teras | Distribution/mapping of KPIs across Teras (chart + table). | BR-021 |
| DSH-03 | Achievement summary | Achievement vs target per Teras. | BR-021 |
| DSH-04 | Risk summary | At-Risk/Critical counts per Teras (heatmap/table). | BR-021 |
| DSH-05 | Budget summary | Allocation status (six-value) per Teras. | BR-010/021 |
| DSH-06 | Monthly submission summary | Submitted/outstanding per Teras/period. | BR-007/021 |
| DSH-07 | Missing information summary | Incomplete-field counts per Teras. | BR-005/006 |
| DSH-08 | Executive AI summary | AI answers to the 7 management questions. | BR-022 |
| DSH-09 | Charts & visual analytics | Bar (KPIs by Teras), stacked (status), risk heatmap, budget, submission, alignment. | BR-021/045 |
| DSH-10 | Quick access to high-risk KPIs | One-click list/drill-down of At-Risk/Critical KPIs. | BR-020 |
| DSH-11 | KPI mapping table | KPI → Teras → PIC → Sector → Status → Risk → Budget Status. | BR-021 |
| DSH-12 | RPM alignment strength | Alignment indicator per Teras. *(metric pending Q-021)* | BR-012/020 |

### 15.2 Behaviour
- **Drill-down:** Teras → KPI list → KPI detail.
- **Role-scoped:** content reflects the viewer's scope (state/district/sector/own).
- **Refresh:** reflects the latest saved updates and AI outputs.
- **Executive insight:** a management summary section combining AI summary + high-risk + budget signals.

---

# 16. AI Features

The platform provides the following confirmed AI capabilities. All are **advisory** (BR-028); any
world-affecting output passes a human-in-the-loop gate (BR-015).

| # | AI Feature | Description | Agent(s) | Human review |
|---|------------|-------------|----------|:------------:|
| AIF-01 | KPI Analysis | Interpret status/trends per Teras. | KPI Analysis | No (display) |
| AIF-02 | KPI Alignment with RPM 2026–2035 | Map KPI↔RPM; score alignment strength. | Knowledge Alignment | No (display) |
| AIF-03 | Budget Intelligence | Budget status analysis, funding-gap detection, budget-risk analysis. | Budget Intelligence (+Financial Monitoring) | **Yes** (before use) |
| AIF-04 | Low Cost High Impact Analysis | Analyse activities, evaluate impact, recommend lower-cost alternatives / resource optimisation / collaboration. | Budget Intelligence | **Yes** |
| AIF-05 | Executive Copilot | Synthesised leadership decision support. | Executive Copilot | Yes (before acting) |
| AIF-06 | KPI Chatbot | Grounded, source-cited Q&A; fixed fallback. | KPI Chatbot | No (info only) |
| AIF-07 | Monthly Report Generation | Draft monthly report + executive summary. | Report Generation | **Yes** |
| AIF-08 | Notification Intelligence | Draft reminders/alerts; suggest escalation. | Notification & Reminder | **Yes** (before send) |
| AIF-09 | Missing Data Detection | Detect incomplete mandatory fields; warn. | Validation/Completeness | No |
| AIF-10 | Risk Detection | Flag At-Risk/Critical KPIs. *(method Q-020)* | Risk | No (display); Yes if triggers action |

> **Financial Decision Support (FDS) grouping (BR-046):** AIF-03 (Budget Intelligence), AIF-04 (Low Cost
> High Impact Analysis), the financial part of AIF-05 (Executive Copilot → Executive Financial Insight) and
> intervention (FRQ-015) together form the **Financial Decision Support capability** — broader than Budget
> Intelligence alone. It is specified in full in **Part 5 §20 Financial Decision Support** and reflected in
> the Dashboard (§15) and Executive Copilot (§19.4). Low Cost High Impact is therefore a **first-class
> analysis**, not merely a Budget Intelligence sub-feature.

---

# 17. AI Agents

The platform implements a **multi-agent architecture** (BR-041). The proposed authoritative roster is
**14 agents** (resolves Q-024 as a proposal; option to merge Financial Monitoring into Budget Intelligence
→ 13). Agents are advisory; **Audit Agent logs all consequential outputs and decisions** (BR-029).

| # | Agent | Purpose | Inputs | Outputs | Dependencies | Human review |
|---|-------|---------|--------|---------|--------------|:------------:|
| 1 | **Data Integration** | Import Excel → structured records | Pelan Taktikal files | KPI master records | — | No (admin verifies) |
| 2 | **Validation/Completeness** | Detect missing/inconsistent data | Imported & updated data | Warnings, completeness flags | Agent 1 | No |
| 3 | **KPI Analysis** | Classify status vs target | KPI data + updates | Status per KPI/Teras | Agents 1,2 | No |
| 4 | **Risk (Early Warning)** | Flag At-Risk/Critical | Progress, thresholds | Risk ratings | Agent 3 | No (Yes if acts) |
| 5 | **Financial Monitoring** | Track allocation/warrant/expenditure | Finance entries | Budget status | Agent 1 | No |
| 6 | **Budget Intelligence** | Budget status analysis, funding-gap detection, budget-risk analysis, Low Cost High Impact + OBB analysis (core of Financial Decision Support, BR-046) | Cost/impact, budget status, activities | Financial recommendations + rationale | Agents 4,5 | **Yes** |
| 7 | **Intervention** | Propose interventions (draft) | Risk + context | Intervention drafts | Agents 4,6 | **Yes** |
| 8 | **Notification & Reminder** | Draft reminders/alerts | Gaps, deadlines, risk | Queued draft emails | Agents 2,4 | **Yes (send)** |
| 9 | **Audit** | Log changes/decisions | All events | Audit-trail entries | all | n/a (system) |
| 10 | **Report Generation** | Draft monthly reports | DB + AI outputs | Report drafts | Agents 3,4,5,6 | **Yes** |
| 11 | **KPI Chatbot** | Grounded Q&A | DB + RAG + links | Cited answers / fallback | RAG (§19) | No |
| 12 | **Knowledge Alignment** | KPI↔RPM alignment | KPIs + RPM corpus | Alignment + strength | RAG (§19) | No |
| 13 | **Executive Copilot** | Leadership decision support | Operational + knowledge | Executive insights | Agents 3,4,6 + RAG | Yes (before acting) |
| 14 | **AI Summary** | Main-page 7-question summary | All signals | Dashboard AI summary | Agents 3,4,5,6 | No |

> **Agent architecture (resolved, C-002):** the architecture is **capability-driven**. The agents above
> are the current primary agents; together with the reusable **Skills Layer** they implement the
> capabilities. The **number of agents may evolve without changing the business architecture** — no fixed
> count is mandated. Capabilities (BCM) and rules (BR-016/041/042) are the stable contract.

---

# 18. Skills Layer

Skills are **reusable, independently testable capabilities** invoked by multiple agents (BR-016/042;
B2A #7). Separating skills from agents promotes reuse, testability and governance.

| Skill | Purpose | Used by agents |
|-------|---------|----------------|
| Excel parsing/normalisation | Read & structure Pelan Taktikal | 1 |
| Completeness validation | Check mandatory fields | 2, 3 |
| KPI status classification | Status vs target | 3, 14 |
| Risk scoring | Score/flag risk | 4, 14, 7 |
| Budget-status classification (six-value) | Classify allocation status | 5, 6 |
| Low Cost High Impact scoring | Cost-vs-impact prioritisation | 6, 7 |
| OBB value-for-money calculation | Outcome-based value | 6 |
| Teras aggregation/roll-up | Aggregate by Teras 1–7 | 3, 14, 10 |
| RAG retrieval + source citation | Retrieve & cite knowledge | 11, 12, 13 |
| Link fetch/refresh/freshness | Ingest & refresh live links | (knowledge ingestion) |
| Alignment scoring (KPI↔RPM) | Score alignment strength | 12 |
| Email/notification drafting | Draft comms | 8, 10 |
| Report templating/generation | Assemble reports | 10 |
| Audit logging | Write audit entries | 9 (all action agents) |
| HITL gating/approval routing | Route to human approval | all action-taking agents |

---

# 19. Knowledge Management (RAG)

The platform maintains **two strictly separate data planes** (BR-017; AD-004; B2A #5).

### 19.1 Operational Data → Database
- **Initial Excel import** (Pelan Taktikal JPN/PPD) — imported once (BR-001/018).
- **Monthly KPI database** — KPI records, monthly updates, PIC info, finance status, evidence, remarks, audit trail.
- *Transactional, structured, audit-grade; the system of record. Never used as RAG knowledge.*

### 19.2 Knowledge Data → RAG / Knowledge Base
- **RPM 2026–2035** (primary reference, BR-012).
- **Supporting documents** and **Guidelines / circulars / notes** (static sources, BR-023).
- **Live knowledge links** (updated sources; stored with title/URL/category/last-checked; admin-refreshable; prefer trusted — BR-023/024).
- *Chunked → embedded → vector store; retrieved with source citation (BR-025); inaccessible source → clear message, never guess (BR-026); fixed fallback when absent (BR-027). Never treated as operational KPI input (BR-019).*

### 19.3 How the Chatbot uses the knowledge base
The **KPI Chatbot** (Agent 11) answers using, in order: KPI database, monthly updates, uploaded knowledge
documents, RPM 2026–2035, and live/updated links where available (AIR-070). It **cites the source(s)**
used and returns the fixed fallback string if information is not found.

### 19.4 How the Executive Copilot uses the knowledge base
The **Executive Copilot** (Agent 13) combines **operational signals** (status, risk, budget, submission
from Agents 3/4/5/6) with **knowledge retrieval** (RPM + guidelines + links via RAG) to produce
synthesised, source-grounded decision support for management — advisory, human-reviewed before any action.

### 19.5 Knowledge governance
**Resolved (Q-022):** live knowledge links are **supported RAG knowledge sources subject to administrator
validation** — an administrator approves/validates each link (preferring official/trusted sources, BR-024)
before it is used by the chatbot/copilot; inaccessible sources yield a clear message, never a guess
(BR-026). Detailed allow-list mechanics are specified in the TRD.

---

## Self-Review — Part 4

| Check | Finding | Action |
|-------|---------|--------|
| Missing roles? | Added Read-only + Internal Audit (read) alongside the 6 requested roles; permission matrix complete. | OK |
| Dashboard items? | All 12 requested components mapped (DSH-01…12) incl. quick-access high-risk + mapping table + alignment. | OK |
| AI features? | All 10 requested capabilities (AIF-01…10) present and agent-mapped. | OK |
| Agents complete? | 14 agents each with purpose/inputs/outputs/dependencies/human-review; C-002 flagged. | OK |
| Skills mapped? | 15 reusable skills mapped to agents. | OK |
| Operational vs Knowledge separation? | Explicitly distinguished (§19.1 vs §19.2); chatbot & copilot usage described. | OK |
| Consistency with approved rules? | All cross-referenced to BR-001…045 and B2A decisions; HITL honoured in matrix & agents. | OK |
| Open parameters | Login domain (C-001), agent count (C-002/Q-024), risk (Q-020), alignment (Q-021), link policy (Q-022) flagged. | Flagged |

*Improvements applied: full permission matrix with scope qualifiers; dashboard components given IDs; AI features linked to agents + human-review; skills mapped to agents; knowledge planes explicitly separated.*

---

**— END OF PART 4 — (APPROVED 2026-06-27)**
*Part 4 covers: User Roles & Permissions · Dashboard Requirements · AI Features · AI Agents (14) · Skills Layer · Knowledge Management (RAG).*

---

# 20. Financial Decision Support (FDS)

**Financial Decision Support is the parent financial capability** (BR-046; CAP-B4). It is deliberately
**broader than budget analysis** — it turns financial and performance data into actionable, value-for-money
recommendations and resource-optimisation strategies. All FDS outputs are **advisory** and pass a
**human-in-the-loop gate before implementation** (BR-015/028/037). FDS comprises four sub-capabilities,
plus an explicit resource-optimisation dimension.

### 20.1 Budget Intelligence *(CAP-B2 / FRQ-014 / Agent 6)*
- **Budget status analysis** — consolidate allocation status (six-value vocabulary, BR-010), warrant and expenditure per KPI/activity/Teras.
- **Funding-gap detection** — identify KPIs/activities where allocation is *pending / not received / insufficient* against planned need.
- **Budget-risk analysis** — flag financial risk (e.g. under-funding of high-priority or at-risk KPIs; over-concentration; spend not aligned to impact).

### 20.2 Low Cost High Impact Analysis *(CAP-B5 / FRQ-029 / Agent 6)*
Applies the **Low Cost High Impact Matrix** as a first-class analysis (not a sub-feature of budget
reporting):
- **Analyse activities** — position each activity/initiative on the cost vs. expected-impact matrix.
- **Evaluate expected impact** — assess contribution to KPI achievement and RPM alignment.
- **Recommend lower-cost alternatives** — propose cheaper ways to achieve the same outcome.
- **Recommend resource optimisation** — see §20.5.
- **Recommend collaboration opportunities** — identify where shared effort raises impact or lowers cost.

### 20.3 Intervention Recommendation *(CAP-AI3 / FRQ-015 / Agent 7)*
For at-risk/critical KPIs and funding gaps:
- **Suggest alternative programmes** — alternative activities/initiatives to achieve the target.
- **Suggest implementation strategies** — practical approaches to deliver within constraints.
- **Prioritise recommendations** — rank by impact, cost, urgency and feasibility.

### 20.4 Executive Financial Insight *(CAP-B6 / FRQ-030 / Agents 13/14)*
- **Present AI-generated financial recommendations** to management in clear, summarised form.
- **Explain the rationale** — why each recommendation is made, with supporting evidence/citation.
- **Support management decision-making** — feed the **Dashboard executive summary (§15, DSH-08)** and the **Executive Copilot (§19.4)**; remain advisory pending human approval.

### 20.5 Resource-Optimisation Strategies *(within FDS — per change CL-024)*
FDS must propose **low-cost high-impact approaches beyond budget analysis**, including:
| Strategy | Description |
|----------|-------------|
| Collaboration opportunities | Joint delivery across PPDs/sectors/divisions to share cost and raise impact. |
| Programme consolidation | Merge overlapping/duplicative activities to reduce cost and effort. |
| Shared resources | Pool venues, trainers, materials, expertise across units. |
| Digital alternatives | Replace high-cost physical activities with digital/online delivery where effective. |
| Other low-cost high-impact approaches | Phasing, targeting high-leverage cohorts, reusing existing assets, etc. |

### 20.6 Outcome-Based Budgeting (OBB) within FDS
**Resolved (Q-025):** OBB is recognised as **part of the Financial Decision Support capability and the
budget-governance process** (BR-038/046). FDS analyses budget against outcomes (value-for-money) as part
of Budget Intelligence (§20.1) and Low Cost High Impact Analysis (§20.2). The precise OBB calculation
method is a Technical Assumption to be specified in the TRD.

### 20.7 FDS as a top-level capability — carry-forward & governance
**Financial Decision Support (FDS) is hereby established as a top-level business capability** of the
platform (CAP-B4), not a sub-feature of budget reporting. It **must be carried forward and reflected
consistently** in:
- **TRD** — FDS components specified as technical requirements (incl. OBB method, Low Cost High Impact scoring).
- **AI Architecture** — FDS realised by the Budget Intelligence + Intervention + Executive Copilot agents and supporting skills.
- **Dashboard** — FDS outputs surfaced (budget summary, Low Cost High Impact recommendations, Executive Financial Insight).
- **Executive Copilot** — FDS recommendations + rationale delivered to leadership.
- **Requirements Traceability Matrix** — FDS requirements (FRQ-014/015/028/029/030) traced end-to-end.

FDS is **advisory only**; recommendations are logged (Audit Agent, BR-029) and require human approval
before any formal action (BR-015; ASM-11). Traces: BR-010/011/037/038/046; CAP-B2/B4/B5/B6, CAP-AI3/AI6;
FRQ-014/015/028/029/030.

---

# 21. Reporting Requirements

| ID | Requirement | Description | BR/Req |
|----|-------------|-------------|--------|
| REP-01 | Monthly report generation | Generate the monthly KPI report (draft → human review → approval). | BR-014/040, FRQ-016, REPQ-001 |
| REP-02 | Executive summary | Management executive summary incl. Executive Financial Insight (§20.4). | BR-039, REPQ-002 |
| REP-03 | Teras dashboard views | Per-Teras dashboards, mapping table and charts (phased). | BR-020/021/045, REPQ-003 |
| REP-04 | AI summary report | AI-generated 7-question summary on the main page. | BR-022, REPQ-004 |
| REP-05 | Risk/budget/submission summaries | Aggregated summaries by Teras. | BR-021, REPQ-006 |
| REP-06 | Report archive & notification log | Store issued reports and a log of notifications sent. | pptx TR012, REPQ-005, BR-029 |

**Reporting workflow (BR-040):** draft → human review → approval → email queue → distribution → audit log.
No report is issued without human approval (BR-015).

---

# 22. Notification Requirements

| ID | Requirement | Description | BR/Req |
|----|-------------|-------------|--------|
| NOT-01 | Reminders | Remind PICs of incomplete data and due monthly updates. | BR-007, FRQ-018 |
| NOT-02 | Alerts | Alert sector/admin on At-Risk/Critical KPIs and funding gaps. | BR-007, FRQ-018 |
| NOT-03 | Escalation tracking | Track and escalate unresolved gaps/late submissions. | BR-007, HMW-15 |
| NOT-04 | Approved distribution | Send only after human approval; queue and log. | BR-015/040, FRQ-019 |
| NOT-05 | Notification intelligence | AI drafts notification content (advisory; human-approved before send). | BR-028, AIF-08 |

---

# 23. Security Requirements

| ID | Requirement | Description | BR/Req |
|----|-------------|-------------|--------|
| SEC-01 | MOE-domain authentication | Only authenticated users with `@moe.gov.my` **or** `@moe-dl.edu.my` may access the system (resolved C-001). | BR-003, NFRQ-001 |
| SEC-02 | Role-based access control | Enforce role permissions (§14 matrix). | BR-031/032 |
| SEC-03 | Data protection | Protect sensitive KPI/budget data; least-privilege access. | NFRQ-001 |
| SEC-04 | Audit & traceability | Tamper-evident audit trail of changes and decisions. | BR-009/029/036, NFRQ-002 |
| SEC-05 | Operational/knowledge separation | Enforce two data planes; no cross-contamination. | BR-017, NFRQ-010 |
| SEC-06 | Knowledge-source trust | Live links are supported RAG sources **subject to administrator validation** (resolved Q-022); prefer official/trusted; allow-list mechanics in TRD. | BR-024 |
| SEC-07 | Compliance & data residency | Meet government security/residency rules. *(pending Q-014/Q-017)* | NFRQ-011 |
| SEC-08 | Provider configuration security | Secure handling of provider keys/config (`config.md`). | BR-044, NFRQ-003 |

---

# 24. Constraints

| ID | Constraint | Source |
|----|-----------|--------|
| CON-01 | Excel used for initial import only; database is the working source. | BR-001/018 |
| CON-02 | Monthly updates keyed in-system by the PIC. | BR-002 |
| CON-03 | Login restricted to MOE accounts (`@moe.gov.my` or `@moe-dl.edu.my`) — resolved C-001. | BR-003 |
| CON-04 | KPI statement/indicator/target editable only July/October. | BR-008 |
| CON-05 | All amendments audited. | BR-009 |
| CON-06 | Human approval required before formal action/report/email. | BR-015 |
| CON-07 | AI advisory only — proposes, never finally acts; cited; honest fallback. | BR-025/027/028 |
| CON-08 | Operational data → database; knowledge data/links → RAG (separate planes). | BR-017 |
| CON-09 | Main dashboard must summarise & map KPIs by the 7 Teras. | BR-020 |
| CON-10 | Provider config: Groq (dev); OpenAI/Anthropic (prod) via `config.md`. | BR-044 |

---

# 25. Assumptions

| ID | Assumption | To confirm |
|----|-----------|-----------|
| ASM-01 | RPM 2026–2035 ≡ PPPM 2026–2035 (terminology). | Business Assumption (Q-001/C-003) |
| ASM-02 | Perak is the initial working set; **national rollout = Future Enhancement** (resolved Q-003). | Approved (CL-026) |
| ASM-03 | Schools are a reporting/evidence tier in Release 1 (not a login tier). | Business Assumption (Q-002) |
| ASM-04 | `project_structure.pptx` is a draft input, subordinate to this gated process. | Business Assumption (Q-027) |
| ASM-05 | **English** is the primary UI/report language; future localisation allowed (resolved Q-012). | Approved (CL-026) |
| ASM-06 | **Capability-driven agent architecture**; agent count may evolve without changing business architecture (resolved C-002). | Approved (CL-026) |
| ASM-07 | Risk and alignment-strength are initially **rule-based**, AI-assisted later (finalised in TRD). | Technical Assumption (Q-020/Q-021) |
| ASM-08 | OBB is part of FDS & budget governance; method specified in TRD (resolved Q-025). | Approved (CL-026) |
| ASM-09 | Live links are RAG sources subject to **administrator validation** (resolved Q-022). | Approved (CL-026) |
| ASM-10 | Allocation/budget figures are entered/managed in-platform; no external finance write-back in scope. | Business Assumption (Q-009) |
| ASM-11 | **AI recommendations are advisory only and do not replace authorised management decisions. Final approval remains with authorised officers.** | Approved (BR-015/028) |

---

# 26. Risks

| ID | Risk | Impact | Mitigation |
|----|------|--------|-----------|
| RSK-01 | PIC adoption / data-entry fatigue | High | Low-friction UX (NFRQ-005); reminders; phased rollout. |
| RSK-02 | Import data quality / alert fatigue | Med-High | Tunable completeness rules; prioritised warnings. |
| RSK-03 | AI credibility / political exposure | High | Advisory-only + HITL + citation + fallback (BR-015/025/027/028). |
| RSK-04 | Incomplete audit/accountability | High | Comprehensive audit trail (BR-009/029); oversight views. |
| RSK-05 | Scope creep (14 agents, OBB, live links) | Med | MoSCoW phasing (§6.4); V1 lean core. |
| RSK-06 | Live-link security / data-egress | Med | Trust allow-list policy (Q-022); prefer official sources (BR-024). |
| RSK-07 | Source-of-truth confusion (versions/Teras 5–7) | Med | Single DB record; import governance; resolve GAP-002. |
| RSK-08 | Vendor lock-in over 10 years | Med | Provider abstraction (BR-044). |
| RSK-09 | Unconfirmed parameters harden into assumptions | Med | Open-items register; flagged inline; resolve before freeze. |

---

# 27. Success Criteria

The project is successful when (traceable to HMW §6 success criteria):
1. **Single source of truth** — all JPN/PPD KPI data centralised; Excel only for initial import. *(OBJ-01)*
2. **Completeness** — every KPI has PIC/sector/email; missing-info warnings near zero. *(OBJ-03)*
3. **Timeliness** — on-time in-system monthly submission; real-time status. *(OBJ-02)*
4. **Early risk visibility** — at-risk/critical KPIs flagged before targets are missed. *(OBJ-06)*
5. **Financial control** — allocation status visible; FDS recommendations used in decisions. *(OBJ-05)*
6. **Reporting effort reduced** — monthly reports generated with minimal manual effort (human-approved). *(OBJ-09)*
7. **Executive clarity** — Teras dashboard + AI summary in active management use. *(OBJ-07)*
8. **Alignment assured** — each KPI's RPM alignment visible/traceable. *(OBJ-08)*
9. **Governed change & audit** — amendments only Jul/Oct, fully logged. *(OBJ-04)*
10. **Trusted AI** — advisory, cited, human-gated, honest about gaps; adopted by users. *(OBJ-10/11)*
11. **Continuity** — knowledge/ownership survive staff change over the 10-year horizon. *(OBJ-12)*

---

# 28. Traceability Summary

This BRD maintains end-to-end traceability. Each requirement links **backward** to a problem (HMW) and a
business rule, and **forward** to capability, module and (subsequently) TRD/architecture/test.

**Chain:** `HMW (PP/HMW IDs) → BRD (OBJ / BRQ / FRQ / NFRQ / AIF / DSH / FDS / REP / NOT / SEC) → Capability (CAP) → Business Rule (BR) → Module (M1–M13) → [TRD → Architecture → Test Case]`

| Example thread | Trace |
|----------------|-------|
| Centralisation | PP01 → HMW-01 → OBJ-01/BRQ-001 → FRQ-003 → CAP-K1 → BR-001/018 → M2 |
| Teras dashboard | PP08 → HMW-13 → OBJ-07/BRQ-007 → FRQ-011/012/DSH-01…12 → CAP-R2/AI7 → BR-020/021/022 → M5 |
| Financial Decision Support | PP05/06 → HMW-08/09/10 → BRQ-005 → §20/FRQ-014/015/029/030 → CAP-B4/B5/B6/AI3 → BR-010/011/046 → M6/M7 |
| Knowledge/RAG | PP12 → HMW-18/19 → BRQ-008 → FRQ-020/021/022 → CAP-KM1–3 → BR-012/019/023–027 → M8 |
| Governance/HITL | PP13 → HMW-04/20 → OBJ-04 → FRQ-010/017/024 → CAP-G1/G2/G3 → BR-008/009/015 → M12 |

The complete row-level matrix is maintained in `TRACEABILITY_REGISTER.md` and will be expanded with TRD,
component, API and test-case IDs in later phases.

---

# 29. Glossary

Key terms (full glossary in `PROJECT_GLOSSARY.md`):
- **RPM 2026–2035** — Rancangan Pendidikan Malaysia, the 10-year national roadmap (≡ PPPM, pending Q-001).
- **Teras Strategik** — strategic pillar (7 total). · **Prakarsa** — initiative. · **TOV** — baseline (Take-Off Value).
- **JPN / PPD** — State / District Education Office. · **PIC** — Person In Charge of a KPI.
- **Financial Decision Support (FDS)** — parent financial capability (Budget Intelligence, Low Cost High Impact Analysis, Intervention Recommendation, Executive Financial Insight + resource optimisation).
- **Low Cost High Impact Matrix** — cost-vs-impact prioritisation analysis.
- **RAG** — Retrieval-Augmented Generation. · **HITL** — Human-in-the-loop.
- **Executive Copilot** — leadership decision-support assistant. · **Agent / Skill** — autonomous AI component / reusable capability.
- **Operational Data / Knowledge Data** — DB-stored transactional data / RAG-stored reference data.

---

# 30. Appendices

- **Appendix A — KPI code scheme:** `TSx.Sy.Pz.KPIn` (Teras.Strategi/Enabler.Prakarsa.KPI).
- **Appendix B — Budget object codes:** OS21000…OS42000 with monthly projections (Jan–Dec).
- **Appendix C — Finance allocation vocabulary:** received / will be received / pending / not received / not required / insufficient.
- **Appendix D — Source data:** Pelan Taktikal JPN (Teras 1&2, 3&4; Reference; SENARAI KPI), 12 PPD workbooks (Perak). *(Teras 5–7 location open — GAP-002.)*
- **Appendix E — AI agent roster (14):** see §17.
- **Appendix F — Open questions register:** Q-001…Q-027, contradictions C-001…C-003, gaps GAP-001/002 (see `QUESTIONS_AND_GAPS.md`).
- **Appendix G — Reference documents:** HMW (D1), As-Is (B4), To-Be (B5), BCM (B6), Business Rules Catalogue (B7), Master Requirements Catalogue (B8).
- **Appendix H — Audit Resolutions (B11-Full / CL-026):**
  | Item | Classification | Resolution adopted |
  |------|----------------|--------------------|
  | Login domain (C-001) | Resolved — Approved decision | Both `@moe.gov.my` and `@moe-dl.edu.my` (BR-003); pptx TR002 superseded. |
  | Agent architecture (C-002/Q-024) | Resolved — Approved decision | Capability-driven; primary agents + Skills Layer; count may evolve without changing business architecture. |
  | OBB (Q-025) | Approved Business Assumption | Part of FDS & budget governance; method in TRD. |
  | Live knowledge links (Q-022) | Resolved — Approved decision | Supported RAG sources subject to administrator validation. |
  | Scope (Q-002/Q-003) | Resolved + Future Enhancement | Adopt approved scope (PROJECT_CONTEXT/§6); national rollout = Future Enhancement. |
  | Language (Q-012) | Resolved — Approved decision | English primary UI/reports; future localisation allowed. |
  | Risk scoring (Q-020) | Technical Assumption | Rule-based initially; finalised in TRD. |
  | Alignment-strength (Q-021) | Technical Assumption | Metric defined in TRD. |
  | Data classification / hosting / residency (Q-017/Q-014) | Requires User Confirmation | Government policy input needed before production. |
  | Expected scale (Q-016) | Technical Assumption | Sized to Perak pilot; revisit if national. |
  | Teras 5–7 source files (GAP-002) | Requires User Confirmation | Locate/confirm remaining Teras data. |
  | Knowledge corpus & link list (Q-019) | Requires User Confirmation | Provide documents/links for RAG. |

---

## Self-Review — Part 5

| Check | Finding | Action |
|-------|---------|--------|
| FDS structured correctly? | §20 parent with 4 sub-capabilities + resource-optimisation strategies (collaboration, consolidation, shared resources, digital alternatives, other). | OK |
| Missing requirements? | Reporting, notifications, security each given IDs (REP/NOT/SEC); all B8 categories now placed. | OK |
| Duplicate content? | Glossary/traceability summarised with reference to KB sources, not reproduced fully. | Avoided |
| Inconsistencies? | Constraints/assumptions/risks consistent with Parts 1–4 and B2A decisions. | None |
| Missing business rules? | All governing BRs cited incl. BR-046 (FDS). | OK |
| Open parameters | C-001, C-002/Q-024, Q-020/021/022, Q-012/014/017, GAP-002 captured in assumptions/risks/appendix. | Flagged |

*Improvements applied: FDS made the financial parent; resource-optimisation strategies tabulated; reporting/notification/security given requirement IDs; full traceability threads provided.*

---

**— END OF PART 5 —**
*Part 5 covers: Financial Decision Support (FDS) · Reporting · Notifications · Security · Constraints · Assumptions · Risks · Success Criteria · Traceability Summary · Glossary · Appendices.*

---

## FREEZE RECORD — Business Requirements Baseline
- **Baseline:** D2 — Business Requirements Document, **v1.0 FROZEN** on 2026-06-27 (Freeze Gate 1).
- **Approved by:** User (suzila@iegcampus.com).
- **Scope of baseline:** §1–§30 + Appendices A–H; OBJ-01…12; BRQ/FRQ (incl. FDS FRQ-014/015/028/029/030)/
  NFRQ/AIF/DSH/REP/NOT/SEC; 45 Business Rules (incl. BR-046 FDS); 11 Approved Assumptions (ASM-01…11);
  Audit Resolutions (Appendix H, CL-026).
- **Final refinements applied (this turn):** ASM-11 (AI advisory only; final approval with authorised
  officers); FDS established as a **top-level capability** to carry into TRD/AI Architecture/Dashboard/
  Executive Copilot/Traceability Matrix; FDS referenced consistently across Business Rules, Functional
  Requirements and AI Features.
- **Precedence:** subordinate to the B2A Authoritative Decisions; consistent with the frozen HMW (D1).
- **Carry-forward to TRD:** technical specs for risk scoring (Q-020), alignment-strength (Q-021), OBB
  method (Q-025), live-link validation (Q-022), FDS components; plus Requires-User-Confirmation items
  (compliance/hosting Q-014/Q-017, Teras 5–7 data GAP-002, knowledge corpus Q-019).
- **Reopen policy:** changes only via explicit, logged change request (CHANGE_LOG.md).

---
*End of Business Requirements Document v1.0 — FROZEN APPROVED BASELINE. Foundation for the TRD (D3).*
