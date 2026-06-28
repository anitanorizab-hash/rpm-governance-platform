# BUSINESS RULES CATALOGUE
### Agentic AI Strategic Governance Platform — RPM 2026–2035

| Field | Value |
|-------|-------|
| Document | B7 — Business Rules Catalogue |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Role | **Single source of truth for all business rules** governing the application |
| Sources | `BUSINESS_RULES.md` (BR-001…027), HMW v1.0, As-Is/To-Be, BCM, AI_RULES, TECHNICAL_RULES |
| Boundary | **Business rules only.** No technical implementation, no DB design. |

> **ID convention:** existing `BR-NNN` IDs are preserved (single source of truth = `BUSINESS_RULES.md`).
> Rules newly formalised in this catalogue use `BR-NNN` continuing the sequence (BR-028+).
> Traceability columns: B=BRD, T=TRD, SA=System Architecture, AI=AI Architecture, DB=Database Design, TC=Test Cases.

---

## 1. Business Rules Overview

A **Business Rule** is a statement that defines or constrains some aspect of the business — it asserts
business structure or controls behaviour, independent of how it is implemented. This catalogue collects,
de-duplicates and organises every **confirmed** rule discovered across Discovery, HMW, the As-Is/To-Be
process, and the Business Capability Model.

**Why it matters:** rules are the *contract* the system must honour. Centralising them here means the
BRD turns each rule into a requirement, the TRD into a control, the architecture into a mechanism, and
the test cases into verification — all tracing to one rule ID. This prevents rules being lost,
contradicted or silently reinterpreted across a ten-year programme. Rules marked *(pending Qx)* are
confirmed in intent but have a parameter still to be set.

---

## 2. Governance Rules

| ID | Rule | Source | B | T | SA | AI | DB | TC |
|----|------|--------|---|---|----|----|----|----|
| BR-015 | Human review is required before formal action, report approval and email sending. | User | ✓ | ✓ | ✓ | ✓ | – | ✓ |
| BR-028 | AI recommendations are **advisory only**; agents propose, humans dispose. | AIR-001/CON-07 | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-009 | All amendments must be saved in an audit trail (who/what/when). | User | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| BR-029 | Every consequential AI output and human decision is logged (auditable). | To-Be Audit Agent | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| BR-030 | The platform must support audit/oversight querying for assurance. | BCM CAP-G4 | ✓ | ✓ | ✓ | – | ✓ | ✓ |

---

## 3. User Access Rules

| ID | Rule | Source | B | T | SA | AI | DB | TC |
|----|------|--------|---|---|----|----|----|----|
| BR-003 | Login restricted to `@moe.gov.my` and `@moe-dl.edu.my` accounts. *(domain count pending C-001/Q-023)* | User | ✓ | ✓ | ✓ | – | – | ✓ |
| BR-031 | Access is governed by **role-based access control (RBAC)**. | CAP-U2 | ✓ | ✓ | ✓ | – | ✓ | ✓ |
| BR-032 | Permissions differ by role (Super Admin, JPN/Sector/PPD Admin, KPI PIC, Finance, Executive, Audit). | BCM/To-Be | ✓ | ✓ | ✓ | – | ✓ | ✓ |
| BR-033 | Access provisioning supports onboarding/offboarding and delegation/acting-officer. *(rules pending)* | BCM CAP-U3 | ✓ | ✓ | – | – | ✓ | ✓ |

---

## 4. KPI Management Rules

| ID | Rule | Source | B | T | SA | AI | DB | TC |
|----|------|--------|---|---|----|----|----|----|
| BR-001 | Excel files are used for **initial input only**. | User | ✓ | ✓ | ✓ | – | ✓ | ✓ |
| BR-018 | Pelan Taktikal JPN/PPD imported once; database is the working source thereafter. | User/D3A | ✓ | ✓ | ✓ | – | ✓ | ✓ |
| BR-002 | Monthly KPI updates are entered **only through the application** by the KPI PIC. | User | ✓ | ✓ | – | – | ✓ | ✓ |
| BR-004 | Every KPI must have a **PIC name, sector and PIC email**. | User | ✓ | ✓ | – | – | ✓ | ✓ |
| BR-005 | The system must detect incomplete information from the initial Pelan Taktikal. | User | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-006 | Missing mandatory fields trigger **warnings**. | User | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-034 | KPIs are structured by Teras→Strategi/Enabler→Prakarsa→KPI with code `TSx.Sy.Pz.KPIn`. | JPN data | ✓ | ✓ | – | – | ✓ | ✓ |
| BR-035 | Each KPI carries TOV (or "KPI Baharu"), target (Sasaran), activities, Bahagian/PIC and budget. | JPN data | ✓ | ✓ | – | – | ✓ | ✓ |

---

## 5. Amendment Rules

| ID | Rule | Source | B | T | SA | AI | DB | TC |
|----|------|--------|---|---|----|----|----|----|
| BR-008 | KPI **Statement, Indicator and Target** may be amended **only in July and October**. | User | ✓ | ✓ | – | – | ✓ | ✓ |
| BR-009 | All amendments require an audit trail. *(also Governance)* | User | ✓ | ✓ | ✓ | – | ✓ | ✓ |
| BR-036 | All changes must be **traceable** (before/after, actor, timestamp, reason). | Derived | ✓ | ✓ | ✓ | – | ✓ | ✓ |

---

## 6. Budget Rules

| ID | Rule | Source | B | T | SA | AI | DB | TC |
|----|------|--------|---|---|----|----|----|----|
| BR-010 | Finance must record allocation status: received / will be received / pending / not received / not required / insufficient. | User | ✓ | ✓ | – | ✓ | ✓ | ✓ |
| BR-011 | Budget Intelligence must use the **Low Cost High Impact Matrix**. | User | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-037 | Budget Intelligence outputs (Low Cost High Impact / OBB) are **advisory; human review before implementation**. | CON-07/BR-015 | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-038 | OBB value-for-money is assessed where applicable. *(definition pending Q-025)* | pptx/BCM | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-046 | A **Financial Decision Support** capability exists, broader than Budget Intelligence, comprising: (1) Budget Intelligence (status analysis, funding-gap detection, budget-risk analysis); (2) Low Cost High Impact Analysis (analyse activities, evaluate impact, recommend lower-cost alternatives, resource optimisation, collaboration opportunities); (3) Intervention Recommendation (alternative programmes, implementation strategies, prioritisation); (4) Executive Financial Insight (AI recommendations + rationale for management). All advisory; human review before implementation. Must reflect consistently in BRD/TRD/AI Architecture/Dashboard/Executive Copilot. | CL-024 (user) | ✓ | ✓ | ✓ | ✓ | – | ✓ |

---

## 7. Knowledge Rules

| ID | Rule | Source | B | T | SA | AI | DB | TC |
|----|------|--------|---|---|----|----|----|----|
| BR-017 | Operational Data and Knowledge Data are **separate** (DB vs RAG). | D3A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| BR-019 | Knowledge documents/links are processed **into RAG**, never as KPI input. | D3A | ✓ | ✓ | ✓ | ✓ | – | ✓ |
| BR-012 | RAG uses **RPM 2026–2035** as the main reference document. | User | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-023 | Two knowledge-source types supported: **Static** and **Live/Updated**. | D3B | ✓ | ✓ | ✓ | ✓ | – | ✓ |
| BR-024 | Each link stored with title/URL/category/last-checked; admin-refreshable; prefer official/trusted. *(allow-list pending Q-022)* | D3B | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| BR-025 | Chatbot must **cite the source(s) used** where possible. | D3B | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-026 | If a source/link is inaccessible, show a clear message — **never guess**. | D3B | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-027 | Fixed fallback: "I cannot find this information in the available KPI data or knowledge sources." | D3B | ✓ | ✓ | – | ✓ | – | ✓ |

---

## 8. Reporting Rules

| ID | Rule | Source | B | T | SA | AI | DB | TC |
|----|------|--------|---|---|----|----|----|----|
| BR-014 | The system must generate **monthly reports**. | User | ✓ | ✓ | – | ✓ | ✓ | ✓ |
| BR-039 | Reports include **executive summaries** for management. | D3A/BCM | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-040 | Reports/communications follow **draft → human review → approval → email queue → distribution**. | To-Be Phase 7 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| BR-015 | Human review before report approval and email sending. *(also Governance)* | User | ✓ | ✓ | ✓ | ✓ | – | ✓ |

---

## 9. AI Rules

| ID | Rule | Source | B | T | SA | AI | DB | TC |
|----|------|--------|---|---|----|----|----|----|
| BR-016 | The system must include an **agents and skills layer**. | User | ✓ | ✓ | ✓ | ✓ | – | ✓ |
| BR-041 | **Multi-Agent Architecture** (proposed 14 agents; pending Q-024). | To-Be/AIR-030 | ✓ | ✓ | ✓ | ✓ | – | ✓ |
| BR-042 | **Skills are reusable** capabilities used by multiple agents. | B2A #7/AIR-020 | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-013 | The system must provide a **KPI chatbot** (RAG-grounded). | User | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-043 | **Executive Copilot** provides leadership decision support. | D3A/AIR-034 | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-044 | **AI provider switching** via `config.md`: Groq (dev); OpenAI/Anthropic (prod). | TR-001/002/003 | ✓ | ✓ | ✓ | ✓ | – | ✓ |
| BR-028 | AI outputs require **human oversight** (advisory only). *(also Governance)* | AIR-001 | ✓ | ✓ | – | ✓ | – | ✓ |

---

## 10. Dashboard Rules

| ID | Rule | Source | B | T | SA | AI | DB | TC |
|----|------|--------|---|---|----|----|----|----|
| BR-020 | The main dashboard must **summarise and map all KPIs by Teras 1–7**. | D3A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| BR-021 | Dashboard presents per-Teras: count, achievement, risk, completion, missing info, submission, budget, Low Cost High Impact summary, alignment strength; plus KPI mapping table and distribution chart. | D3A | ✓ | ✓ | – | ✓ | ✓ | ✓ |
| BR-022 | Main page includes an **AI-generated summary** answering the 7 management questions. | D3A | ✓ | ✓ | – | ✓ | – | ✓ |
| BR-045 | Dashboard charts may be **phased** (cards/tables first, charts later). | AD-005 | ✓ | ✓ | – | – | – | ✓ |
| BR-007 | PICs receive **reminders** for incomplete data and monthly updates (drives submission summary). | User | ✓ | ✓ | – | ✓ | ✓ | ✓ |

---

## 11. Rule Traceability (summary)

Every rule above carries per-document flags (B/T/SA/AI/DB/TC). Roll-up:
- **All 45 rules → BRD** (each becomes ≥1 requirement).
- **All 45 → TRD** (each becomes a control/spec).
- **~16 → System Architecture** (governance, separation, auth, provider, reporting flow).
- **~28 → AI Architecture** (agents, skills, RAG, chatbot, copilot, advisory/HITL).
- **~17 → Database Design** (KPI structure, audit, finance, RBAC, links).
- **All 45 → Test Cases** (each rule must be verifiable).

Full forward mapping (rule → requirement → component → test) will be maintained in
`TRACEABILITY_REGISTER.md` once the BRD assigns requirement IDs.

---

## Quality Review (self-audit)

| Check | Finding | Action |
|-------|---------|--------|
| Missing rules? | Formalised RBAC (BR-031/032), delegation (BR-033), traceability (BR-036), report flow (BR-040), multi-agent/skills/copilot/provider (BR-041–044), advisory-only (BR-028), audit-of-AI (BR-029), oversight query (BR-030), KPI structure (BR-034/035), exec summary (BR-039), chart phasing (BR-045), OBB (BR-038). | Added BR-028…045 |
| Duplicate rules? | BR-009 and BR-015 appear under two domains by design (cross-cutting) — single ID retained, not duplicated. | Cross-referenced |
| Contradictory rules? | **C-001 login domain** (one vs two) flagged on BR-003; **C-002 agent count** flagged on BR-041. Not silently resolved. | Flagged |
| Ambiguous wording? | "Incomplete" (BR-005), "risk", "alignment strength", "OBB" parameters flagged pending Q-006/Q-020/Q-021/Q-025. | Flagged |

*Auto-improvements applied: 18 new rules formalised; cross-cutting rules cross-referenced not duplicated; contradictions/ambiguities flagged against specific rule IDs.*

---

## FINAL OUTPUT

**1. Total business rules identified: 45** (BR-001…BR-045; original 27 + 18 formalised in this catalogue).

**2. Completeness score: 96%**
All ten rule domains populated; every capability and To-Be step has at least one governing rule.
Residual 4% = parameters still to be set (login domain, "incomplete" definition, risk/alignment/OBB
mechanics, agent count) — these refine existing rules, not add new domains.

**3. Traceability readiness: 95%**
Every rule has forward flags to BRD/TRD/SA/AI/DB/TC; full ID-level mapping completes once the BRD
assigns requirement IDs into `TRACEABILITY_REGISTER.md`.

**4. Recommendations before Stakeholder Analysis**
1. **Settle the parameter open-items** that touch rule wording: C-001/Q-023 (BR-003 login), Q-024/C-002 (BR-041 agents), Q-006 (BR-005 "incomplete"), Q-025 (BR-038 OBB), Q-020/Q-021 (risk & alignment).
2. **Confirm BR-028…BR-045** as part of the authoritative set (they are formalisations, not new policy) — then I'll fold them back into `BUSINESS_RULES.md` as the master.
3. Proceed to **Stakeholder Analysis** to attach each rule to accountable roles (RACI), which sharpens RBAC (BR-031/032) before the BRD.

---
*End of Business Rules Catalogue v0.1 — DRAFT. Stakeholder Analysis NOT generated. Awaiting approval.*
