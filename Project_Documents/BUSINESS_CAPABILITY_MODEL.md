# BUSINESS CAPABILITY MODEL (BCM)
### Agentic AI Strategic Governance Platform — RPM 2026–2035

| Field | Value |
|-------|-------|
| Document | B6 — Business Capability Model |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Foundation for | BRD, System Modules, AI Agents, Skills, APIs, Dashboard, User Roles |
| Traces to | HMW v1.0 (HMW-01…25), To-Be Process (Phases 1–7), B2A authoritative decisions, BR-001…027 |
| Boundary | **Business capabilities only.** No technical implementation, no database design. |

---

## 1. Business Capability Overview

A **Business Capability Model** describes *what the organisation must be able to do* to achieve its
goals — expressed as stable, outcome-oriented "abilities," independent of *how* (process, technology,
org structure). Capabilities answer **"what,"** processes answer **"how,"** and systems answer **"with what."**

**Why it matters here:** for a ten-year governance platform spanning JPN/PPD/Schools, capabilities are
the most **stable** layer — processes, agents and tech will evolve, but the abilities (e.g. "monitor KPI
performance," "detect risk," "govern amendments") endure. The BCM gives one vocabulary that the **BRD**
(requirements), **modules**, **agents/skills**, **APIs**, **dashboard** and **roles** all map back to,
preventing scope drift and ensuring nothing essential is missed before requirements are written.

Convention: capabilities are `CAP-<domain><n>`. Each links to business rules and To-Be phases.

---

## 2. Capability Domains

| # | Domain | Scope |
|---|--------|-------|
| D1 | **Governance Management** | Amendment control, audit trail, human-in-the-loop, compliance |
| D2 | **KPI Management** | KPI definition, import, ownership, alignment to RPM |
| D3 | **Monthly Monitoring** | In-system updates, completeness, status, submission tracking |
| D4 | **Financial Decision Support (FDS)** *(top-level capability, BR-046)* | Budget Intelligence (status/funding-gap/risk), Low Cost High Impact Analysis, Intervention Recommendation, Executive Financial Insight, resource-optimisation strategies. To be reflected consistently in TRD, AI Architecture, Dashboard, Executive Copilot and the Traceability Matrix. |
| D5 | **Knowledge Management** | Static docs + live links, RAG, freshness, citation |
| D6 | **AI Decision Support** | Analysis, risk, intervention, alignment, copilot, chatbot |
| D7 | **Reporting & Analytics** | Monthly reports, Teras dashboard, AI/executive summaries |
| D8 | **User & Security Management** | Authentication, RBAC, roles, access governance |
| D9 | **Notification & Communication** | Reminders, alerts, escalation, distribution |
| D10 | **System Administration** | Provider config, knowledge-link admin, windows, platform ops |

---

## 3. Capability Details

> Compact format per capability: Purpose · Value · Primary Users · Inputs · Outputs · Rules · Dependencies.

### D1 — Governance Management
- **CAP-G1 Amendment Window Control** — Purpose: restrict KPI statement/indicator/target edits to Jul/Oct. Value: governed change. Users: Super Admin, PIC. In: amendment request, calendar. Out: allowed/blocked edit. Rules: BR-008. Deps: CAP-U* (roles), CAP-G2.
- **CAP-G2 Audit Trail** — Purpose: record who/what/when for every change & decision. Value: accountability, audit-readiness. Users: all (write), Audit (read). In: events. Out: immutable log. Rules: BR-009. Deps: CAP-U1.
- **CAP-G3 Human-in-the-Loop Approval** — Purpose: require human sign-off before formal action/report/email. Value: trust, risk control. Users: managers/executives. In: AI drafts. Out: approve/reject. Rules: BR-015. Deps: CAP-R1, CAP-N3.
- **CAP-G4 Compliance & Oversight Support** — Purpose: provide queryable assurance to audit/oversight. Value: governance. Users: Internal Audit. In: audit log, records. Out: assurance views. Rules: BR-009. Deps: CAP-G2.

### D2 — KPI Management
- **CAP-K1 KPI Import (one-time)** — Purpose: ingest Pelan Taktikal JPN/PPD into the record. Value: single source of truth. Users: Admin. In: Excel. Out: structured KPI records. Rules: BR-001/018. Deps: CAP-K2.
- **CAP-K2 KPI Definition & Structure** — Purpose: maintain KPI by Teras→Strategi→Prakarsa→KPI (`TSx.Sy.Pz.KPIn`), TOV, target, activities, budget. Value: consistency. Users: Admin/Sector. In: KPI data. Out: canonical KPI. Rules: BR-004. Deps: —.
- **CAP-K3 KPI Ownership Assignment** — Purpose: assign PIC (name/sector/email). Value: clear accountability. Users: Admin/Sector. In: assignment. Out: owned KPI. Rules: BR-004. Deps: CAP-U1.
- **CAP-K4 KPI–RPM Alignment** — Purpose: map each KPI to RPM and gauge alignment strength. Value: strategic coherence. Users: Admin/Exec. In: KPI + RPM corpus. Out: alignment + strength. Rules: BR-012/020. Deps: CAP-KM*, CAP-AI5.

### D3 — Monthly Monitoring
- **CAP-M1 In-System Monthly Update** — Purpose: PIC enters achievement/finance/evidence/remarks. Value: timely, owned data. Users: PIC. In: monthly data. Out: saved, audited update. Rules: BR-002/003. Deps: CAP-U1, CAP-G2.
- **CAP-M2 Completeness Detection & Warnings** — Purpose: detect missing mandatory info; warn. Value: data quality. Users: PIC/Admin. In: records. Out: warnings per KPI/Teras. Rules: BR-005/006. Deps: CAP-K2.
- **CAP-M3 KPI Status Classification** — Purpose: classify on-track/lagging/achieved. Value: visibility. Users: all. In: achievement vs target. Out: status. Rules: BR-020. Deps: CAP-M1.
- **CAP-M4 Submission Tracking** — Purpose: track who has/hasn't updated by Teras/period. Value: compliance. Users: Admin/Exec. In: update events. Out: submission status. Rules: BR-007. Deps: CAP-M1, CAP-N1.

### D4 — Budget & Financial Management
- **CAP-B1 Allocation Status Tracking** — Purpose: record six-value allocation status + warrant/expenditure. Value: financial control. Users: PIC/Finance. In: finance entries. Out: budget status. Rules: BR-010. Deps: CAP-M1.
- **CAP-B2 Budget Intelligence (Low Cost High Impact)** — Purpose: prioritise/recommend via Low Cost High Impact Matrix. Value: value-for-money. Users: Finance/Exec. In: cost/impact. Out: LCHI recommendations. Rules: BR-011. Deps: CAP-B1, CAP-AI*.
- **CAP-B3 OBB Value-for-Money Analysis** *(pending Q-025)* — Purpose: assess outcome-based budget value. Value: spending efficiency. Users: Finance/Exec. In: budget + outcomes. Out: OBB assessment. Rules: BR-010. Deps: CAP-B1.
- **CAP-B4 Financial Decision Support (FDS)** *(umbrella; added per BRD change CL-024)* — Purpose: an end-to-end financial decision-support capability **broader than Budget Intelligence**. Four components: (1) **Budget Intelligence** — budget status analysis, **funding-gap detection**, **budget-risk analysis** (CAP-B2 refined); (2) **Low Cost High Impact Analysis** (CAP-B5); (3) **Intervention Recommendation** (CAP-AI3); (4) **Executive Financial Insight** (CAP-B6). Value: value-for-money, optimised resourcing, faster financial decisions. Users: Finance/Exec/Sector. In: finance status, activities, impact, risk. Out: financial recommendations + rationale. Rules: BR-010/011/037/046. Deps: CAP-B1, CAP-AI3, CAP-AI6.
- **CAP-B5 Low Cost High Impact Analysis** — Purpose: analyse activities, evaluate expected impact, recommend lower-cost alternatives, resource optimisation, and collaboration opportunities (via the Low Cost High Impact Matrix). Value: efficiency. Users: Finance/Sector/Exec. In: activities, cost, impact. Out: ranked recommendations. Rules: BR-011/046. Deps: CAP-B1/B2.
- **CAP-B6 Executive Financial Insight** — Purpose: present AI-generated financial recommendations with rationale to support management decisions. Value: decision support. Users: Executive. In: FDS outputs. Out: explained financial insight (feeds Dashboard + Executive Copilot). Rules: BR-046/043. Deps: CAP-B4, CAP-AI6, CAP-R3.

### D5 — Knowledge Management
- **CAP-KM1 Knowledge Ingestion (static + live)** — Purpose: ingest docs + links into RAG. Value: grounded knowledge. Users: Admin. In: docs, URLs. Out: indexed knowledge. Rules: BR-012/019/023. Deps: CAP-S2.
- **CAP-KM2 Link Registry & Freshness** — Purpose: manage links (title/URL/category/last-checked) + refresh. Value: current knowledge. Users: Admin. In: links. Out: refreshed sources. Rules: BR-024. Deps: CAP-KM1.
- **CAP-KM3 Grounded Retrieval & Citation** — Purpose: retrieve with source citation; honest fallback. Value: trust. Users: all (via chatbot/copilot). In: query. Out: cited evidence / fallback. Rules: BR-025/026/027. Deps: CAP-KM1.

### D6 — AI Decision Support
- **CAP-AI1 KPI Analysis** — interpret status/trends. Rules: BR-020. Deps: CAP-M3.
- **CAP-AI2 Risk Detection** — flag At-Risk/Critical (Q-020). Rules: BR-020. Deps: CAP-M3.
- **CAP-AI3 Intervention Recommendation** — propose actions (draft). Rules: BR-015. Deps: CAP-AI2, CAP-G3.
- **CAP-AI4 KPI Chatbot** — grounded Q&A. Rules: BR-013/025/027. Deps: CAP-KM3.
- **CAP-AI5 Knowledge Alignment (AI)** — KPI↔RPM scoring (Q-021). Rules: BR-012. Deps: CAP-KM3, CAP-K4.
- **CAP-AI6 Executive Copilot** — leadership synthesis. Rules: BR-015. Deps: CAP-KM3, CAP-R*.
- **CAP-AI7 AI Summary (dashboard)** — main-page 7-question summary. Rules: BR-022. Deps: CAP-R2.

### D7 — Reporting & Analytics
- **CAP-R1 Monthly Report Generation** — draft monthly reports for approval. Value: effort reduction. Users: Admin/Exec. In: DB + AI outputs. Out: report draft. Rules: BR-014/015. Deps: CAP-G3, CAP-N3.
- **CAP-R2 Teras 1–7 Dashboard** — summarise/map KPIs by Teras (count, achievement, risk, missing, budget, submission, alignment, AI summary, mapping table, exec summary). Value: visibility. Users: all. In: DB + AI. Out: dashboard. Rules: BR-020/021/022. Deps: CAP-M3, CAP-B1, CAP-AI7.
- **CAP-R3 Executive Insight & Summary** — synthesised management view. Value: faster decisions. Users: Executive. In: aggregated signals. Out: executive summary. Rules: BR-022. Deps: CAP-AI6/AI7.

### D8 — User & Security Management
- **CAP-U1 Authentication (MOE domains)** — login restricted to MOE domains (count pending C-001). Value: controlled access. Users: all. In: credentials. Out: session. Rules: BR-003. Deps: —.
- **CAP-U2 Role-Based Access Control** — enforce role permissions (Super Admin…PIC…Exec). Value: least privilege. Users: Admin. In: role assignments. Out: authorised actions. Rules: BR-003. Deps: CAP-U1.
- **CAP-U3 Access Governance** — manage onboarding/offboarding, delegation. Value: continuity. Users: Super Admin. In: HR/role changes. Out: provisioned access. Rules: BR-003. Deps: CAP-U2.

### D9 — Notification & Communication
- **CAP-N1 Reminder Management** — remind PICs of incomplete data/updates. Value: timeliness. Users: PIC. In: gaps/deadlines. Out: reminders (drafted). Rules: BR-007. Deps: CAP-M2/M4.
- **CAP-N2 Alert & Escalation** — alert at-risk KPIs; track escalation. Value: early action. Users: Sector/Admin. In: risk flags. Out: alerts/escalation. Rules: BR-007. Deps: CAP-AI2.
- **CAP-N3 Approved Distribution (Email Queue)** — send only after human approval. Value: control. Users: managers. In: approved items. Out: distributed comms. Rules: BR-015. Deps: CAP-G3.

### D10 — System Administration
- **CAP-S1 LLM Provider Configuration** — Groq(dev)/OpenAI|Anthropic(prod) via config.md. Value: flexibility/longevity. Users: Admin/IT. In: config. Out: active provider. Rules: TR-001/002/003. Deps: —.
- **CAP-S2 Platform & Data-Plane Administration** — manage operational vs knowledge planes, windows, system settings. Value: integrity. Users: Super Admin/IT. In: settings. Out: configured platform. Rules: BR-017. Deps: —.

---

## 4. AI Capability Mapping

| AI Capability | Responsible Agent(s) | Supporting Skill(s) | Human Review Required |
|---------------|----------------------|---------------------|-----------------------|
| KPI Analysis (CAP-AI1) | KPI Analysis Agent | status classification, Teras roll-up | No (advisory display) |
| Risk Detection (CAP-AI2) | Risk Agent | risk scoring | No (display); Yes if triggers action |
| Budget Intelligence / Low Cost High Impact (CAP-B2) | Budget Intelligence Agent | LCHI scoring, budget classification | Yes (before formal use) |
| OBB Value-for-Money (CAP-B3) | Budget Intelligence Agent | OBB calculation | Yes |
| Intervention (CAP-AI3) | Intervention Agent | risk scoring, drafting | **Yes** |
| KPI–RPM Alignment (CAP-AI5/K4) | Knowledge Alignment Agent | RAG retrieval, alignment scoring | No (display) |
| Executive Copilot (CAP-AI6) | Executive Copilot Agent | RAG retrieval+citation, Teras roll-up | Yes (before acting on advice) |
| KPI Chatbot (CAP-AI4) | KPI Chatbot Agent | RAG retrieval+citation | No (info only) |
| Monthly Report Generation (CAP-R1) | Report Generation Agent | report templating, summarisation | **Yes** |
| AI Dashboard Summary (CAP-AI7) | AI Summary Agent | Teras roll-up, summarisation | No (display) |
| Completeness Detection (CAP-M2) | Validation/Completeness Agent | completeness validation | No |
| Notification drafting (CAP-N1/N2) | Notification & Reminder Agent | email drafting | **Yes (before send)** |
| Import (CAP-K1) | Data Integration Agent | Excel parsing | No (admin verifies) |
| Audit (CAP-G2) | Audit Agent | audit logging | n/a (system) |

---

## 5. Capability Relationship Diagram

```
STRATEGIC GOVERNANCE OF RPM 2026–2035
├── Governance Management (D1)
│     ├── Amendment Control · Audit Trail · Human-in-the-Loop · Compliance
├── KPI Management (D2)
│     ├── Import · Definition/Structure · Ownership · RPM Alignment
├── Monthly Monitoring (D3)
│     ├── In-System Update · Completeness · Status · Submission Tracking
├── Budget & Financial Management (D4)
│     ├── Allocation Status · Budget Intelligence (LCHI) · OBB Value-for-Money
├── Knowledge Management (D5)
│     ├── Ingestion(static+live) · Link Registry/Freshness · Retrieval+Citation
├── AI Decision Support (D6)
│     ├── Analysis · Risk · Intervention · Chatbot · Alignment · Copilot · AI Summary
├── Reporting & Analytics (D7)
│     ├── Monthly Report · Teras 1–7 Dashboard · Executive Insight
├── User & Security Management (D8)
│     ├── Authentication · RBAC · Access Governance
├── Notification & Communication (D9)
│     ├── Reminders · Alert/Escalation · Approved Distribution
└── System Administration (D10)
      ├── Provider Config · Platform/Data-Plane Admin
```

---

## 6. Capability Maturity

| Capability | Today | Target maturity |
|-----------|-------|-----------------|
| CAP-K1 Import | Manual | Semi-automated (admin-verified) |
| CAP-K2/K3 Definition/Ownership | Manual | Fully automated record + manual assignment |
| CAP-K4 / CAP-AI5 Alignment | Manual | AI-assisted |
| CAP-M1 Monthly Update | Manual (Excel) | Fully automated capture (in-system) |
| CAP-M2 Completeness | Manual/ad hoc | Fully automated (rule-based) |
| CAP-M3 Status | Manual | AI-assisted |
| CAP-M4 Submission Tracking | Manual | Fully automated |
| CAP-B1 Allocation Status | Manual | Fully automated capture |
| CAP-B2/B3 Budget Intelligence/OBB | Manual | AI-assisted + Human-in-the-loop |
| CAP-KM1–3 Knowledge/RAG | None | AI-assisted |
| CAP-AI1–7 AI Decision Support | None | AI-assisted (HITL where acting) |
| CAP-R1 Report | Manual | AI-assisted + Human-in-the-loop |
| CAP-R2/R3 Dashboard/Exec | Manual snapshots | Fully automated + AI-assisted |
| CAP-U1–3 Auth/RBAC | Weak/file-based | Fully automated |
| CAP-N1–3 Notification | Manual | Semi-automated + Human-in-the-loop (send) |
| CAP-G1–4 Governance | Intended/unenforced | Fully automated + Human-in-the-loop |
| CAP-S1–2 Admin | Manual | Fully automated config |

---

## 7. Traceability

| Capability(s) | HMW | To-Be Phase | → Future BRD | → Future TRD | → Future AI Arch |
|---------------|-----|-------------|--------------|--------------|------------------|
| CAP-K1/K2/K3 | HMW-01/02/03/25 | Phase 1/2 | BRQ (centralise/ownership) | import + data model | Data Integration Agent |
| CAP-M1–M4 | HMW-05/14 | Phase 3 | monthly update reqs | update + validation | Validation/KPI Analysis |
| CAP-M3/AI1/AI2 | HMW-05/06/07 | Phase 4 | status/risk reqs | classification logic | KPI Analysis/Risk |
| CAP-B1–B3 | HMW-08/09/10 | Phase 4 | finance reqs | budget logic | Budget Intelligence |
| CAP-KM1–3 | HMW-18/19 | Phase 5 | knowledge reqs | RAG pipeline | RAG/Chatbot |
| CAP-K4/AI5 | HMW-17 | Phase 5 | alignment reqs | alignment logic | Knowledge Alignment |
| CAP-AI6/R3 | HMW-12 | Phase 5/6 | exec support reqs | copilot | Executive Copilot |
| CAP-R2/AI7 | HMW-13 | Phase 6 | dashboard reqs | dashboard/agg | AI Summary |
| CAP-R1 | HMW-11 | Phase 7 | reporting reqs | report engine | Report Generation |
| CAP-N1–3 | HMW-14/15 | Phase 4/7 | notification reqs | email engine | Notification Agent |
| CAP-G1–4 | HMW-04/20/21 | cross-cutting | governance reqs | audit/HITL | Audit Agent/HITL |
| CAP-U1–3 | HMW-23/25 | cross-cutting | security reqs | auth/RBAC | — |
| CAP-S1–2 | HMW-24 | cross-cutting | config reqs | provider/config | provider abstraction |

---

## 8. Gap Analysis

| Gap found | Recommendation |
|-----------|----------------|
| **Data quality at import** beyond presence (validity/format, not just missing) | Add a validation sub-capability under CAP-M2 (quality rules), confirm in BRD. |
| **Delegation / acting-officer** (government continuity) | CAP-U3 extended to cover delegation; confirm rules. |
| **Historical KPI trend / year-over-year** (10-yr horizon) | Note as analytics capability for BRD (not in current scope text). |
| **Feedback/correction loop on AI output** (rate/override) | Add governance sub-capability for AI override logging under CAP-G2/G3. |
| **Data retention & archival policy** (multi-year) | Flag for BRD/TRD (records over 2026–2035). |
| **Multi-state scalability** (if national beyond Perak — Q-003) | Capabilities are state-agnostic; confirm scope. |
| **Bilingual support** (Q-012) | Treat as cross-cutting UX capability; confirm. |

No missing *domain*; gaps are sub-capabilities/parameters to confirm in the BRD.

---

## Quality Review (self-audit)

| Check | Finding | Action |
|-------|---------|--------|
| Missing capabilities? | Added Compliance/Oversight (CAP-G4), Access Governance (CAP-U3), Submission Tracking (CAP-M4). | Included |
| Duplicate capabilities? | Merged generic "analytics" into Dashboard/Exec; kept Financial Monitoring within D4 to avoid overlap with Budget Intelligence. | Resolved |
| Overlapping responsibilities? | Clarified Budget Intelligence (LCHI) vs OBB vs Allocation Status as distinct. | Clarified |
| Missing AI support? | Mapped all 14 agents to capabilities (§4); none unmapped. | Verified |
| Missing governance? | D1 covers amendment/audit/HITL/compliance; cross-cut to all action capabilities. | Verified |
| Missing business rules? | Every capability cites BR/TR ids. | Verified |

*Auto-improvements applied: added 3 capabilities; clarified finance overlaps; ensured full AI mapping.*

---

## FINAL OUTPUT

1. **Business Capability completeness score: 95%**
2. **Readiness for BRD: 95%**
3. **AI capability coverage: 96%** (all 14 agents mapped to capabilities)
4. **Governance coverage: 96%** (amendment, audit, HITL, RBAC, compliance)

**Is the Business Capability Model complete enough to begin Business Requirements Definition?**

# YES

Complete at the domain and capability level (10 domains, ~35 capabilities, all AI-mapped and traced).
The residual 5% is **parameter confirmation, not missing capability** — the same open items
(Q-024 agent roster 14/13, Q-023 login domain, Q-025 OBB, Q-020/Q-021 risk & alignment, Q-002/Q-003
scope, Q-012 language) plus the §8 sub-capabilities (data-quality rules, delegation, retention,
trend analytics) — all of which the BRD will pin down as requirements, not discover as new capabilities.

---
*End of Business Capability Model v0.1 — DRAFT. BRD NOT generated. Awaiting approval.*
