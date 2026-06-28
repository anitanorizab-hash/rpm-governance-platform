# AI AGENT ARCHITECTURE BLUEPRINT
### Agentic AI Strategic Governance Platform — RPM 2026–2035
#### Implementation guide for the `/agents` module

| Field | Value |
|-------|-------|
| Document | A2 — AI Agent Architecture Blueprint |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Audience | Developers implementing `/agents` |
| Baselines (frozen, not modified) | HMW v1.0, BRD v1.0, RTM v1.0, TRD v1.0, System Architecture Blueprint (A1) |
| Boundary | Architecture only — **no code**; implements frozen baselines (no new requirements). |

> **Foundations.** Capability-driven (BR-041): capabilities + rules are the contract; the agent set realises
> them and may evolve. AI is **advisory**; humans approve every formal action (BR-015/028/ASM-11). Agents
> reach data **only through backend services** (never the DB directly). Skills are **reusable** and never
> duplicated inside agents (BR-042). All AI activity is **logged** (BR-029). A **custom Agent Orchestrator**
> coordinates V1 (TRD §17.5). Provider Adapter exposes `chat()`/`embedding()` (TRD §17.2).

> **Roster note (capability-driven).** This blueprint specifies **11 primary agents**. They cover the same
> capabilities as the 14-entry roster in BRD §17; folded items: **Data Integration** import is handled by
> `ImportService` + the `excel_parsing` skill (a one-time pipeline, not a runtime agent); **Financial
> Monitoring + Budget Intelligence + Low Cost High Impact + OBB** are consolidated into the **Financial
> Decision Support Agent**; **AI Summary** is produced by the **Executive Copilot Agent** (dashboard summary
> mode). This is consistent with BR-041 (count may evolve without changing the architecture).

---

## 1. Agent catalogue (overview)

| # | Agent | Capability | RTM | Human review |
|---|-------|-----------|-----|:------------:|
| 1 | KPI Analysis | CAP-AI1 | AIRQ-004/FRQ-008 | No (display) |
| 2 | Validation | CAP-M2 | FRQ-006 | No |
| 3 | Financial Decision Support | CAP-B2/B3/B5 | FRQ-014/028/029, AIRQ-006 | **Yes** |
| 4 | Risk Assessment | CAP-AI2 | FRQ-009/AIRQ-005 | No (Yes if it triggers action) |
| 5 | Strategic Recommendation | CAP-AI3 | FRQ-015 | **Yes** |
| 6 | Knowledge Alignment | CAP-AI5 | FRQ-022/AIRQ-007 | No (display) |
| 7 | KPI Chatbot | CAP-AI4 | FRQ-013/AIRQ-009 | No (info only) |
| 8 | Report Generation | CAP-R1 | FRQ-016/REPQ-001 | **Yes** |
| 9 | Notification | CAP-N1/N2 | FRQ-018/019 | **Yes (before send)** |
| 10 | Audit Trail | CAP-G2 | FRQ-024/DATQ-004 | n/a (system) |
| 11 | Executive Copilot | CAP-AI6/AI7 | FRQ-012/023/030 | Yes (before acting) |

---

## 2. Agent specifications

### Agent 1 — KPI Analysis Agent
- **Purpose:** interpret KPI performance vs target across Teras 1–7.
- **Responsibilities:** classify status (on-track/lagging/achieved); compute Teras roll-ups; trend notes.
- **Inputs:** KPI records, monthly updates, targets.
- **Outputs:** status per KPI/Teras (advisory).
- **Services Called:** KpiService, UpdateService, DashboardService (read).
- **Skills Used:** `kpi_status_classification`, `teras_aggregation`.
- **Data Access:** via services (read-only); never direct DB.
- **Knowledge Access:** none.
- **Dependencies:** Validation (clean data).
- **Human Review:** No (display only).
- **Failure Behaviour:** on error, return "status unavailable" for affected KPI; do not block dashboard.
- **Logging:** input refs, computed status, model/provider (if LLM used), timestamp → AuditService.

### Agent 2 — Validation Agent
- **Purpose:** detect incomplete/inconsistent KPI data; raise warnings.
- **Responsibilities:** check mandatory fields (PIC/sector/email/target); flag per KPI/Teras; gate "ready for monitoring".
- **Inputs:** imported records, monthly updates.
- **Outputs:** completeness flags/warnings.
- **Services Called:** ValidationService, KpiService.
- **Skills Used:** `completeness_validation`.
- **Data Access:** via services (read).
- **Knowledge Access:** none.
- **Dependencies:** runs after import and on each update.
- **Human Review:** No (warnings are informational; PIC acts).
- **Failure Behaviour:** fail safe — if validation cannot run, mark "validation pending", never auto-pass.
- **Logging:** validation run, issues found, timestamp.

### Agent 3 — Financial Decision Support (FDS) Agent
- **Purpose:** the top-level financial capability (BR-046) — budget analysis + Low Cost High Impact + OBB.
- **Responsibilities:** budget status analysis; **funding-gap detection**; **budget-risk analysis**; **Low Cost High Impact Analysis** (activities, expected impact, lower-cost alternatives, resource optimisation, collaboration); OBB value-for-money; produce recommendations + rationale.
- **Inputs:** FinanceAllocation (6-value status, OS codes, expenditure), KPI, RiskAssessment.
- **Outputs:** financial recommendations + rationale (advisory).
- **Services Called:** FinanceService, KpiService, AgentOrchestrationService.
- **Skills Used:** `budget_status_classification`, `low_cost_high_impact_scoring`, `obb_value_for_money`.
- **Data Access:** via FinanceService/KpiService (read); writes Recommendation via service.
- **Knowledge Access:** RAG (RPM/guidelines) for context via `rag_retrieval_and_citation` (optional).
- **Dependencies:** Risk Assessment (risk context); feeds Strategic Recommendation & Executive Copilot.
- **Human Review:** **Yes** — recommendations reviewed before implementation (BR-037/046).
- **Failure Behaviour:** on provider/data error, return partial analysis with a clear note; never fabricate figures.
- **Logging:** inputs, recommendation, rationale, provider/model, timestamp.

### Agent 4 — Risk Assessment Agent
- **Purpose:** flag At-Risk/Critical KPIs early.
- **Responsibilities:** score risk (rule-based initially, TASM-07); per KPI/Teras risk summary; feed early-warning.
- **Inputs:** KPI progress vs target/time, thresholds.
- **Outputs:** risk ratings (advisory).
- **Services Called:** KpiService, UpdateService.
- **Skills Used:** `risk_scoring`.
- **Data Access:** via services (read).
- **Knowledge Access:** none.
- **Dependencies:** KPI Analysis.
- **Human Review:** No for display; **Yes** if a risk triggers a formal action (routes via Strategic Recommendation/Notification).
- **Failure Behaviour:** on error, mark risk "unknown"; never silently mark low-risk.
- **Logging:** risk method, score, inputs, timestamp.

### Agent 5 — Strategic Recommendation Agent (Intervention)
- **Purpose:** recommend interventions for at-risk KPIs / funding gaps.
- **Responsibilities:** suggest **alternative programmes**, **implementation strategies**, **prioritise** recommendations.
- **Inputs:** risk ratings, FDS outputs, KPI context.
- **Outputs:** intervention drafts (advisory, prioritised).
- **Services Called:** AgentOrchestrationService, KpiService, FinanceService.
- **Skills Used:** `risk_scoring` (read), `low_cost_high_impact_scoring`, drafting.
- **Data Access:** via services; writes Recommendation via service.
- **Knowledge Access:** RAG for RPM-aligned options (cited).
- **Dependencies:** Risk Assessment, FDS Agent.
- **Human Review:** **Yes** (before any action).
- **Failure Behaviour:** if no grounded option, return "no recommendation"; never invent programmes.
- **Logging:** inputs, recommendations, priority, rationale, timestamp.

### Agent 6 — Knowledge Alignment Agent
- **Purpose:** map each KPI to RPM 2026–2035 and score alignment strength.
- **Responsibilities:** KPI↔RPM mapping; alignment-strength metric (TASM-07); surface misalignment.
- **Inputs:** KPI records; RPM corpus (RAG).
- **Outputs:** AlignmentScore (advisory, display).
- **Services Called:** KnowledgeService, KpiService.
- **Skills Used:** `alignment_scoring`, `rag_retrieval_and_citation`.
- **Data Access:** via services (read); writes AlignmentScore via service.
- **Knowledge Access:** RAG (RPM main reference).
- **Dependencies:** RAG/Knowledge layer.
- **Human Review:** No (display).
- **Failure Behaviour:** if RPM context unavailable, mark "alignment unavailable"; cite sources when present.
- **Logging:** KPI, rpm_ref, score, timestamp.

### Agent 7 — KPI Chatbot Agent
- **Purpose:** grounded, source-cited Q&A over KPI data + knowledge.
- **Responsibilities:** answer using grounding order (KPI DB → updates → docs → RPM → live links); cite sources; fixed fallback.
- **Inputs:** user question; role/scope.
- **Outputs:** cited answer or fallback string.
- **Services Called:** ChatbotService, KnowledgeService, KpiService (role-scoped reads).
- **Skills Used:** `rag_retrieval_and_citation`, `teras_aggregation` (for data questions).
- **Data Access:** via services, **role-scoped** (user sees only permitted KPI data).
- **Knowledge Access:** RAG (docs, RPM, live links).
- **Dependencies:** RAG/Knowledge layer; Auth (scope).
- **Human Review:** No (informational; cannot act).
- **Failure Behaviour:** source inaccessible → clear message; no grounding → fixed fallback (BR-026/027); never fabricate.
- **Logging:** question, sources used, answer, timestamp.

### Agent 8 — Report Generation Agent
- **Purpose:** draft monthly reports + executive summary.
- **Responsibilities:** assemble report from DB + AI outputs; template; produce DRAFT for approval.
- **Inputs:** KPI status, risk, finance/FDS, submission, period.
- **Outputs:** report draft (advisory until approved).
- **Services Called:** ReportService, DashboardService, FinanceService.
- **Skills Used:** `report_templating`, `teras_aggregation`, `email_notification_drafting` (cover note).
- **Data Access:** via services (read); writes Report (status=draft) via service.
- **Knowledge Access:** optional RAG for narrative context (cited).
- **Dependencies:** KPI Analysis, Risk, FDS, Executive Copilot (summary).
- **Human Review:** **Yes** — report approved before issue (BR-014/015/040).
- **Failure Behaviour:** on partial data, mark gaps in draft; never issue without approval.
- **Logging:** report id, inputs, generated_by, timestamp.

### Agent 9 — Notification Agent
- **Purpose:** draft reminders/alerts; manage escalation.
- **Responsibilities:** monthly update reminders, missing-info reminders, approval/report notifications, **escalation for overdue**; queue with retry.
- **Inputs:** completeness gaps, deadlines, risk flags, approvals.
- **Outputs:** draft notifications (queued; sent only after approval).
- **Services Called:** NotificationService, WorkflowService, ValidationService.
- **Skills Used:** `email_notification_drafting`.
- **Data Access:** via services (read).
- **Knowledge Access:** none.
- **Dependencies:** Validation, Risk, WorkflowService (HITL).
- **Human Review:** **Yes** — nothing sends without human approval (BR-015/040).
- **Failure Behaviour:** email failure → queue retry (backoff); surface if exhausted; never silent-drop.
- **Logging:** notification id, type, recipient, status, approver, sent_at.

### Agent 10 — Audit Trail Agent
- **Purpose:** record all consequential AI outputs and human decisions.
- **Responsibilities:** write append-only audit entries (who/what/when/before/after/reason).
- **Inputs:** events from all agents/services and HITL decisions.
- **Outputs:** AuditLog entries.
- **Services Called:** AuditService.
- **Skills Used:** `audit_logging`.
- **Data Access:** append-only writes via AuditService.
- **Knowledge Access:** none.
- **Dependencies:** all agents/services (cross-cutting).
- **Human Review:** n/a (system).
- **Failure Behaviour:** audit write failure raises an alert; the originating action should fail closed (no unaudited formal action).
- **Logging:** is the logging mechanism (self-consistent, immutable).

### Agent 11 — Executive Copilot Agent
- **Purpose:** synthesise operational + knowledge signals for leadership; also produces the dashboard AI summary.
- **Responsibilities:** combine KPI/Risk/FDS/RAG/Report/Notification outputs; produce executive insight + rationale; answer the 7 dashboard questions (AI Summary mode).
- **Inputs:** outputs of KPI Analysis, Risk, FDS, RAG, Report, Notification.
- **Outputs:** executive insight + rationale (advisory); dashboard AI summary.
- **Services Called:** CopilotService, DashboardService, KnowledgeService.
- **Skills Used:** `teras_aggregation`, `rag_retrieval_and_citation`, summarisation.
- **Data Access:** via services (read).
- **Knowledge Access:** RAG (RPM, guidelines, links) — cited.
- **Dependencies:** **orchestrates/consumes** Agents 1,3,4,6,8,9 outputs (does not replace them).
- **Human Review:** Yes before acting on advice (final approval with authorised officers, ASM-11).
- **Failure Behaviour:** degrade gracefully (summarise available signals); cite sources; fallback if none.
- **Logging:** inputs consumed, insight, sources, timestamp.

---

## 3. Orchestration diagrams

### 3.1 Agent communication (via Orchestrator + services)
```
                         ┌──────────── Agent Orchestrator (custom, V1) ───────────┐
 L2 services ──invoke──► │ context assembly · routing · logging · HITL routing    │
                         └───┬───────┬───────┬───────┬───────┬───────┬────────────┘
                             ▼       ▼       ▼       ▼       ▼       ▼
                        Validation KPIAnal. Risk    FDS  Strategic Knowledge
                             │       │       │       │     Recomm.   Align.
                             └───────┴───────┴───┬───┴───────┴────────┘
                                                 ▼
                       Audit Agent logs ALL ◄────┤  (advisory outputs)
                                                 ▼
                              Report · Notification · Executive Copilot
                                                 ▼
                                         HITL gate (WorkflowService) → action
   Rule: agents talk via Orchestrator/services; NEVER directly to DB or each other's internals.
```

### 3.2 Executive Copilot orchestration
```
[User/Exec request] → CopilotService → Executive Copilot Agent
        │ requests (read) outputs of:
        ├─ KPI Analysis (status/Teras)
        ├─ Risk Assessment (at-risk/critical)
        ├─ FDS Agent (budget, Low Cost High Impact, financial insight)
        ├─ RAG/Knowledge Alignment (RPM grounding, cited)
        ├─ Report (latest monthly outputs)
        └─ Notification (open gaps/escalations)
        ▼ synthesise → executive insight + rationale (cited)
   → advisory only → HITL before acting → AuditLog
   (Copilot ORCHESTRATES; specialist agents remain the source of truth)
```

### 3.3 Financial Decision Support workflow
```
FinanceService(budget) → FDS Agent
   budget status · funding-gap · budget-risk
        ▼
   Low Cost High Impact Analysis (activities·impact·alternatives·resource-opt·collaboration)
        ▼
   Strategic Recommendation Agent (alt programmes·strategies·prioritise)
        ▼
   Executive Copilot (Executive Financial Insight + rationale)
        ▼
   HITL approval → action/report ; AuditLog
```

### 3.4 Chatbot workflow
```
[Question] → ChatbotService → KPI Chatbot Agent
   grounding: KPI DB(role-scoped) → updates → docs → RPM → live links (RAG, cited)
        ▼ Provider Adapter chat() (+ embedding() for retrieval)
   cited answer  | inaccessible source → clear message | no grounding → fixed fallback
        ▼ log Q&A + sources (Audit)
```

### 3.5 Monthly KPI workflow (agent view)
```
PIC update → UpdateService → Validation Agent (completeness)
        ▼ saved (DB via service) → Audit Agent logs
   KPI Analysis (status) → Risk Assessment (rating) → FDS (budget context)
        ▼
   Dashboard refresh (Teras 1–7) ; if gaps → Notification Agent (draft→HITL→send)
```

### 3.6 Report generation workflow
```
[Period close/trigger] → ReportService → Report Generation Agent
   pulls: KPI Analysis · Risk · FDS · Executive Copilot summary
        ▼ assemble DRAFT (template)
   HITL review/approve (WorkflowService) → issue → distribute (Notification) → Audit
```

---

## 4. Agent Dependency Matrix

Rows depend on columns (✓ = consumes output / requires). All data access is via services.
```
                 │ Valid │ KPIAn │ Risk │ FDS │ StratRec │ KnowAlign │ Chatbot │ Report │ Notif │ Audit │ Copilot
KPI Analysis     │  ✓    │   –   │  –   │  –  │    –     │     –     │    –    │   –    │   –   │  →log │   –
Validation       │  –    │   –   │  –   │  –  │    –     │     –     │    –    │   –    │   –   │  →log │   –
FDS              │  –    │   ✓   │  ✓   │  –  │    –     │     –     │    –    │   –    │   –   │  →log │   –
Risk Assessment  │  –    │   ✓   │  –   │  –  │    –     │     –     │    –    │   –    │   –   │  →log │   –
Strategic Recomm.│  –    │   –   │  ✓   │  ✓  │    –     │     –     │    –    │   –    │   –   │  →log │   –
Knowledge Align. │  –    │   –   │  –   │  –  │    –     │     –     │    –    │   –    │   –   │  →log │   –
KPI Chatbot      │  –    │   –   │  –   │  –  │    –     │     ~     │    –    │   –    │   –   │  →log │   –
Report Gen.      │  –    │   ✓   │  ✓   │  ✓  │    –     │     –     │    –    │   –    │   –   │  →log │   ✓
Notification     │  ✓    │   –   │  ✓   │  –  │    –     │     –     │    –    │   –    │   –   │  →log │   –
Audit Trail      │  (consumes events from ALL agents/services — cross-cutting)         │   –
Executive Copilot│  –    │   ✓   │  ✓   │  ✓  │    ~     │     ✓     │    –    │   ✓    │   ✓   │  →log │   –
```
(✓ = direct dependency; ~ = optional/contextual; →log = writes to Audit). **Audit** is depended on by all;
**Copilot** orchestrates 1/3/4/6/8/9 but does not replace them.

---

## 5. Design-rule compliance

| Rule | Compliance |
|------|-----------|
| 1 Independent & modular | Each agent is self-contained, single-purpose; communicates via Orchestrator/services. |
| 2 No skill duplication | Shared logic lives in the Skills Layer; agents reference skills (§2 "Skills Used"). |
| 3 Advisory only | All outputs advisory; only Audit writes system records. |
| 4 Human approval mandatory | FDS, Strategic Recommendation, Report, Notification, Copilot route through HITL. |
| 5 No direct DB access | Agents call backend services only; services own the DB. |
| 6 All AI logged | Every agent writes to AuditService (BR-029). |
| 7 Future expansion | Capability-driven; add/replace agents via Orchestrator without redesign (BR-041). |

---

## 6. Validation

| Check | Result |
|-------|--------|
| Every agent supports ≥1 capability? | ✅ §1 maps each agent to CAP-* . |
| Every agent maps to RTM? | ✅ §1 maps to FRQ/AIRQ/REPQ/DATQ IDs. |
| No duplicate responsibilities? | ✅ FDS consolidates finance; Copilot synthesises (not duplicates); skills shared not copied. |
| Copilot orchestrates, not replaces? | ✅ §3.2 — Copilot consumes specialist outputs; specialists remain source of truth. |
| No new requirements? | ✅ Implements frozen BRD/RTM/TRD only. |

---

## 7. Suggested Implementation Order (`/agents`)

1. **Audit Trail Agent** — foundational (everything logs to it).
2. **Validation Agent** — gates data quality early.
3. **KPI Analysis Agent** — status/Teras roll-up (dashboard depends on it).
4. **Risk Assessment Agent** — builds on KPI Analysis.
5. **Financial Decision Support Agent** — budget + Low Cost High Impact + OBB.
6. **Strategic Recommendation Agent** — uses Risk + FDS.
7. **Knowledge Alignment Agent** — needs RAG/Knowledge layer ready.
8. **KPI Chatbot Agent** — needs RAG; user-facing.
9. **Report Generation Agent** — consumes Analysis/Risk/FDS.
10. **Notification Agent** — reminders/escalation + HITL send.
11. **Executive Copilot Agent** — last; orchestrates/synthesises all of the above.
> Build the Agent Orchestrator + Provider Adapter first (scaffolding), then agents in this order; test each before the next (TR-006).

---
*End of AI Agent Architecture Blueprint v0.1 — DRAFT. No code. Frozen baselines unmodified. Awaiting approval.*
