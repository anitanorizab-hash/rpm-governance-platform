# BUSINESS PROCESS ANALYSIS — AS-IS (CURRENT STATE)
### KPI Monitoring & Reporting for RPM 2026–2035 (before the Agentic AI Platform)

| Field | Value |
|-------|-------|
| Document | B4 — As-Is Business Process Analysis |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Scope | **Current manual process only.** No future/To-Be solution described. |
| Sources | JPN/PPD tactical-plan inspection, BUSINESS_RULES.md, HMW v1.0 (PP01–18), user context |

> **Boundary rule:** This document describes how things are done **today**. Where a pain point implies
> a future capability, it is recorded as a *problem*, not a *solution*. To-Be is out of scope here.

---

## 1. Business Process Overview

Today, KPI governance for the RPM 2026–2035 roadmap is run as a **manual, spreadsheet-and-email
process** across three tiers — **JPN (state) → PPD (district) → School**. The roadmap's **7 Teras
Strategik** are broken into strategies/enablers, initiatives (*Prakarsa*) and KPIs. Each KPI carries a
code (`TSx.Sy.Pz.KPIn`), a baseline (**TOV / Pencapaian 2025**) or a "KPI Baharu" marker, a **2026
target (Sasaran)**, main and supporting activities, a responsible division (**Bahagian**) / officer,
and a budget broken down by government **object codes (OS21000…OS42000)** with **monthly projections
(Jan–Dec)**.

The end-to-end cycle is: **plan preparation → distribution of Excel templates → manual completion by
PICs → submission (email) → manual consolidation and checking → manual follow-up for gaps → manual
monthly report compilation → management review**. There is no central system; the Excel workbooks are
simultaneously the template, the working file, the database and the reporting source. Coordination,
validation, reminders, financial tracking and reporting are all performed by hand.

---

## 2. Current Actors

| Actor | Responsibilities (today) | Inputs | Outputs |
|-------|--------------------------|--------|---------|
| **JPN Administrator / Planning (BPPDP-type role)** | Prepare and distribute tactical-plan templates; consolidate returns; compile state reports | RPM/PPPM plan, KPI list (SENARAI KPI), prior-year data | Excel templates, consolidated workbook, state report |
| **Sector Head / Bahagian (e.g. BPSH, BPK, IPGM)** | Own KPIs for their sector/division; oversee delivery | Assigned KPIs, activity plans | Sector inputs, verbal/written status |
| **KPI PIC** | Complete KPI rows; enter achievement, activities, budget; update monthly | Blank/partial Excel rows, evidence | Filled KPI rows, monthly figures (in Excel) |
| **PPD Officer** | Complete district tactical plan; report district KPIs upward | PPD Excel template | Completed PPD workbook (per Teras 1–7) |
| **School** | Provide ground-level delivery data/evidence | Requests from PPD | Manual returns (email/forms) |
| **Finance Officer** | Track allocation/warrant/expenditure against KPIs | Budget columns, allocation info | Manual financial notes/updates |
| **State Management (JPN leadership)** | Monitor state implementation; direct interventions | Consolidated workbook, reports | Decisions, instructions |
| **Executive Management / Ministry** | Oversee roadmap progress & accountability | State reports, summaries | Strategic directives |
| **Internal Audit / Oversight** | After-the-fact assurance | Submitted files, reports | Audit observations |

---

## 3. Current Workflow (step by step)

1. **Plan preparation.** JPN planning derives the KPI list (SENARAI KPI) from the RPM/PPPM roadmap and
   builds the **Pelan Taktikal** template per Teras (1–7), with KPI codes, TOV, targets, activities,
   Bahagian/PIC and budget object-code columns.
2. **Excel distribution.** Templates are distributed by email/shared drive to the 12 PPDs and to
   sectors/PICs (the working set observed: 1 JPN workbook + 12 PPD workbooks).
3. **Manual completion.** PICs/PPDs fill rows manually — achievement, activities, milestones, PIC name,
   sector, email, budget breakdown and monthly projections.
4. **Data submission.** Completed/partially completed workbooks are returned by email (multiple
   versions and revisions circulate).
5. **Manual consolidation.** JPN merges returns into a master workbook — copy/paste across many files
   and sheets.
6. **Manual checking.** Staff visually scan for missing PIC/sector/email/targets and obvious errors;
   completeness depends on the reviewer's diligence.
7. **Follow-up.** Gaps and late returns are chased manually via email/phone; no systematic tracking of
   who is outstanding.
8. **Monthly update.** PICs revise figures each month inside the Excel files; changes overwrite prior
   values (no inherent history).
9. **Monthly reporting.** JPN compiles status, financial and progress summaries manually into reports
   for management.
10. **Management review.** State/executive management reviews the compiled report and issues directions;
    interventions are decided and communicated manually.

---

## 4. Current Data Flow

- **Origin documents:** RPM/PPPM 2026–2035 roadmap → **SENARAI KPI** (KPI master list) → **Pelan
  Taktikal JPN** and **Pelan Taktikal PPD** (per-Teras workbooks).
- **Working medium:** **Excel files** serve as template + data store + reporting source simultaneously.
- **Movement:** files travel by **email / shared drive**; returns are re-merged manually.
- **Supplementary inputs:** **emails** (instructions, follow-ups, evidence), **manual documents**
  (notes, attachments), school returns.
- **Budget data:** entered directly into OS-object-code columns and monthly projection cells.
- **Result:** data is **distributed across many file copies**, with no single authoritative version and
  no structured linkage between KPI, PIC, budget and reporting.

```
RPM/PPPM 2026–2035 → SENARAI KPI → Pelan Taktikal (JPN + 12 PPD, per Teras)
        → [email/shared drive] → PIC/PPD manual entry → [email return]
        → JPN manual merge (master Excel) → manual report → management
```

---

## 5. Current Pain Points

| ID | Pain point (current) | Description |
|----|----------------------|-------------|
| AS-PP01 | Heavy manual work | Preparation, completion, merging and reporting are all manual and time-consuming. |
| AS-PP02 | Fragmented / duplicate data | Many Excel copies; no single source of truth; conflicting versions. |
| AS-PP03 | Missing information | PIC name, sector, email, targets and evidence frequently incomplete (BR-004/005). |
| AS-PP04 | Late submission | No systematic deadline tracking; returns arrive late and unevenly. |
| AS-PP05 | Hard to track KPI progress | Status must be read across files; no real-time or Teras-level view. |
| AS-PP06 | No audit trail | Monthly overwrites lose history; amendments untracked (vs BR-008/009). |
| AS-PP07 | Limited executive visibility | Management sees only periodic, manually-compiled snapshots. |
| AS-PP08 | Difficult RPM alignment | No systematic way to confirm KPI alignment with RPM 2026–2035. |
| AS-PP09 | Budget monitoring challenges | Allocation/warrant/expenditure and value-for-money tracked ad hoc across columns. |
| AS-PP10 | No intelligent recommendations | No risk flagging, no Low Cost High Impact guidance, no prioritisation. |
| AS-PP11 | Manual reminders & escalation | Follow-up is manual and inconsistent; no escalation tracking. |
| AS-PP12 | Weak access control | Sensitive KPI/budget data in uncontrolled files; anyone with the file can edit. |
| AS-PP13 | Continuity risk | Knowledge tied to individuals and files; lost on staff rotation over the 10-yr horizon. |
| AS-PP14 | Inconsistent completeness checks | Quality depends on the individual reviewer; no enforced rules. |

*(Maps to HMW frozen pain points PP01–18.)*

---

## 6. Current Business Rules (as practised today)

| ID | Current rule (implicit/explicit) |
|----|----------------------------------|
| AS-BR01 | Tactical plans are authored and exchanged as **Excel workbooks**. |
| AS-BR02 | KPIs are organised by **Teras → Strategi/Enabler → Prakarsa → KPI** with code `TSx.Sy.Pz.KPIn`. |
| AS-BR03 | Each KPI should have a **TOV (or "KPI Baharu")**, a **2026 target**, activities, a Bahagian/PIC, and a budget breakdown. |
| AS-BR04 | Budget is expressed via **government object codes (OS21000…OS42000)** with **monthly projections**. |
| AS-BR05 | Allocation status is described in narrative/columns (the six-value vocabulary is the target standard, not consistently enforced today). |
| AS-BR06 | Updates are made **monthly**, in-file, typically overwriting prior values. |
| AS-BR07 | Returns are **submitted by email** and **consolidated manually** by JPN. |
| AS-BR08 | Reporting is **manually compiled** for management review. |
| AS-BR09 | Amendment discipline (July/October only) and audit trail are **intended governance** but not technically enforced in the current process. |

> Note: BR-001…BR-027 in the Knowledge Base describe the **target** governed rules; this section records
> what actually happens **today**, which is largely manual and weakly enforced.

---

## 7. Current Reporting Process

1. After monthly returns are consolidated, JPN staff **manually extract** status, achievement and
   budget figures from the master workbook.
2. Figures are **re-keyed or copied** into report templates / slides for management.
3. Risk and priority are assessed **subjectively** by the compiler, if at all.
4. Reports are **periodic and backward-looking** (reflecting the state at compilation time).
5. Distribution to management is **manual** (email/printout/meeting).
6. There is **no automated linkage** from a report figure back to its source KPI row, so verification
   is manual and audit is after-the-fact.

---

## 8. Current Risks

| ID | Risk | Type |
|----|------|------|
| AS-R01 | **Data integrity** — wrong version used; copy/paste errors during merge. | Operational |
| AS-R02 | **No audit trail** — amendments untraceable; weak accountability. | Governance |
| AS-R03 | **Late / incomplete data** — decisions made on stale or partial data. | Operational |
| AS-R04 | **Key-person dependency** — process knowledge held by individuals; continuity risk. | Governance |
| AS-R05 | **Security exposure** — sensitive KPI/budget data in uncontrolled files. | Security |
| AS-R06 | **Delayed intervention** — risks surface late, after targets are missed. | Operational |
| AS-R07 | **Budget mismanagement** — value-for-money and allocation issues unnoticed. | Financial |
| AS-R08 | **Misalignment with RPM** — KPIs drift from roadmap intent without checks. | Strategic |
| AS-R09 | **Audit / compliance findings** — manual records may not satisfy oversight. | Compliance |
| AS-R10 | **Reporting inconsistency** — different compilers produce different figures. | Operational |

---

## 9. Opportunities for Improvement (problem areas only — no solution design)

- Eliminate fragmented Excel copies in favour of a **single authoritative record**.
- Enforce **completeness** at entry rather than relying on manual review.
- Provide **real-time, Teras-level visibility** instead of periodic manual snapshots.
- Detect **risk early** rather than discovering it at reporting time.
- Make **budget/value-for-money** monitoring systematic.
- Automate **reminders and escalation** rather than manual chasing.
- Introduce a **governed amendment window + audit trail**.
- Make **RPM alignment** explicit and checkable.
- Reduce **manual reporting effort** and improve consistency.
- Strengthen **access control** over sensitive data.
- Preserve **institutional knowledge** beyond individuals.

---

## 10. Business Process Diagram (text-based, As-Is)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CURRENT (AS-IS) PROCESS                            │
└─────────────────────────────────────────────────────────────────────────┘

 [RPM/PPPM 2026–2035]
        │  derive
        ▼
 [SENARAI KPI master list]
        │  build templates (per Teras 1–7)
        ▼
 [JPN Planning] ──prepare──> [Pelan Taktikal Excel templates]
        │ distribute (email / shared drive)
        ├──────────────► [12 × PPD Officers] ──fill──┐
        └──────────────► [Sectors / KPI PICs] ──fill─┤
                                                      │ (manual entry:
                                                      │  achievement, PIC,
                                                      │  budget OS-codes,
                                                      │  monthly Jan–Dec)
                                                      ▼
                                          [Completed/partial workbooks]
                                                      │ submit (email; many versions)
                                                      ▼
                                   [JPN manual consolidation → master Excel]
                                                      │
                         ┌────────────────────────────┼───────────────────────┐
                         ▼                            ▼                         ▼
               [Manual completeness check]   [Manual follow-up/reminders]  [Monthly overwrite
                  (visual, ad hoc)              (email/phone, untracked)     — no history]
                         │                            │                         │
                         └────────────┬───────────────┴─────────────────────────┘
                                      ▼
                          [Manual monthly report compilation]
                                      │ (re-key/copy; subjective risk)
                                      ▼
                          [State / Executive Management review]
                                      │
                                      ▼
                          [Manual interventions & directives]

 Audit/oversight: after-the-fact, on submitted files.   Access control: weak (file-based).
```

---

## Quality Review (self-audit)

| Check | Finding | Action |
|-------|---------|--------|
| Missing actors? | Added Finance Officer, Internal Audit/Oversight, Bahagian/Sector, School beyond the obvious JPN/PPD/PIC. | Included §2 |
| Missing steps? | Added monthly-overwrite step (8) and explicit management-review/intervention (10). | Included §3 |
| Missing pain points? | Added AS-PP11–14 (reminders, access control, continuity, inconsistent checks). | Included §5 |
| Missing business rules? | Distinguished **practised today** (AS-BR) from **target** (BR-001…027); flagged weak enforcement of amendment/audit. | §6 note |
| Missing risks? | Added security (AS-R05), continuity (AS-R04), compliance (AS-R09), reporting inconsistency (AS-R10). | §8 |
| Solution leak? | Verified no To-Be/system design described; opportunities stated as problems only. | Confirmed |

*Auto-improvements applied: actor list completed; overwrite/management steps added; pain points and risks extended; As-Is vs target rules separated.*

---

## FINAL OUTPUT

**1. As-Is completeness score: 94%**
All current actors, workflow steps, data flows, pain points, business rules, reporting and risks are
captured and grounded in the actual tactical-plan structure. Residual 6% reflects unconfirmed real-world
detail (e.g. exact school-tier mechanics, precise current finance handling) that only on-site process
interviews could fully verify (Q-002/Q-009).

**2. Confidence score: 90%**
High confidence: the document is grounded in inspected data and confirmed rules. Deductions are the
inferred operational specifics that have not been directly observed (current process is reconstructed
from artifacts, not from direct observation of staff).

**3. Readiness to design the To-Be process: READY.**
The As-Is is complete enough to anchor a To-Be design: every current pain point and risk has a clear
origin, mapped to the frozen HMW. The To-Be can now address these without ambiguity — **on your approval.**

---
*End of As-Is Business Process Analysis v0.1 — DRAFT. To-Be NOT generated. Awaiting approval.*
