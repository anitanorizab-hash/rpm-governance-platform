# BUSINESS REQUIREMENTS DOCUMENT (BRD) — OUTLINE / STRUCTURE
### Agentic AI Strategic Governance Platform — RPM 2026–2035

| Field | Value |
|-------|-------|
| Document | B9 — BRD Outline (structure only) |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Purpose | Define the **structure** of the BRD (D2) before writing it |
| Consolidates | HMW v1.0, As-Is, To-Be, BCM, Business Rules Catalogue (45), Master Requirements Catalogue (83) |
| Boundary | Outline only — **no BRD content written yet.** |

> **Review outcome:** the 31 proposed sections are sound. I recommend **3 added sections** (Integration
> Requirements, Data Requirements, Release & Phasing Plan) and **2 consolidations** to remove overlap
> (Low Cost High Impact as a sub-section of Budget Intelligence; AI Features as an umbrella for the AI
> sub-sections). Net structure below = **34 numbered sections**. Every B8 requirement maps to a section
> (see coverage map at end).

---

## 1. Complete BRD Table of Contents (with descriptions)

> Legend: **[orig]** = from your list · **[ADDED]** = new, with justification · **[merged]** = overlap consolidated.

### Front matter & context
1. **Document Control** [orig] — Version history, authors, reviewers, approvers, sign-off, distribution, change-control and freeze status. *Single place for governance of the BRD itself.*
2. **Executive Summary** [orig] — One-page synthesis: problem, solution intent, scope, value, key decisions. *Written last; read first by executives.*
3. **Project Background** [orig] — RPM 2026–2035, 7 Teras, JPN/PPD/School context, why now. *From HMW §1 + As-Is overview.*
4. **Business Objectives** [orig] — Confirmed business objectives and target outcomes. *From HMW success criteria + BRQ-001…012.*
5. **Project Scope** [orig] — Overall scope statement and boundaries. *From To-Be + B2A decisions.*
6. **In Scope / Out of Scope** [orig] — Explicit inclusions/exclusions; pilot (Perak) vs national note. *Resolves scope ambiguity (Q-002/Q-003).*
7. **Release & Phasing Plan** [ADDED] — V1 (Must) vs later phases (Should/Could/Future) from the MoSCoW summary. *Justification: 83 requirements with 6 deferrable items need an explicit phasing decision; prevents scope overload in V1.*

### Stakeholders & process
8. **Stakeholder Analysis** [orig] — Roles, interests, influence, desired outcomes, RACI. *From HMW §3 + BCM roles; to be enriched by the Stakeholder Analysis step.*
9. **Current Business Process (As-Is)** [orig] — Summary of the current manual process. *Reference B4; do not duplicate fully.*
10. **Future Business Process (To-Be)** [orig] — The 7-phase target workflow. *Reference B5 master blueprint.*
11. **Business Capability Model** [orig] — 10 domains, ~35 capabilities, maturity. *Reference B6.*

### Rules & requirements
12. **Business Rules** [orig] — The 45 governing rules by domain. *Reference B7; cite BR IDs.*
13. **Functional Requirements** [orig] — FRQ-001…028 with descriptions, priority, traceability. *Core of the BRD.*
14. **Non-Functional Requirements** [orig] — NFRQ-001…013 (security, performance, scalability, availability, maintainability, auditability, integrity, compliance, localisation, retention).
15. **Integration Requirements** [ADDED] — INTQ-001…005 (Excel import, live links, email, LLM providers, future SharePoint). *Justification: B8 has a distinct Integration category with 5 requirements and no home in the original 31.*
16. **Data Requirements (business-level)** [ADDED] — DATQ-001…007 (initial dataset, operational DB, knowledge repository, audit store, finance data, link registry, reference/master data) at business level. *Justification: B8 Data category (7 reqs) needs a business-level home; detailed schema stays in the TRD.*

### Roles, UX & feature areas
17. **User Roles and Permissions** [orig] — Role catalogue + permission matrix (RBAC). *From BR-031/032; FRQ-002.*
18. **Dashboard Requirements** [orig] — Teras 1–7 summaries, mapping table, charts (phased), AI/executive summary. *From BR-020/021/022; FRQ-011/012, REPQ-003/006.*
19. **AI Features (umbrella)** [orig, merged] — Overview of the AI solution and how the sub-sections relate. *Parent for 20–24 to avoid duplication.*
   - 19.1 **AI Agents** [orig] — The agent roster (14 proposed; Q-024), purpose/inputs/outputs.
   - 19.2 **Skills Layer** [orig] — Reusable skills and agent mapping.
   - 19.3 **Knowledge Management (RAG)** [orig] — Static + live sources, ingestion, retrieval, citation, fallback.
   - 19.4 **Budget Intelligence** [orig] — Allocation analysis + recommendations.
     - 19.4.1 **Low Cost High Impact Matrix** [orig, merged] — *Recommended as sub-section of Budget Intelligence (it is the method Budget Intelligence applies), removing duplicate top-level section.*
   - 19.5 **Executive Copilot & AI Summary** [ADDED sub] — Leadership decision support + dashboard summary. *Justification: these AI capabilities (AIRQ-008/010) otherwise lack an explicit home.*

### Cross-cutting requirements
20. **Reporting Requirements** [orig] — Monthly report, executive summary, archive. *REPQ-001…005.*
21. **Notification Requirements** [orig] — Reminders, alerts, escalation, approved distribution. *FRQ-018/019; BR-007/040.*
22. **Security Requirements** [orig] — Auth, RBAC, data protection, **Compliance & Data Residency** (sub-section). *NFRQ-001/011; pending Q-014/Q-017/Q-022.*

### Closure
23. **Constraints** [orig] — CON-01…10 (Excel input-once, MOE login, Jul/Oct, HITL, advisory AI, separation, provider config).
24. **Assumptions** [orig] — Working assumptions (pilot, naming, school tier, language).
25. **Dependencies** [ADDED] — External/internal dependencies (knowledge corpus availability, provider access, identity source). *Justification: government projects depend on external inputs; needed for realistic planning.*
26. **Risks** [orig] — Business/governance risks + mitigations (from As-Is risks + adoption/political).
27. **Success Criteria** [orig] — Measurable success measures. *From HMW §6.*
28. **Traceability Summary** [orig] — HMW → BRD → (forward to TRD/Arch/Test) mapping summary. *From TRACEABILITY_REGISTER.*
29. **Glossary** [orig] — Terms & abbreviations. *Reference PROJECT_GLOSSARY.*
30. **Appendices** [orig] — Source data structures, KPI code scheme, object-code list, open-questions register, supporting tables.

> Original sections 16–21 (AI Features, AI Agents, Skills Layer, Knowledge Management, Budget
> Intelligence, Low Cost High Impact) are **preserved** but re-nested under §19 to eliminate duplication
> and show their real relationship. Numbering renders as 34 logical sections (30 top-level + sub-sections).

---

## 2. Review Findings

| Check | Finding |
|-------|---------|
| Duplicate sections? | **Low Cost High Impact (21)** duplicates **Budget Intelligence (20)** → merged as §19.4.1. **AI Features (16)** overlapped **17–21** → made the umbrella §19. |
| Missing sections? | **Integration**, **Data**, **Release/Phasing**, **Dependencies** were absent → added with justification. Compliance folded into Security as a sub-section. |
| Every requirement placed? | Yes — all 83 B8 requirements map to a section (see coverage map). All 45 rules → §12. |
| Justified additions only? | Yes — 4 added sections each tied to a B8 category or government-project necessity. |

### Requirement → Section coverage map
| B8 category | Lives in BRD section |
|-------------|----------------------|
| BRQ (Business) | §4 Objectives, §5/6 Scope |
| FRQ (Functional) | §13 (+ §17 roles, §18 dashboard, §19 AI, §20 reporting, §21 notification) |
| NFRQ (Non-functional) | §14 (+ §22 security) |
| AIRQ (AI) | §19 (and sub-sections) |
| INTQ (Integration) | §15 |
| DATQ (Data) | §16 |
| REPQ (Reporting) | §20 (+ §18 dashboard) |

---

## 3. Recommended Writing Order

Writing order ≠ reading order. Recommended sequence (build context first, summarise last):

1. **§3 Background → §4 Objectives → §5/6 Scope → §7 Phasing** (frame the problem & boundaries)
2. **§8 Stakeholders** (after the Stakeholder Analysis step)
3. **§9 As-Is → §10 To-Be → §11 Capabilities** (reference existing frozen/approved artefacts)
4. **§12 Business Rules** (anchor)
5. **§13 Functional → §14 Non-functional → §15 Integration → §16 Data** (the requirement core)
6. **§17 Roles → §18 Dashboard → §19 AI (agents/skills/RAG/budget/copilot)** (feature areas)
7. **§20 Reporting → §21 Notification → §22 Security** (cross-cutting)
8. **§23 Constraints → §24 Assumptions → §25 Dependencies → §26 Risks → §27 Success Criteria**
9. **§28 Traceability → §29 Glossary → §30 Appendices**
10. **§2 Executive Summary** (write last)
11. **§1 Document Control** (finalise version/sign-off at the end)

*Rationale: requirements and feature sections depend on rules and scope; the executive summary and
document control can only be accurate once the body is stable.*

---

## 4. Estimated Page Count (completed BRD)

| Block | Sections | Est. pages |
|-------|----------|-----------|
| Front matter & context | 1–7 | 8–10 |
| Stakeholders & process | 8–11 | 10–14 |
| Rules & requirements | 12–16 | 22–30 |
| Roles, UX & AI | 17–19 | 14–20 |
| Cross-cutting | 20–22 | 8–11 |
| Closure | 23–30 | 10–14 |
| **Total** | | **~72–99 pages** |

> Estimate for an enterprise government BRD with full requirement tables and traceability. A leaner
> V1-scoped BRD (Must-have only, referencing rather than reproducing As-Is/To-Be/BCM) would be **~45–60 pages**.

---

## Final Note

The outline is complete and every confirmed requirement and rule has a defined home. Two recommendations
before writing the BRD:
1. **Decide BRD breadth** — full (~72–99 pp, all MoSCoW) vs V1-scoped (~45–60 pp, Must-have, phased).
2. **Confirm the open parameters** that affect specific sections (login domain §22, agent roster §19.1,
   OBB §19.4, risk/alignment §13/§18, pilot/school §6) — or I write with flagged assumptions.

---
*End of BRD Outline v0.1 — DRAFT. Full BRD NOT written. Awaiting approval.*
