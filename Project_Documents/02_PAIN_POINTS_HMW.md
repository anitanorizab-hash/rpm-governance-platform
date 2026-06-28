# HOW MIGHT WE (HMW) DOCUMENT
### Agentic AI Strategic Governance Platform for RPM 2026–2035

| Field | Value |
|-------|-------|
| Document | D1 — HMW & Problem Discovery |
| Version | **1.0 (FROZEN — APPROVED BASELINE)** |
| Date | 2026-06-27 |
| Frozen on | 2026-06-27 by user approval (B2A → Freeze) |
| Status | Draft → Audited (B2) → Revised → **FROZEN ✅** |
| Change control | Reopened only via an explicit, logged change request from the user. |
| Foundation for | BRD (D2) |
| Sources | User context + D3/D3A/D3B corrections, `BUSINESS_RULES.md` (BR-001…BR-027), `project_structure.pptx` (draft pain points PP01–PP10, HMW01–HMW10), JPN/PPD data inspection |

> **Scope note:** This document frames *business problems and desired outcomes only*. No technical
> solutions are proposed. Working assumptions are stated in §11 and flagged in Remaining Questions.

---

## 1. Project Background

The Ministry of Education (Kementerian Pendidikan Malaysia) is executing **RPM 2026–2035**, a ten-year
national education roadmap organised into **7 Teras Strategik (strategic pillars)**. The roadmap is
delivered through tactical plans (**Pelan Taktikal**) at **State (JPN)** and **District (PPD)** level,
cascading to **schools**. Each plan contains KPIs with baselines (TOV), 2026 targets, activities,
responsible divisions/PICs, and budget allocations broken down by government object codes.

Today, this execution is tracked in **many separate Excel files** across JPN and the PPDs (the working
data set covers **Perak: 1 JPN plan + 12 PPD district plans**). There is no central platform: monitoring,
reporting, financial review and intervention are largely manual. Over a **ten-year horizon** spanning
staff rotation and leadership change, this fragmented approach threatens the continuity, auditability and
strategic coherence of the roadmap.

This project is needed to replace the spreadsheet-based process with a **single, audit-grade governance
platform** that centralises KPI data, enforces disciplined monthly updates, and uses **agentic AI to
assist — never replace — human decision-makers** in monitoring performance, analysing budget, detecting
risk, recommending interventions, and supporting executive decisions, all grounded in the RPM 2026–2035
knowledge base.

---

## 2. Current Business Challenges

| ID | Challenge | Description | Origin |
|----|-----------|-------------|--------|
| PP01 | Fragmented KPI data | KPI data stored across many Excel files (JPN + 12 PPD), no single source of truth. | pptx PP01 |
| PP02 | No central monitoring platform | No unified, real-time view of KPI status across Teras/tiers. | pptx PP02 |
| PP03 | Manual reporting | Monthly reports compiled manually — slow, inconsistent, effort-heavy. | pptx PP03 |
| PP04 | No early-warning mechanism | At-Risk / Critical KPIs are not detected early. | pptx PP04 |
| PP05 | Unsystematic financial monitoring | Allocation, warrant and expenditure not monitored systematically. | pptx PP05 |
| PP06 | Manual OBB / value-for-money analysis | Outcome-based budget analysis done by hand. | pptx PP06 |
| PP07 | Slow intervention | Corrective action is reactive and delayed. | pptx PP07 |
| PP08 | No real-time management visibility | Leadership lacks an up-to-date strategic view. | pptx PP08 |
| PP09 | Data completeness issues | Missing PIC, sector, email, targets, evidence in initial plans. | pptx PP09 / BR-004/005 |
| PP10 | Manual email reminders | Reminders and escalations handled manually and inconsistently. | pptx PP10 |
| PP11 | Weak RPM alignment visibility | No systematic way to see how each KPI aligns with RPM 2026–2035 and its strength. | D3A (BR-020), Q-021 |
| PP12 | Dispersed institutional knowledge | RPM, guidelines, circulars and updates are scattered; hard to consult while working on KPIs. | D3A/D3B (BR-012/023) |
| PP13 | Uncontrolled amendments | KPI statements/indicators/targets can drift without governance or audit. | BR-008/009 |
| PP14 | Limited collaboration across tiers | JPN ↔ PPD ↔ School coordination is manual and opaque. | User context |
| PP15 | No decision-support synthesis | Management has data but no synthesised, prioritised guidance. | D3A §4 |
| PP16 | AI trust & adoption gap | Users may distrust or under-adopt AI guidance and in-system entry; change management is non-trivial in a government setting. | B2 audit |
| PP17 | Weak access control over sensitive data | Sensitive KPI and budget data sit in uncontrolled Excel with no role-based access; exposure and accountability risk. | B2 audit / BR-003 |
| PP18 | Continuity & institutional-memory risk | Over the 10-year horizon, staff rotation and leadership change erode roadmap continuity and knowledge. | B2 audit / §1 |

---

## 3. Stakeholders

| Stakeholder | Role | Current challenges | Desired outcome |
|-------------|------|--------------------|-----------------|
| **KPI PIC** | Owns and updates a KPI's data, evidence, finance | Manual Excel entry; chased by email; unclear what's missing | Simple in-system monthly update; clear prompts for missing info |
| **PPD Officer** | District-level KPI accuracy & reporting | Compiling district data manually; version conflicts | Accurate, real-time district KPI view; less rework |
| **JPN Officer** | State-level monitoring & oversight | No consolidated state view; slow aggregation | One state-wide, Teras-level monitoring view |
| **Sector Head** | Sector oversight & intervention | Late awareness of at-risk KPIs | Early alerts enabling timely intervention |
| **Finance Officer** | Budget / OBB monitoring | Allocation & spending tracked ad hoc | Systematic allocation status & value-for-money view |
| **Top Management / State Management** | Strategic decisions | No real-time, prioritised insight | Executive dashboard + AI summary for faster decisions |
| **Ministry (MOE) leadership** | National roadmap accountability | Hard to assure roadmap progress & auditability | Auditable, aligned, evidence-based progress on RPM |
| **System / Governance Admin** *(inferred, Q-005)* | Users, windows, audit, knowledge links | — | Controlled governance of access, windows, knowledge |
| **Schools** *(reporting tier, scope Q-002)* | Source of ground-level delivery | Manual, opaque reporting upward | Clear, low-effort contribution to KPI evidence |
| **Implementing Divisions (Bahagian Pelaksana)** | National divisions accountable for KPIs (e.g. BPSH, BPK, IPGM) | KPI accountability split across divisions; no shared view | Clear division-level ownership and visibility |
| **Internal Audit / Oversight** | Assurance over governance & compliance | Audit done after-the-fact on scattered records | Built-in, queryable audit trail |
| **IT / Platform Operations** | Runs the platform, config, knowledge refresh | Manual, fragmented tooling | Stable, configurable, maintainable platform |

---

## 4. Problem Statements

*Format: Current Situation → Problem → Impact.*

- **PS-01 (from PP01/PP02).** KPI data lives in many Excel files with no central platform → there is no
  single source of truth or real-time monitoring → leadership cannot see true, current status; errors and
  duplication multiply.
- **PS-02 (PP09).** Initial tactical plans contain missing PIC, sector, email and target information →
  records are incomplete and unverifiable → KPIs cannot be owned, monitored or actioned reliably.
- **PS-03 (PP03/PP08).** Reports are compiled manually each month → reporting is slow, inconsistent and
  backward-looking → management decisions are delayed and based on stale data.
- **PS-04 (PP04/PP07).** There is no early-warning mechanism → at-risk KPIs surface late → interventions
  are reactive and corrective windows are missed.
- **PS-05 (PP05/PP06).** Allocation, warrant, expenditure and OBB value-for-money are tracked manually →
  financial monitoring is unsystematic → budget risk and poor value-for-money go unnoticed.
- **PS-06 (PP10).** Reminders and escalations are manual → follow-up is inconsistent → data gaps persist
  and accountability weakens.
- **PS-07 (PP11/PP12).** KPI alignment to RPM and supporting knowledge is dispersed → officers cannot
  easily confirm strategic alignment or consult guidance → KPIs drift from roadmap intent.
- **PS-08 (PP13).** Amendments to KPI statements/indicators/targets are uncontrolled → plans change
  without governance or trail → audit and accountability are compromised.
- **PS-09 (PP14).** JPN↔PPD↔School coordination is manual → collaboration is opaque and slow → effort is
  duplicated and issues fall between tiers.
- **PS-10 (PP15).** Management receives data but no synthesised guidance → decision-makers must interpret
  raw numbers themselves → strategic focus is diffused and slow.
- **PS-11 (PP16).** A new AI-driven system is introduced into established manual habits → users may distrust
  AI output or under-use in-system entry → adoption stalls and the platform's value is not realised.
- **PS-12 (PP17).** Sensitive KPI/budget data sits in uncontrolled files with no role-based access →
  data exposure and unclear accountability → governance, privacy and audit risk.
- **PS-13 (PP18).** The roadmap spans ten years with rotating staff and leadership → knowledge and
  continuity are lost at handover → strategic execution degrades over time.

---

## 5. How Might We Statements

> IDs are stable and will be traced into BRD requirements. Each HMW links to problem statement(s).

### A. Centralisation & data integrity
- **HMW-01** How might we centralise all JPN, PPD and school KPI data into one trusted source? *(PS-01)*
- **HMW-02** How might we reduce incomplete KPI information at import and over time? *(PS-02)*
- **HMW-03** How might we ensure every KPI has a clear owner (PIC), sector and contact? *(PS-02)*
- **HMW-04** How might we make controlled, auditable amendments without losing governance? *(PS-08)*

### B. Monitoring, risk & intervention
- **HMW-05** How might we give a clear, real-time view of KPI status across the 7 Teras? *(PS-01/PS-03)*
- **HMW-06** How might we help management identify high-risk KPIs earlier? *(PS-04)*
- **HMW-07** How might we shorten the time from risk detection to intervention? *(PS-04)*

### C. Budget intelligence
- **HMW-08** How might we monitor allocation, warrant and expenditure systematically? *(PS-05)*
- **HMW-09** How might we assess budget value-for-money (OBB) consistently? *(PS-05)*
- **HMW-10** How might we recommend Low Cost High Impact alternatives when allocation is unavailable or insufficient? *(PS-05)*

### D. Reporting & decision support
- **HMW-11** How might we reduce manual monthly reporting effort? *(PS-03)*
- **HMW-12** How might we give management synthesised, prioritised decision support? *(PS-10)*
- **HMW-13** How might we summarise overall status and focus areas for management each month? *(PS-10)*

### E. Communication & collaboration
- **HMW-14** How might we automate reminders for incomplete data and monthly updates? *(PS-06)*
- **HMW-15** How might we track escalation automatically when follow-up is needed? *(PS-06)*
- **HMW-16** How might we improve collaboration and transparency between JPN, PPD and schools? *(PS-09)*

### F. Alignment & knowledge
- **HMW-17** How might we ensure and show KPI alignment with RPM 2026–2035? *(PS-07)*
- **HMW-18** How might we make RPM, guidelines and updated knowledge easy to consult while working? *(PS-07)*
- **HMW-19** How might we keep knowledge current when some sources are live/online links? *(PS-07)*

### G. Trust & governance
- **HMW-20** How might we keep humans in control of every formal action, approval and communication? *(constraint, BR-015)*
- **HMW-21** How might we make AI guidance trustworthy, source-cited and honest about what it doesn't know? *(BR-025/027)*

### H. Adoption, security & continuity *(added in B2 audit)*
- **HMW-22** How might we drive user adoption and trust so officers prefer the system over Excel? *(PS-11)*
- **HMW-23** How might we ensure only the right people access sensitive KPI and budget data? *(PS-12)*
- **HMW-24** How might we preserve continuity and institutional memory across the 10-year horizon and staff changes? *(PS-13)*
- **HMW-25** How might we make KPI ownership clear across implementing divisions, JPN and PPD? *(PS-02/PS-12)*

---

## 6. Success Criteria

The problems are solved when:
1. **One source of truth:** all JPN/PPD KPI data is centralised; Excel is used only for the initial import. *(HMW-01)*
2. **Completeness:** every KPI has PIC name, sector and email; missing-information warnings approach zero. *(HMW-02/03)*
3. **Timeliness:** monthly updates are submitted in-system on cadence; status is real-time. *(HMW-05/14)*
4. **Early risk visibility:** at-risk/critical KPIs are flagged before targets are missed. *(HMW-06/07)*
5. **Financial control:** allocation status and value-for-money are visible and systematic. *(HMW-08/09/10)*
6. **Reporting effort down:** monthly reports are generated (human-approved) with minimal manual effort. *(HMW-11)*
7. **Executive clarity:** management sees a Teras-level dashboard + AI summary answering the key questions. *(HMW-12/13)*
8. **Alignment assured:** each KPI's alignment with RPM is visible and traceable. *(HMW-17)*
9. **Governed change & audit:** amendments occur only in July/October and are fully logged. *(HMW-04)*
10. **Trusted AI:** AI is advisory, source-cited, human-gated, and honest about gaps. *(HMW-20/21)*
11. **Adoption:** officers actively prefer in-system entry over Excel; AI guidance is trusted and used. *(HMW-22)*
12. **Secure access:** sensitive KPI/budget data is protected by role-based access. *(HMW-23/25)*
13. **Continuity:** roadmap knowledge and ownership survive staff/leadership change over 10 years. *(HMW-24)*

---

## 7. Opportunities

*(Opportunities only — not solution designs.)*
- **AI:** KPI status interpretation, risk detection, summarisation, alignment scoring.
- **Agentic AI:** autonomous-but-gated agents that monitor, analyse, draft and recommend.
- **Multi-Agent:** specialised agents per concern (monitoring, finance/OBB, budget intelligence, intervention, notification, reporting, alignment, chatbot, executive copilot).
- **Skills Layer:** reusable capabilities (completeness check, status/risk scoring, Low Cost High Impact scoring, Teras roll-up, report templating, retrieval+citation).
- **RAG:** grounding answers in RPM 2026–2035 + guidelines + live links.
- **Dashboard:** Teras-centric summarisation and KPI mapping as the primary management view.
- **Executive Copilot:** synthesised decision support for leadership.
- **Budget Intelligence:** Low Cost High Impact prioritisation and value-for-money guidance.
- **Human Review:** approval gates before any formal action/report/email.
- **Automation:** reminders, escalation tracking, monthly report drafting.

---

## 8. Business Value

| Beneficiary | Expected value |
|-------------|----------------|
| **JPN** | One real-time, state-wide Teras view; faster, evidence-based oversight; less manual aggregation. |
| **PPD** | Accurate district KPIs with less rework; clear visibility of obligations and gaps. |
| **Schools** | Lower-effort, clearer contribution to KPI evidence; transparency on expectations. |
| **KPI PIC** | Simple guided updates; fewer chasing emails; clarity on what's missing and due. |
| **State Management** | Prioritised, synthesised insight; earlier risk awareness; faster strategic decisions. |
| **Ministry (MOE)** | Auditable, aligned, continuous progress on RPM 2026–2035 across a 10-year horizon. |

---

## 9. Constraints

| ID | Constraint | Source |
|----|-----------|--------|
| CON-01 | Excel is used for **initial import only**; database is the working source thereafter. | BR-001/018 |
| CON-02 | Monthly KPI updates are **keyed in-system by the PIC**. | BR-002 |
| CON-03 | Login restricted to MOE email accounts (**domain rule pending C-001/Q-023**). | BR-003 |
| CON-04 | KPI statement/indicator/target editable **only in July and October**. | BR-008 |
| CON-05 | **All amendments audited.** | BR-009 |
| CON-06 | **Human approval required** before formal action, report approval, email send. | BR-015 |
| CON-07 | **AI is advisory only** — proposes, never finally acts; answers cited; honest fallback. | BR-015/025/027 |
| CON-08 | Operational data → database; knowledge data/links → RAG (separate planes). | BR-017–019 |
| CON-09 | Main dashboard must **summarise & map KPIs by the 7 Teras**. | BR-020/021 |
| CON-10 | Provider config: Groq (dev), OpenAI/Anthropic (prod) via `config.md`. | TR-001/002 |

---

## 10. Recommendations (business priorities before BRD)

1. **Anchor the BRD on centralisation + completeness + Teras dashboard** — these (HMW-01/02/03/05/13) are the highest-value, lowest-ambiguity foundations.
2. **Confirm V1 vs later phases**: recommend V1 = import, completeness, monthly update, Teras dashboard, core monitoring/risk, chatbot; **phase** OBB, full Low Cost High Impact automation, live-link RAG and the full agent roster.
3. **Settle the 4 framing decisions** (pptx authority, pilot/national + school login, agent roster, RPM/PPPM naming) so BRD requirements are precise.
4. **Treat human-review and AI-advisory as non-negotiable cross-cutting requirements** in every BRD feature.
5. **Prioritise the adoption problem (PIC data-entry friction)** as a first-class business requirement, not an afterthought.

---

## 11. Working Assumptions (stated, not hidden)

1. `project_structure.pptx` is a **draft input**, subordinate to this gated process (pending Q-027).
2. Initial scope is a **Perak pilot** (1 JPN + 12 PPD) ahead of national rollout (Q-003).
3. Schools are primarily a **reporting/evidence tier** in V1 (Q-002).
4. **RPM 2026–2035 ≡ PPPM 2026–2035** (terminology drift) until told otherwise (C-003/Q-001).
5. Primary content language is **Bahasa Malaysia**; UI language to confirm (Q-012).

---

## 12. HMW Quality Check (self-audit)

| Check | Result | Action taken |
|-------|--------|--------------|
| Missing business problem? | Added PP11–PP15 (alignment, knowledge, amendments, collaboration, decision-synthesis) beyond pptx PP01–PP10. | Revised §2 |
| Duplicate problem? | PP03/PP08 (reporting/visibility) and PP04/PP07 (risk/intervention) overlap → consolidated into PS-03 and PS-04. | Revised §4 |
| Missing stakeholder? | Added Sector Head, Finance Officer, Ministry, System/Governance Admin, Schools beyond pptx's 4 roles. | Revised §3 |
| Missing opportunity? | Added Skills Layer, RAG, Human Review, Executive Copilot, Alignment. | Revised §7 |
| Missing business rule? | Mapped constraints to BR-001…BR-027 incl. D3A/D3B (separation, dashboard, knowledge, fallback). | §9 |
| Contradictions? | Login-domain (C-001) and agent-count (C-002) contradictions noted, not resolved here; flagged. | §9, Remaining Qs |
| Solutioning leak? | Verified §1–§10 describe problems/outcomes, not technical solutions. | Confirmed |

*Auto-revisions applied (v0.1): pain points expanded (PP11–15); duplicates consolidated at problem-statement level; stakeholders and opportunities completed; constraints traced to BR IDs.*

### B2 audit revisions (v0.2)
- **Added:** pain points PP16 (AI trust/adoption), PP17 (access control), PP18 (continuity/memory);
  problem statements PS-11/12/13; HMW-22/23/24/25 (Group H); success criteria 11/12/13;
  stakeholders Implementing Divisions (Bahagian Pelaksana), Internal Audit/Oversight, IT/Platform Operations.
- **Removed:** none (nothing found incorrect).
- **Updated:** version 0.1→0.2; final scores recalculated; AI value made explicit via PP16/HMW-22.

---

## FINAL OUTPUT

> **Updated after B2 audit (v0.2).**

**1. HMW completeness score: 97%** (was 92%)
Rationale: B2 closed the adoption, security/access and continuity problem gaps and the three missing
stakeholders. Residual 3% = unconfirmed scope/agent-roster precision.

**2. Confidence score: 90%** (was 88%)
Deductions are the two open, *logged* contradictions (login domain, agent count) and pilot/scope
confirmation — none change the problems, only their boundaries.

**3. Remaining questions (carried for BRD)**
- Q-027 — Is `project_structure.pptx` authoritative or draft? *(affects baseline)*
- Q-003 / Q-002 — Perak pilot vs national; do schools log in? *(affects scope of HMW-16)*
- Q-024 / C-002 — the authoritative agent roster (target 14). *(affects opportunity sizing)*
- Q-023 / C-001 — login domain (one domain vs two).
- Q-025 — OBB definition & relation to Low Cost High Impact *(HMW-09/10 precision)*.
- Q-020 / Q-021 — definitions of KPI "risk" and "RPM alignment strength" *(HMW-06/17)*.
- Q-001 / C-003 — RPM vs PPPM official naming.

**4. Recommendations before BRD**
1. Resolve the 4 framing decisions (pptx authority, pilot/school scope, agent roster, naming).
2. Confirm V1 scope vs phased items (OBB, live-link RAG, full agent set).
3. Approve this HMW (or request revisions) so it can be **frozen** as the foundation the BRD traces to.
4. Provide the knowledge corpus + live-link list to ground the later RAG/Knowledge Base design.

---

## FREEZE RECORD
- **Baseline:** D1 — HMW & Problem Discovery, **v1.0 FROZEN** on 2026-06-27.
- **Approved by:** User (suzila@iegcampus.com).
- **Contents locked:** 18 pain points (PP01–18), 12 stakeholders, 13 problem statements (PS-01–13),
  25 HMW statements (HMW-01–25), 13 success criteria, 10 constraints (CON-01–10).
- **Precedence:** Subordinate to the B2A authoritative decisions; the BRD must trace to this baseline.
- **Residual open items** (do NOT block freeze; carried to BRD for precision, not foundation):
  Q-001/C-003 (RPM vs PPPM naming), Q-002/Q-003 (school login, pilot vs national), Q-023/C-001
  (login domain), Q-024/C-002 (14-agent roster), Q-025 (OBB), Q-020/Q-021 (risk & alignment-strength).
- **Reopen policy:** changes only via explicit, logged change request (recorded in CHANGE_LOG.md).

---
*End of HMW Document v1.0 — FROZEN APPROVED BASELINE. Foundation for the BRD (D2).*
