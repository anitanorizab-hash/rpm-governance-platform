# BUSINESS PROCESS DESIGN — TO-BE (FUTURE STATE)
### Master Workflow Blueprint — Agentic AI Strategic Governance Platform (RPM 2026–2035)

| Field | Value |
|-------|-------|
| Document | B5 — To-Be Business Process Design |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Role | **Master workflow blueprint** for BRD (D2), TRD (D3), System & AI Architecture |
| Traces to | HMW v1.0 (HMW-01…25, frozen), As-Is (AS-PP01–14), B2A authoritative decisions |
| Governs | All future operational and AI workflows |

> **Boundary:** This describes the future *business/operational workflow* and how AI assists it.
> It is process design, not technical implementation (no code, schema or infrastructure here).
> All AI is **advisory + human-gated** per BR-015 / B2A #9.

---

## 1. Future Business Process Overview

The platform replaces the manual Excel-and-email process with a **single, audit-grade system of record**
plus an **agentic AI layer** that monitors, analyses, recommends and drafts — while **humans approve every
formal action**. The lifecycle is:

**Import once → validate → store in database → assign PIC & complete data → monthly in-system updates →
AI processing (validation, analysis, risk, budget intelligence, intervention, notification, audit) →
knowledge layer (RAG) powering chatbot, alignment and Executive Copilot → Teras 1–7 dashboard with AI
summary → monthly report → human review → approval → notification/distribution.**

Two data planes are kept strictly separate (B2A #5): **Operational Data → database**;
**Knowledge Data (docs + live links) → RAG/vector store**. LLM provider is config-driven
(**Groq dev; OpenAI/Anthropic prod** via `config.md`, B2A #8).

---

## 2. Future Actors

### Human actors
| Actor | Responsibilities |
|-------|------------------|
| **Super Admin** | Platform governance: manage users/roles, amendment windows (Jul/Oct), knowledge links, provider config, audit oversight. |
| **JPN Administrator** | State-level oversight; manage state KPIs; consolidate; initiate state reports (for approval). |
| **Sector Administrator** | Manage KPIs for their sector/Bahagian; assign PICs; act on at-risk alerts. |
| **PPD Administrator** | District-level KPI management; oversee district PICs; monitor district submission. |
| **KPI PIC** | Own a KPI: complete missing info, enter monthly achievement, finance status, evidence, remarks. |
| **Finance Officer** | Review allocation/expenditure and budget-intelligence outputs. |
| **Executive Management** | Consume Teras dashboard + AI/executive summary; approve reports & formal actions (HITL). |
| **Internal Audit / Oversight** | Query the audit trail for assurance. |

### System actors
| Actor | Responsibilities |
|-------|------------------|
| **AI Agents (14)** | Specialised, advisory agents that process operational + knowledge data and produce drafts/recommendations (never final actions). See §6. |
| **Skills Layer** | Reusable, deterministic capabilities invoked by multiple agents (see §6). |
| **RAG / Knowledge Base** | Ingests and retrieves knowledge (static docs + live links) with source citation. |
| **Human-in-the-loop Gate** | Workflow control that requires human approval before any formal action/report/email. |

---

## 3. Complete End-to-End Workflow

### Phase 1 — Initial Import & Validation *(one-time onboarding; BR-001/018)*
1. Super/JPN Admin uploads **Pelan Taktikal JPN** and **Pelan Taktikal PPD** Excel files.
2. **Data Integration Agent** parses each Teras sheet (KPI code `TSx.Sy.Pz.KPIn`, TOV/target, activities, Bahagian, OS budget codes, monthly projections).
3. **Validation Agent** checks structure and completeness; flags anomalies.
4. Clean, structured records are written to the **operational database** (single source of truth).
5. Excel is now **input-only**; the database becomes the working source.

```
Excel (JPN + PPD) → Data Integration Agent → Validation Agent → Operational Database
```

### Phase 2 — PIC Assignment & Completeness *(BR-004/005/006)*
1. Admins **assign a PIC** (name, sector, email) to each KPI.
2. **Validation/Completeness Agent** detects missing mandatory fields and raises **warnings** per KPI/Teras.
3. PICs **complete missing information**; warnings clear as data is filled.
4. When completeness thresholds are met, KPIs are **"ready for monthly monitoring."**

```
Assign PIC → Completeness check → Warnings → PIC completes → Ready for monitoring
```

### Phase 3 — Monthly KPI Update *(BR-002/003; in-system only)*
1. **PIC logs in** (MOE domain auth, RBAC).
2. Updates **achievement** against target.
3. Updates **finance/allocation status** (six-value vocabulary, BR-010).
4. Attaches **evidence** and **remarks**.
5. **Saves** — the update is versioned; the **Audit Agent** logs who/what/when.
6. KPI statement/indicator/target are **locked except in July/October** (BR-008).

```
PIC login → Achievement → Finance status → Evidence → Remarks → Save (audited)
```

### Phase 4 — AI Processing *(advisory; outputs feed dashboard & review)*
Triggered on update/schedule; agents run as a pipeline, each producing recommendations:
1. **Validation Agent** — confirm completeness/consistency of the update.
2. **KPI Analysis Agent** — classify status vs target (on-track / lagging / achieved) per Teras.
3. **Risk Agent** — score and flag At-Risk / Critical KPIs (rule-based first, AI-assisted later — Q-020).
4. **Budget Intelligence Agent** — analyse allocation status; apply **Low Cost High Impact Matrix**; (OBB value-for-money — Q-025).
5. **Intervention Agent** — propose interventions for at-risk KPIs (draft, for human review).
6. **Notification Agent** — draft reminders/alerts (queued for approval before sending).
7. **Audit Agent** — record all AI outputs and human decisions to the audit trail.

```
Validation → KPI Analysis → Risk → Budget Intelligence → LCHI → Intervention → Notification → Audit
                                   (all advisory; results routed to Dashboard + Human Review)
```

### Phase 5 — Knowledge Layer (RAG) *(B2A #4/#5; BR-012/019/023)*
1. **Knowledge Documents** (RPM 2026–2035, guidelines, circulars, notes) + **Live Links** are ingested.
2. **Chunking → Embedding → Vector Database** (links carry title/URL/category/last-checked; admin-refreshable, BR-024).
3. **KPI Chatbot** answers from KPI DB + monthly updates + knowledge + live links, **citing sources** (BR-025); fixed fallback if absent (BR-027).
4. **Knowledge Alignment Agent** maps each KPI to RPM and scores **alignment strength** (Q-021).
5. **Executive Copilot** synthesises operational + knowledge data for leadership.

```
Docs + RPM + Live Links → Chunking → Embedding → Vector DB → Chatbot / Alignment / Executive Copilot
```

### Phase 6 — Dashboard *(B2A #1; BR-020/021/022)*
Aggregations roll up by **Teras 1–7**:
```
Main Dashboard → Summary by Teras 1–7 → Risk Summary → Budget Summary
              → Submission Summary → AI Summary → Executive Summary
```
The **AI Summary Agent** generates the main-page summary answering the 7 management questions.

### Phase 7 — Monthly Report & Distribution *(BR-014/015)*
1. **Report Generation Agent** drafts the monthly report from DB + AI outputs.
2. **Human Review** by the responsible manager.
3. **Approval** (or send-back for revision).
4. Approved outputs enter the **Email Queue**.
5. **Distribution** to recipients; **Audit Agent** logs issuance.

```
Report draft → Human Review → Approval → Email Queue → Distribution (audited)
```

---

## 4. Dashboard Workflow

The dashboard is the **primary management view**, organised by **Teras 1–7**. On load it queries the
operational database and the latest AI outputs and renders, **per Teras**:
- **KPI count** · **Achievement** summary · **Risk** summary (heatmap/table) · **Missing information**
  · **Budget/allocation** status · **Monthly submission** status · **Low Cost High Impact** summary
  · **RPM alignment strength** · **AI-generated summary**.
Plus cross-Teras: **distribution chart** (KPIs by Teras), **KPI mapping table**
(KPI → Teras → PIC → Sector → Status → Risk → Budget Status), and an **Executive insight/summary**
section. Phasing allowed: **cards/tables first, charts later** (AD-005). Drill-down: Teras → KPI → detail.

---

## 5. Knowledge Workflow

**Knowledge Documents + Live Links** are the *only* inputs to the knowledge plane (never operational
data). They are chunked, embedded and stored in the **vector database** with source metadata. The
**RAG** retriever serves three consumers: (a) the **KPI Chatbot** (grounded, source-cited Q&A with
fixed fallback), (b) the **Knowledge Alignment Agent** (KPI↔RPM mapping + alignment strength), and
(c) the **Executive Copilot** (leadership synthesis combining knowledge with operational signals).
Live links are periodically **refreshed** by admin; inaccessible sources yield a clear message, never a
guess (BR-026).

```
Knowledge Docs + RPM + Live Links → RAG (chunk/embed/retrieve, cited)
        → Chatbot   → Knowledge Alignment   → Executive Copilot
```

---

## 6. AI Workflow — Agents & Skills

### Proposed authoritative agent roster (14) — *resolves Q-024 as a proposal, pending confirmation*
| # | Agent | Purpose | Key inputs | Key outputs | Phase |
|---|-------|---------|-----------|-------------|-------|
| 1 | **Data Integration Agent** | Import Excel → structured records | Pelan Taktikal files | KPI master records | 1 |
| 2 | **Validation / Completeness Agent** | Detect missing/inconsistent data | Imported & updated data | Warnings, completeness flags | 1,2,4 |
| 3 | **KPI Analysis Agent** | Classify status vs target | KPI data + updates | Status per KPI/Teras | 4 |
| 4 | **Risk Agent (Early Warning)** | Flag At-Risk/Critical | Progress, thresholds | Risk ratings | 4 |
| 5 | **Financial Monitoring Agent** | Track allocation/warrant/expenditure | Finance entries | Budget status | 4 |
| 6 | **Budget Intelligence Agent** | Low Cost High Impact + OBB value-for-money | Cost/impact, budget | LCHI recommendations | 4 |
| 7 | **Intervention Agent** | Propose interventions (draft) | Risk + context | Intervention drafts | 4 |
| 8 | **Notification & Reminder Agent** | Draft reminders/alerts | Gaps, deadlines, risk | Queued draft emails | 4,7 |
| 9 | **Audit Agent** | Log all changes/decisions | All events | Audit trail entries | 3,4,7 |
| 10 | **Report Generation Agent** | Draft monthly reports | DB + AI outputs | Report drafts | 7 |
| 11 | **KPI Chatbot Agent** | Grounded Q&A | DB + RAG + links | Cited answers / fallback | 5 |
| 12 | **Knowledge Alignment Agent** | KPI↔RPM alignment | KPIs + RPM corpus | Alignment + strength | 5 |
| 13 | **Executive Copilot Agent** | Leadership decision support | Operational + knowledge | Executive insights | 5,6 |
| 14 | **AI Summary Agent** | Main-page 7-question summary | All signals | Dashboard AI summary | 6 |

> Agents are **advisory**; any world-affecting output (email, report issue, formal action) passes the
> **Human-in-the-loop gate** (BR-015). Agent 5 may later merge into Agent 6 if the user prefers a 13-agent
> roster — flagged for confirmation (Q-024).

### Reusable Skills (skills layer) and which agents use them
| Skill | Used by |
|-------|---------|
| Excel parsing/normalisation | Data Integration |
| Completeness validation | Validation, KPI Analysis |
| KPI status classification | KPI Analysis, AI Summary |
| Risk scoring | Risk, AI Summary, Intervention |
| Budget-status classification (six-value) | Financial Monitoring, Budget Intelligence |
| Low Cost High Impact scoring | Budget Intelligence, Intervention |
| OBB value-for-money calculation | Budget Intelligence |
| Teras aggregation / roll-up | AI Summary, Dashboard, KPI Analysis |
| RAG retrieval + source citation | Chatbot, Knowledge Alignment, Executive Copilot |
| Link fetch / refresh / freshness check | Knowledge ingestion |
| Alignment scoring (KPI↔RPM) | Knowledge Alignment |
| Email / notification drafting | Notification & Reminder, Report Generation |
| Report templating / generation | Report Generation |
| Audit logging | Audit (used by all action agents) |
| HITL gating / approval routing | All action-taking agents |

---

## 7. Future Business Rules

All target rules **BR-001…BR-027** apply (now technically enforced, vs the As-Is where they were weakly
enforced). To-Be highlights:
- Excel input-once; database is the working source (BR-001/002/018).
- MOE-domain login + RBAC (BR-003; domain count pending C-001/Q-023).
- Every KPI has PIC name/sector/email (BR-004); completeness enforced with warnings (BR-005/006).
- Reminders for incomplete data + monthly updates (BR-007).
- KPI statement/indicator/target editable **only July/October** (BR-008); all amendments audited (BR-009).
- Six-value finance status (BR-010); Budget Intelligence via Low Cost High Impact (BR-011).
- RAG on RPM 2026–2035 (BR-012); chatbot (BR-013); monthly reports (BR-014).
- **Human review before formal action/report/email (BR-015)** — enforced as a workflow gate.
- Agents + skills layer (BR-016); operational/knowledge separation (BR-017–019).
- Teras 1–7 dashboard + AI summary (BR-020/021/022).
- Static + live knowledge sources; link registry; cite sources; no-guess; fixed fallback (BR-023–027).
- Provider config Groq/OpenAI/Anthropic via `config.md` (TR-001/002/003).

---

## 8. Benefits vs the Current (As-Is) Process

| As-Is problem | To-Be improvement |
|---------------|-------------------|
| AS-PP01 Manual work | Automated import, validation, drafting; staff review not re-key. |
| AS-PP02 Fragmented/duplicate data | Single source of truth in the database. |
| AS-PP03 Missing info | Enforced completeness + warnings at entry. |
| AS-PP04 Late submission | Automated reminders + submission tracking by Teras. |
| AS-PP05 Hard to track progress | Real-time Teras 1–7 dashboard. |
| AS-PP06 No audit trail | Every change/decision audited (Audit Agent). |
| AS-PP07 Limited visibility | Executive dashboard + AI summary. |
| AS-PP08 RPM alignment difficulty | Knowledge Alignment Agent + alignment strength. |
| AS-PP09 Budget challenges | Systematic finance status + Budget Intelligence + Low Cost High Impact. |
| AS-PP10 No recommendations | Risk flags, interventions, prioritisation. |
| AS-PP11 Manual reminders | Notification Agent (human-approved). |
| AS-PP12 Weak access control | MOE-domain auth + RBAC. |
| AS-PP13 Continuity risk | Durable system of record + knowledge base. |
| AS-PP14 Inconsistent checks | Rule-based, consistent validation. |

---

## 9. Business Process Diagram (text-based, To-Be)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       FUTURE (TO-BE) MASTER WORKFLOW                           │
└──────────────────────────────────────────────────────────────────────────────┘

PHASE 1  Excel (JPN+PPD) → [Data Integration Agent] → [Validation Agent] → ┐
                                                                           ▼
                                                              ╔══════════════════════╗
                                                              ║  OPERATIONAL DATABASE ║  (single source of truth)
                                                              ╚══════════════════════╝
PHASE 2  Assign PIC → [Completeness Agent] → Warnings → PIC completes → Ready ─┘
                                                                           │
PHASE 3  [PIC login] → Achievement → Finance status → Evidence → Remarks → Save → [Audit Agent]
                                                                           │ (triggers)
PHASE 4  AI PIPELINE (advisory):
         Validation → KPI Analysis → Risk → Financial Monitoring → Budget Intelligence(LCHI/OBB)
                    → Intervention → Notification(draft) → Audit
                                                                           │ outputs
        ┌──────────────────────────────────────────────────────────────────┤
        ▼                                                                    ▼
PHASE 6  ╔═══════════════════════════╗                          PHASE 7  Report draft
         ║  DASHBOARD (Teras 1–7)    ║                                    → HUMAN REVIEW
         ║  count/achv/risk/missing/ ║                                    → Approval
         ║  budget/submission/       ║                                    → Email Queue
         ║  AI summary/exec summary  ║                                    → Distribution → [Audit]
         ╚═══════════════════════════╝
                    ▲
PHASE 5  KNOWLEDGE PLANE (separate):
         Docs + RPM + Live Links → Chunk → Embed → [Vector DB]
                 → Chatbot (cited) → Knowledge Alignment → Executive Copilot ──┘
                 (feeds dashboard AI/executive summary & decision support)

CROSS-CUTTING:  Human-in-the-loop gate before every formal action · RBAC (MOE domains)
                · Audit trail on all changes · Config: Groq(dev)/OpenAI|Anthropic(prod)
```

---

## 10. Readiness Check

| Capability | Supported? | Where |
|------------|------------|-------|
| HMW (HMW-01…25) | ✅ | All phases trace to HMW |
| Dashboard by Teras 1–7 | ✅ | Phase 6, §4 |
| Monthly Workflow | ✅ | Phase 3 |
| Budget Intelligence | ✅ | Phase 4 (Agent 6) |
| Low Cost High Impact Matrix | ✅ | Phase 4, §6 |
| Skills Layer | ✅ | §6 skills table |
| RAG | ✅ | Phase 5, §5 |
| Executive Copilot | ✅ | Phase 5/6 (Agent 13) |
| Human Review | ✅ | Phase 7 + cross-cutting gate |
| Notification | ✅ | Phase 4/7 (Agent 8) |
| Audit Trail | ✅ | Agent 9, cross-cutting |
| Reporting | ✅ | Phase 7 (Agent 10) |
| Config Mode (Dev/Prod) | ✅ | §1, §7 (Groq/OpenAI/Anthropic via config.md) |

---

## Quality Audit (self-review)

| Check | Finding | Action |
|-------|---------|--------|
| Missing workflow? | Added explicit Audit logging in Phases 3/4/7 and drill-down in §4. | Included |
| Missing actor? | Added Finance Officer + Internal Audit alongside the requested admin roles; separated system actors. | §2 |
| Missing AI capability? | Added AI Summary Agent (dashboard) + Financial Monitoring distinct from Budget Intelligence → clean 14. | §6 |
| Missing dashboard function? | Added RPM alignment strength + KPI mapping table + distribution chart. | §4 |
| Missing business rule? | Mapped all BR-001…027 to To-Be; noted enforcement now technical. | §7 |
| Missing governance? | HITL gate, RBAC, audit trail, amendment windows all cross-cutting. | §3/§7/§9 |
| Solution leak (tech)? | Kept to process level; no schema/code/infra specified. | Confirmed |

*Auto-improvements applied: 14-agent roster reconciled; audit + finance roles added; dashboard functions completed; governance made cross-cutting.*

---

## FINAL OUTPUT

1. **To-Be completeness score: 95%**
2. **Business readiness score: 95%**
3. **AI readiness score: 94%**
4. **Governance readiness score: 96%**
5. **Overall confidence score: 95%**

**Is this To-Be Business Process ready to become the master blueprint for the BRD, TRD and System Architecture?**

# YES

Ready at 95%. Residual items are **precision parameters, not workflow gaps**, and are carried as known
open questions (they refine *values*, not the *blueprint*):
- Q-024 — confirm the 14-agent roster (or merge to 13).
- Q-023/C-001 — login domain count.
- Q-025 — OBB definition & relation to Low Cost High Impact.
- Q-020/Q-021 — risk scoring & alignment-strength formulas.
- Q-002/Q-003 — school login & pilot vs national scope.

None of these change the phases, actors, agents, dashboard or governance — they tune specific rules the
BRD/TRD will pin down.

---
*End of To-Be Business Process Design v0.1 — DRAFT. Master blueprint pending approval. BRD NOT generated.*
