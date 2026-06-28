# SKILLS LAYER DESIGN BLUEPRINT
### Agentic AI Strategic Governance Platform — RPM 2026–2035
#### Implementation guide for the `/skills` module

| Field | Value |
|-------|-------|
| Document | A3 — Skills Layer Design Blueprint |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Audience | Developers implementing `/skills` |
| Baselines (frozen, not modified) | HMW v1.0, BRD v1.0, RTM v1.0, TRD v1.0, A1, A2 |
| Boundary | Architecture only — **no code**; implements frozen baselines (no new requirements). |

> **What a Skill is here.** A **reusable, independently-testable capability** invoked by one or more agents
> (BR-016/042). Skills **compute/draft**; agents **orchestrate**; services **own the data**. Skills **never**
> approve or change official records (design rule 5), never access the DB directly (they receive data from
> agents/services), are **versioned**, **logged when used by AI**, and **support the human-review workflow**
> (they output drafts/scores, not actions). Agents map = A2 (1 KPI Analysis, 2 Validation, 3 FDS, 4 Risk,
> 5 Strategic Recommendation, 6 Knowledge Alignment, 7 Chatbot, 8 Report, 9 Notification, 10 Audit, 11 Copilot).

---

## 1. Skills Catalogue

### S1 — KPI Analysis Skill
- **Purpose:** classify KPI status vs target and compute progress.
- **Inputs:** KPI record, monthly updates, target/TOV.
- **Outputs:** status (on-track/lagging/achieved), progress %.
- **Used by:** KPI Analysis Agent, Report Generation, Executive Copilot.
- **Data access:** receives data from caller (no direct DB).
- **Knowledge access:** none.
- **Type:** Deterministic (rule-based).
- **Validation rules:** target present; period valid; handle "KPI Baharu" (no TOV).
- **Failure behaviour:** return "status unavailable" for the KPI; never default to on-track.
- **Logging:** inputs ref, output status, version, timestamp (when used by AI).
- **Implementation notes:** pure function; table-driven thresholds; unit-testable.

### S2 — Validation Skill
- **Purpose:** detect incomplete/inconsistent mandatory fields.
- **Inputs:** KPI/monthly-update record + field ruleset.
- **Outputs:** list of missing/invalid fields, completeness flag.
- **Used by:** Validation Agent, KPI Analysis Agent.
- **Data access:** caller-supplied.
- **Knowledge access:** none.
- **Type:** Deterministic.
- **Validation rules:** PIC name/sector/email present; target present; types valid.
- **Failure behaviour:** fail safe — if cannot evaluate, mark "validation pending" (never auto-pass).
- **Logging:** record id, issues, version, timestamp.
- **Implementation notes:** rule config externalised; reusable for import + monthly update.

### S3 — Risk Scoring Skill
- **Purpose:** score KPI risk (At-Risk/Critical).
- **Inputs:** progress vs target/time, thresholds.
- **Outputs:** risk level + factors.
- **Used by:** Risk Assessment Agent, Strategic Recommendation, Executive Copilot.
- **Data access:** caller-supplied.
- **Knowledge access:** none.
- **Type:** Deterministic (rule-based V1; AI-assisted later — TASM-07).
- **Validation rules:** require progress + timeline; bounded score.
- **Failure behaviour:** return "risk unknown"; never silently mark low-risk.
- **Logging:** method, score, inputs, version, timestamp.
- **Implementation notes:** thresholds configurable; deterministic for testability.

### S4 — Financial Decision Support Skill ⭐
- **Purpose:** core FDS computations — budget status, **funding-gap detection**, **budget-risk analysis**.
- **Inputs:** FinanceAllocation (6-value status, OS codes, expenditure), planned need, KPI/risk context.
- **Outputs:** budget status summary, funding gaps, budget-risk flags.
- **Used by:** FDS Agent, Report Generation, Executive Copilot.
- **Data access:** caller-supplied (from FinanceService).
- **Knowledge access:** none (numeric); narrative grounding via S9/S10 if needed.
- **Type:** Deterministic (computations).
- **Validation rules:** allocation status ∈ six-value vocabulary; amounts numeric; no negative expenditure.
- **Failure behaviour:** return partial analysis with explicit gaps; never fabricate figures.
- **Logging:** inputs, outputs, version, timestamp.
- **Implementation notes:** pure calculations; feeds S5/S6; testable with fixtures.

### S5 — Low Cost High Impact Matrix Skill ⭐
- **Purpose:** position activities on cost-vs-impact; recommend lower-cost alternatives + resource optimisation.
- **Inputs:** activities (cost), expected impact, KPI linkage.
- **Outputs:** matrix placement, ranked recommendations (alternatives, **collaboration, consolidation, shared resources, digital alternatives**).
- **Used by:** FDS Agent, Strategic Recommendation Agent.
- **Data access:** caller-supplied.
- **Knowledge access:** optional RAG (RPM-aligned options) via S9.
- **Type:** Deterministic scoring + AI-assisted suggestion of alternatives.
- **Validation rules:** cost & impact present/normalised; quadrant thresholds defined.
- **Failure behaviour:** if impact unknown, flag "impact unassessed"; never invent savings.
- **Logging:** inputs, placement, recommendations, version, timestamp.
- **Implementation notes:** matrix thresholds configurable; AI suggestions cited + human-reviewed.

### S6 — OBB Analysis Skill ⭐
- **Purpose:** Outcome-Based Budgeting value-for-money assessment within FDS.
- **Inputs:** budget (allocation/expenditure) + outcomes (KPI achievement).
- **Outputs:** OBB value-for-money indicator + rationale.
- **Used by:** FDS Agent.
- **Data access:** caller-supplied.
- **Knowledge access:** none.
- **Type:** Deterministic (method = Technical Assumption TASM-08; finalise formula in build).
- **Validation rules:** outcomes mapped to spend; period aligned.
- **Failure behaviour:** "OBB unavailable" if outcomes missing; never assume value.
- **Logging:** inputs, indicator, method version, timestamp.
- **Implementation notes:** formula versioned; documented assumptions; testable.

### S7 — Strategic Recommendation Skill
- **Purpose:** draft interventions — alternative programmes, implementation strategies, prioritisation.
- **Inputs:** risk (S3), FDS/LCHI outputs (S4/S5), KPI context.
- **Outputs:** prioritised intervention drafts + rationale.
- **Used by:** Strategic Recommendation Agent, FDS Agent.
- **Data access:** caller-supplied.
- **Knowledge access:** RAG (RPM-aligned options) via S9/S10.
- **Type:** AI-assisted (drafting) + deterministic prioritisation.
- **Validation rules:** each recommendation traces to a risk/gap; priority bounded.
- **Failure behaviour:** "no recommendation" if no grounded option; never invent programmes.
- **Logging:** inputs, recommendations, priority, sources, version, timestamp.
- **Implementation notes:** advisory only; output reviewed via HITL (rule 6).

### S8 — RPM Alignment Skill ⭐
- **Purpose:** map a KPI to RPM 2026–2035 and score alignment strength.
- **Inputs:** KPI statement/indicator; RPM corpus (via RAG).
- **Outputs:** alignment mapping + strength score (metric = TASM-07).
- **Used by:** Knowledge Alignment Agent, Executive Copilot.
- **Data access:** caller-supplied KPI.
- **Knowledge access:** RAG (RPM main reference) via S9.
- **Type:** AI-assisted (semantic) + deterministic mapping rules.
- **Validation rules:** RPM reference resolvable; score normalised 0–1.
- **Failure behaviour:** "alignment unavailable" if RPM context missing; cite sources when present.
- **Logging:** KPI, rpm_ref, score, sources, version, timestamp.
- **Implementation notes:** uses embeddings via S9; deterministic fallback (keyword) when vectors absent.

### S9 — RAG Retrieval Skill ⭐
- **Purpose:** retrieve relevant knowledge chunks for a query.
- **Inputs:** query text, scope/filters.
- **Outputs:** top-k chunks + source metadata.
- **Used by:** Chatbot, Knowledge Alignment, Executive Copilot, FDS (optional), Report (optional).
- **Data access:** none operational; reads knowledge plane via KnowledgeService.
- **Knowledge access:** Vector store (Chroma/pgvector) + **keyword-search fallback** (TR-012).
- **Type:** AI-assisted (embeddings via Provider Adapter `embedding()`) with deterministic fallback.
- **Validation rules:** query non-empty; respect source validation (admin-validated links only).
- **Failure behaviour:** source inaccessible → clear message; nothing found → empty result (caller emits fallback).
- **Logging:** query, sources returned, retrieval mode (vector/keyword), version, timestamp.
- **Implementation notes:** embedding provider independent of LLM; cache frequent queries.

### S10 — Citation & Source Grounding Skill ⭐
- **Purpose:** attach verifiable source citations to AI answers; enforce honesty.
- **Inputs:** answer draft + retrieved sources (S9).
- **Outputs:** answer with citations, or the **fixed fallback string** when ungrounded.
- **Used by:** Chatbot, Executive Copilot, Knowledge Alignment, Report.
- **Data access:** none.
- **Knowledge access:** consumes S9 outputs.
- **Type:** Deterministic.
- **Validation rules:** every cited claim has a source; if none → fixed fallback (BR-027).
- **Failure behaviour:** never present uncited content as grounded; emit fallback string.
- **Logging:** sources cited, fallback flag, version, timestamp.
- **Implementation notes:** central enforcement point for BR-025/026/027.

### S11 — Report Writing Skill
- **Purpose:** assemble monthly report content (template + narrative).
- **Inputs:** KPI status (S1), risk (S3), FDS (S4/S5), submission, period.
- **Outputs:** report draft (sections, tables, narrative).
- **Used by:** Report Generation Agent.
- **Data access:** caller-supplied.
- **Knowledge access:** optional RAG (narrative context) via S9/S10.
- **Type:** AI-assisted (narrative) + deterministic templating.
- **Validation rules:** required sections present; figures match source; mark data gaps.
- **Failure behaviour:** produce partial draft flagging gaps; never auto-issue (HITL).
- **Logging:** report id, inputs, version, timestamp.
- **Implementation notes:** output is DRAFT only; issuance via HITL + ReportService.

### S12 — Notification Writing Skill
- **Purpose:** draft reminders/alerts/escalations.
- **Inputs:** trigger type (reminder/missing-info/approval/report/escalation), recipient context.
- **Outputs:** draft notification content.
- **Used by:** Notification Agent, Report Generation (cover note).
- **Data access:** caller-supplied.
- **Knowledge access:** none.
- **Type:** AI-assisted drafting + deterministic templates.
- **Validation rules:** recipient + context valid; tone/template appropriate.
- **Failure behaviour:** fall back to template if AI drafting fails; never send (HITL gate).
- **Logging:** notification draft id, type, version, timestamp.
- **Implementation notes:** drafts only; sending handled by NotificationService after approval.

### S13 — Audit Logging Skill
- **Purpose:** write append-only audit entries.
- **Inputs:** event (entity, action, actor, before/after, reason).
- **Outputs:** persisted AuditLog entry (via AuditService).
- **Used by:** Audit Trail Agent (and all action agents through it).
- **Data access:** append-only write via AuditService.
- **Knowledge access:** none.
- **Type:** Deterministic.
- **Validation rules:** mandatory fields present; immutable (no update/delete).
- **Failure behaviour:** audit failure raises alert; originating formal action fails closed.
- **Logging:** is the logging mechanism (self-consistent).
- **Implementation notes:** central, reused everywhere; no business logic.

### S14 — Dashboard Summary Skill
- **Purpose:** Teras 1–7 roll-ups + the main-page AI summary (7 management questions).
- **Inputs:** KPI status, risk, budget, submission, alignment per Teras.
- **Outputs:** per-Teras aggregates + AI summary text answering the 7 questions.
- **Used by:** Executive Copilot (AI Summary mode), KPI Analysis Agent, DashboardService.
- **Data access:** caller-supplied.
- **Knowledge access:** optional RAG (context) via S9/S10.
- **Type:** Deterministic roll-up + AI-assisted summary text.
- **Validation rules:** all 7 Teras represented (even if partial — RUC-03); figures reconcile.
- **Failure behaviour:** show available Teras; mark missing data; summary degrades gracefully.
- **Logging:** inputs, summary, version, timestamp.
- **Implementation notes:** roll-up deterministic & cached; summary text advisory.

### S15 — RALPH LOOP Review Skill ⭐ (internal iterative QA)
- **Purpose:** an **internal review/critique loop** that re-checks an AI output **before** it reaches the
  human-review (HITL) gate — improving quality and catching rule violations.
- **Inputs:** a candidate AI output (recommendation/report/answer) + the applicable rule checklist.
- **Outputs:** review verdict (pass/revise), issues found, optionally an improved draft; **never an approval**.
- **Used by:** FDS, Strategic Recommendation, Report Generation, Executive Copilot, Chatbot (pre-HITL QA).
- **Data access:** caller-supplied (the draft + context).
- **Knowledge access:** via S9/S10 to verify grounding/citations.
- **Type:** AI-assisted critique + deterministic rule checks (grounding present? cited? advisory-only? within scope?).
- **Validation rules:** checks BR compliance (citation BR-025, fallback BR-027, advisory BR-028, amendment BR-008 where relevant); bounded iteration count (e.g. ≤2 loops) to avoid runaway.
- **Failure behaviour:** if it cannot improve/verify, flag "needs human attention"; **never auto-approves or sends**.
- **Logging:** loop iterations, issues, final verdict, version, timestamp (BR-029).
- **Implementation notes:** a cross-cutting QA wrapper around agent outputs; strictly advisory; the human
  still makes the final decision (ASM-11). Iteration cap + cost guard (token budget).

> **Supplementary utility skills (used by services, not agents — for completeness):** `excel_parsing`
> (ImportService), `link_fetch_refresh` (KnowledgeService). Listed for traceability; not part of the 15
> agent-facing skills.

---

## 2. Skill-to-Agent Matrix

```
Skill ＼ Agent        KPIAn Valid Risk FDS StratRec KnowAlign Chatbot Report Notif Audit Copilot
S1  KPI Analysis        ✓    –    –    –     –        –        –       ✓     –     –     ✓
S2  Validation          ✓    ✓    –    –     –        –        –       –     –     –     –
S3  Risk Scoring        –    –    ✓    –     ✓        –        –       –     –     –     ✓
S4  FDS (budget)        –    –    –    ✓     –        –        –       ✓     –     –     ✓
S5  Low Cost High Imp.  –    –    –    ✓     ✓        –        –       –     –     –     –
S6  OBB Analysis        –    –    –    ✓     –        –        –       –     –     –     –
S7  Strategic Recomm.   –    –    –    ✓     ✓        –        –       –     –     –     –
S8  RPM Alignment       –    –    –    –     –        ✓        –       –     –     –     ✓
S9  RAG Retrieval       –    –    –    ~     ✓        ✓        ✓       ~     –     –     ✓
S10 Citation/Grounding  –    –    –    –     ✓        ✓        ✓       ✓     –     –     ✓
S11 Report Writing      –    –    –    –     –        –        –       ✓     –     –     –
S12 Notification Writ.  –    –    –    –     –        –        –       ✓     ✓     –     –
S13 Audit Logging       (used by ALL action agents via Audit Trail Agent — cross-cutting)  ✓(all)
S14 Dashboard Summary   ✓    –    –    –     –        –        –       –     –     –     ✓
S15 RALPH LOOP Review   –    –    –    ✓     ✓        –        ✓       ✓     –     –     ✓
```
(✓ = uses; ~ = optional/contextual). **S13** is used by all action agents; **Audit Agent** uses S13.

### Coverage check
- **Every skill used by ≥1 agent:** ✅ (S1–S15 all mapped).
- **Every agent uses ≥1 skill:** ✅ — KPIAn(S1,S2,S14), Validation(S2), Risk(S3), FDS(S4,S5,S6,S7,S9,S15),
  StratRec(S3,S5,S7,S9,S10,S15), KnowAlign(S8,S9,S10), Chatbot(S9,S10,S15), Report(S1,S4,S11,S12,S10,S15),
  Notification(S12), Audit(S13), Copilot(S1,S3,S4,S8,S9,S10,S14,S15).
- **No duplicate skills:** ✅ each skill has a single distinct responsibility; shared logic is referenced, not copied.

---

## 3. Skills Dependency Diagram

```
                 ┌──────────── S13 Audit Logging (used by everything that logs) ──────────┐
                 │                                                                          │
 S2 Validation ──┤                                                                          │
 S1 KPI Analysis ┼─► S14 Dashboard Summary ─► (Copilot)                                      │
 S3 Risk Scoring ┘            ▲                                                              │
                              │                                                              │
 S4 FDS ──► S5 Low Cost High Impact ──► S7 Strategic Recommendation ──► (HITL)               │
   └──► S6 OBB ───────────────┘                ▲                                             │
                                               │                                             │
 S9 RAG Retrieval ──► S10 Citation/Grounding ──┼─► S8 RPM Alignment                          │
        ▲                                       └─► S11 Report Writing ─► S12 Notification    │
        └──────────────── knowledge plane (KnowledgeService) ──────────────────────────────┘
 S15 RALPH LOOP Review  ──(wraps)──►  S4/S5/S7, S11, S8, Chatbot, Copilot outputs (pre-HITL QA)
```
Foundational: **S13 (audit)**, **S9+S10 (retrieval+citation)**. Composite: **S5/S6/S7 build on S4**;
**S11 builds on S1/S3/S4**; **S14 builds on S1/S3/S4**; **S15 reviews the outputs of others**.

---

## 4. Suggested Implementation Order (`/skills`)

1. **S13 Audit Logging** — everything logs to it.
2. **S2 Validation** — data-quality gate.
3. **S1 KPI Analysis** — status/progress.
4. **S3 Risk Scoring** — builds on S1.
5. **S9 RAG Retrieval** + **S10 Citation/Grounding** — knowledge foundation (with keyword fallback first).
6. **S4 FDS** → **S5 Low Cost High Impact** → **S6 OBB** — financial core.
7. **S7 Strategic Recommendation** — uses S3/S5.
8. **S8 RPM Alignment** — uses S9/S10.
9. **S14 Dashboard Summary** — uses S1/S3/S4.
10. **S11 Report Writing** → **S12 Notification Writing**.
11. **S15 RALPH LOOP Review** — last; wraps mature outputs for QA.
> Each skill is independently unit-tested before the agent that uses it (TR-006).

---

## 5. Design-rule compliance & validation

| Design rule | Compliance |
|-------------|-----------|
| 1 Reusable | Skills are shared across agents (matrix §2). |
| 2 Independently testable | Deterministic cores; AI parts mockable; pure-function bias. |
| 3 Versioned | Every skill carries a version; logged on use. |
| 4 Logged when used by AI | S13 + per-skill logging fields. |
| 5 No approve/change official records | Skills output drafts/scores; only services write (via HITL/Audit). |
| 6 Support human-review workflow | Outputs are advisory drafts; S15 pre-checks; HITL approves. |
| 7 Traceable to RTM/TRD | Each skill maps to skills in TRD §19 + RTM skill column (S1→status, S4/S5/S6→FDS, S9/S10→RAG, etc.). |

**Validation result:** ✅ every skill used by ≥1 agent; ✅ every agent uses ≥1 skill; ✅ no duplicate skill
responsibilities; ✅ skills modular/reusable; ✅ no new requirements; ✅ key differentiators (S4/S5/S6/S8/S9/S15)
specified in depth.

---
*End of Skills Layer Design Blueprint v0.1 — DRAFT. No code. Frozen baselines unmodified. Awaiting approval.*
