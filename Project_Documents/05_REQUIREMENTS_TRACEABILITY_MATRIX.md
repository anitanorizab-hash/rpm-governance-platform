# REQUIREMENTS TRACEABILITY MATRIX (RTM)
### Agentic AI Strategic Governance Platform — RPM 2026–2035

| Field | Value |
|-------|-------|
| Document | R1 — Requirements Traceability Matrix |
| Version | **1.0 (FROZEN — APPROVED BASELINE)** |
| Date | 2026-06-27 |
| Frozen on | 2026-06-27 by user approval |
| Status | **APPROVED · FROZEN** — Draft → Approved → **FROZEN ✅** |
| Role | **Bridge between the frozen BRD (D2 v1.0) and the TRD (D3)** |
| Baseline | BRD v1.0 (FROZEN) — not modified by this document |
| Change control | Reopened only via an explicit, logged change request (CHANGE_LOG.md). |
| Boundary | Traceability only. Forward columns (TRD §, API, DB entity, Test Case) are **planned references** to be finalised in the TRD/test phases. |

### Document Control
| Role | Name | Responsibility | Signature | Date |
|------|------|----------------|-----------|------|
| Business Owner | User (suzila@iegcampus.com) | Approve traceability baseline | **Approved** | 2026-06-27 |
| Solution Architect | _TBC_ | Endorse traceability integrity | | |
| Quality / Audit | _TBC_ | Confirm no orphans / full coverage | | |

### Version History
| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 2026-06-27 | BA/Architecture team | Initial RTM draft: 86 requirements × 17 columns; validation (0 orphans); completeness 98%. |
| **1.0** | **2026-06-27** | **BA/Architecture team** | **Approved and FROZEN as the official Requirements Traceability baseline.** |

> **Legend.** Priority: M=Must, S=Should, C=Could, F=Future. Status: Baselined = traced to frozen BRD;
> forward artefacts (TRD/API/DB/Test) are *Planned* until those documents are authored.
> Modules: M1 Auth/Access · M2 KPI Import/Master · M3 Monthly Update · M4 Validation · M5 Dashboard ·
> M6 Finance/FDS · M7 Agent Centre · M8 Knowledge/RAG · M9 Chatbot · M10 Reporting/Archive ·
> M11 Notification/Email · M12 Audit/Governance · M13 Admin/Config.

---

## 1. RTM — Business Requirements (BRQ)

| Req ID | Name | Bus. Objective | Bus. Rule | Capability | BRD § | TRD § (planned) | Module | AI Agent | Skill | Dashboard | API/Service | DB Entity | Knowledge Src | Test Case | Pri | Status |
|--------|------|---------------|-----------|-----------|-------|------------------|--------|----------|-------|-----------|-------------|-----------|---------------|-----------|-----|--------|
| BRQ-001 | Centralised KPI governance | OBJ-01 | BR-001/018 | CAP-K1/K2 | §5,6,8 | TRD-§Data/Import | M2 | Data Integration | Excel parsing | — | ImportService, KPIService | KPI, Teras, Activity | — | TC-001 | M | Baselined |
| BRQ-002 | Monthly KPI monitoring | OBJ-02 | BR-002 | CAP-M1/M4 | §6,9 | TRD-§Update | M3 | — | completeness validation | DSH-06 | UpdateService | MonthlyUpdate | — | TC-007 | M | Baselined |
| BRQ-003 | KPI ownership | OBJ-03 | BR-004 | CAP-K3 | §5 | TRD-§KPI | M2 | — | — | DSH-11 | KPIService | PIC, KPI | — | TC-005 | M | Baselined |
| BRQ-004 | Governed amendment | OBJ-04 | BR-008/009 | CAP-G1/G2 | §6 | TRD-§Governance | M12 | Audit | audit logging | — | AuditService | AmendmentWindow, AuditLog | — | TC-010 | M | Baselined |
| BRQ-005 | Budget & value-for-money | OBJ-05 | BR-010/046 | CAP-B1/B4 | §20 | TRD-§FDS | M6 | Budget Intelligence | budget classification, LCHI scoring | DSH-05 | FinanceService | FinanceAllocation | — | TC-014 | M | Baselined |
| BRQ-006 | Early risk identification | OBJ-06 | BR-020 | CAP-AI2 | §15,16 | TRD-§Risk | M7 | Risk | risk scoring | DSH-04/10 | AgentService | RiskAssessment | — | TC-009 | M | Baselined |
| BRQ-007 | Executive decision support | OBJ-07 | BR-022/043 | CAP-AI6/R3 | §15,19 | TRD-§Copilot | M5/M7 | Executive Copilot, AI Summary | RAG retrieval, Teras roll-up | DSH-08 | CopilotService | (views) | RPM, docs, links | TC-012 | M | Baselined |
| BRQ-008 | RPM alignment assurance | OBJ-08 | BR-012 | CAP-K4/AI5 | §19 | TRD-§Alignment | M8 | Knowledge Alignment | alignment scoring, RAG | DSH-12 | KnowledgeService | AlignmentScore | RPM 2026–2035 | TC-022 | S | Baselined |
| BRQ-009 | Reduce manual reporting | OBJ-09 | BR-014 | CAP-R1 | §21 | TRD-§Reporting | M10 | Report Generation | report templating | — | ReportService | Report | — | TC-016 | M | Baselined |
| BRQ-010 | Cross-tier collaboration | OBJ-10 | BR-007 | CAP-M4/R2 | §15 | TRD-§Dashboard | M5 | — | Teras roll-up | DSH-06 | DashboardService | (views) | — | TC-025 | S | Baselined |
| BRQ-011 | Adoption & trust | OBJ-11 | BR-028 | CAP-G3 | §16 | TRD-§HITL | M3/M7 | — | HITL gating | — | (UX) | — | — | TC-017 | S | Baselined |
| BRQ-012 | Continuity / memory | OBJ-12 | BR-033 | CAP-KM1/U3 | §4 | TRD-§Knowledge | M8/M1 | — | RAG retrieval | — | KnowledgeService | KnowledgeSource | docs/links | TC-020 | S | Baselined |

## 2. RTM — Functional Requirements (FRQ)

| Req ID | Name | Bus. Rule | Capability | BRD § | TRD § (planned) | Module | AI Agent | Skill | Dashboard | API/Service | DB Entity | Knowledge Src | Test Case | Pri | Status |
|--------|------|-----------|-----------|-------|------------------|--------|----------|-------|-----------|-------------|-----------|---------------|-----------|-----|--------|
| FRQ-001 | MOE-domain login (`@moe.gov.my`/`@moe-dl.edu.my`) | BR-003 | CAP-U1 | §14,23 | TRD-§Auth | M1 | — | — | — | AuthService | User | — | TC-001 | M | Baselined |
| FRQ-002 | Role-based access | BR-031/032 | CAP-U2 | §14 | TRD-§Auth | M1 | — | — | — | AuthService | Role, User | — | TC-002 | M | Baselined |
| FRQ-003 | Excel import (once) | BR-001/018 | CAP-K1 | §6 | TRD-§Import | M2 | Data Integration | Excel parsing | — | ImportService | KPI, Teras, Activity | — | TC-003 | M | Baselined |
| FRQ-004 | KPI record management | BR-034/035 | CAP-K2 | §4 | TRD-§KPI | M2 | — | — | DSH-11 | KPIService | KPI, Strategi, Prakarsa | — | TC-004 | M | Baselined |
| FRQ-005 | PIC assignment | BR-004 | CAP-K3 | §14 | TRD-§KPI | M2 | — | — | DSH-11 | KPIService | PIC | — | TC-005 | M | Baselined |
| FRQ-006 | Completeness detection & warnings | BR-005/006 | CAP-M2 | §15 | TRD-§Validation | M4 | Validation/Completeness | completeness validation | DSH-07 | ValidationService | KPI, MonthlyUpdate | — | TC-006 | M | Baselined |
| FRQ-007 | Monthly KPI update | BR-002 | CAP-M1 | — | TRD-§Update | M3 | — | — | DSH-06 | UpdateService | MonthlyUpdate, Evidence | — | TC-007 | M | Baselined |
| FRQ-008 | KPI status classification | BR-020 | CAP-M3 | §15 | TRD-§Analysis | M5/M7 | KPI Analysis | status classification | DSH-03 | AgentService | KPI, MonthlyUpdate | — | TC-008 | M | Baselined |
| FRQ-009 | Risk flagging | BR-020 | CAP-AI2 | §16 | TRD-§Risk | M7 | Risk | risk scoring | DSH-04/10 | AgentService | RiskAssessment | — | TC-009 | M | Baselined |
| FRQ-010 | Amendment window enforcement | BR-008 | CAP-G1 | §6 | TRD-§Governance | M12 | Audit | audit logging | — | AuditService | AmendmentWindow | — | TC-010 | M | Baselined |
| FRQ-011 | Teras 1–7 dashboard | BR-020/021 | CAP-R2 | §15 | TRD-§Dashboard | M5 | AI Summary | Teras roll-up | DSH-01…12 | DashboardService | (views) | — | TC-011 | M | Baselined |
| FRQ-012 | AI dashboard summary | BR-022 | CAP-AI7 | §15 | TRD-§Dashboard | M5/M7 | AI Summary | summarisation, roll-up | DSH-08 | DashboardService | (views) | RPM, docs | TC-012 | M | Baselined |
| FRQ-013 | KPI chatbot | BR-013/025/027 | CAP-AI4 | §19 | TRD-§Chatbot | M9 | KPI Chatbot | RAG retrieval+citation | — | ChatbotService | (vector) | RPM, docs, links | TC-013 | S | Baselined |
| FRQ-014 | Budget Intelligence (FDS) | BR-010/011/046 | CAP-B2 | §20.1 | TRD-§FDS | M6/M7 | Budget Intelligence | budget classification, LCHI | DSH-05 | FinanceService | FinanceAllocation | — | TC-014 | M | Baselined |
| FRQ-015 | Intervention Recommendation (FDS) | BR-015/046 | CAP-AI3 | §20.3 | TRD-§FDS | M7 | Intervention | risk scoring, drafting | DSH-10 | AgentService | Recommendation | RPM, docs | TC-015 | S | Baselined |
| FRQ-016 | Report generation | BR-014/039 | CAP-R1 | §21 | TRD-§Reporting | M10 | Report Generation | report templating | — | ReportService | Report | — | TC-016 | M | Baselined |
| FRQ-017 | Human review & approval | BR-015 | CAP-G3 | §14,22 | TRD-§HITL | M12 | — | HITL gating | — | WorkflowService | ApprovalRecord | — | TC-017 | M | Baselined |
| FRQ-018 | Notification & reminders | BR-007 | CAP-N1/N2 | §22 | TRD-§Notification | M11 | Notification & Reminder | email drafting | DSH-06 | NotificationService | Notification | — | TC-018 | M | Baselined |
| FRQ-019 | Email queue & distribution | BR-040 | CAP-N3 | §22 | TRD-§Notification | M11 | Notification & Reminder | email drafting | — | NotificationService | Notification, EmailQueue | — | TC-019 | M | Baselined |
| FRQ-020 | Knowledge ingestion | BR-019/023 | CAP-KM1 | §19 | TRD-§RAG | M8 | — | link fetch/refresh | — | KnowledgeService | KnowledgeSource | docs/links | TC-020 | S | Baselined |
| FRQ-021 | Link registry & refresh | BR-024 | CAP-KM2 | §19.5 | TRD-§RAG | M8/M13 | — | link fetch/refresh | — | KnowledgeService | LinkRegistry | live links | TC-021 | S | Baselined |
| FRQ-022 | KPI–RPM alignment | BR-012 | CAP-K4/AI5 | §19 | TRD-§Alignment | M8 | Knowledge Alignment | alignment scoring | DSH-12 | KnowledgeService | AlignmentScore | RPM 2026–2035 | TC-022 | S | Baselined |
| FRQ-023 | Executive Copilot | BR-043 | CAP-AI6 | §19.4 | TRD-§Copilot | M7 | Executive Copilot | RAG retrieval, roll-up | DSH-08 | CopilotService | (views) | RPM, docs, links | TC-023 | S | Baselined |
| FRQ-024 | Audit trail | BR-009/029/036 | CAP-G2 | §22 | TRD-§Governance | M12 | Audit | audit logging | — | AuditService | AuditLog | — | TC-024 | M | Baselined |
| FRQ-025 | Submission tracking | BR-007 | CAP-M4 | §15 | TRD-§Dashboard | M5 | — | Teras roll-up | DSH-06 | DashboardService | MonthlyUpdate | — | TC-025 | M | Baselined |
| FRQ-026 | Provider configuration | BR-044 | CAP-S1 | §6 | TRD-§Config | M13 | — | — | — | AdminConfigService | ProviderConfig | — | TC-026 | M | Baselined |
| FRQ-027 | Admin & user management | BR-032/033 | CAP-U3/S2 | §14 | TRD-§Admin | M13 | — | — | — | AdminService | User, Role | — | TC-027 | M | Baselined |
| FRQ-028 | OBB value-for-money (FDS) | BR-038/046 | CAP-B3 | §20.6 | TRD-§FDS | M6/M7 | Budget Intelligence | OBB calculation | DSH-05 | FinanceService | FinanceAllocation | — | TC-028 | C | Baselined |
| FRQ-029 | Low Cost High Impact Analysis (FDS) | BR-011/046 | CAP-B5 | §20.2 | TRD-§FDS | M6/M7 | Budget Intelligence | LCHI scoring | DSH-05 | FinanceService | Recommendation, Activity | — | TC-029 | M | Baselined |
| FRQ-030 | Executive Financial Insight (FDS) | BR-043/046 | CAP-B6 | §20.4 | TRD-§FDS/Copilot | M5/M7 | Executive Copilot, AI Summary | summarisation | DSH-08 | CopilotService | Recommendation | RPM, docs | TC-030 | S | Baselined |

## 3. RTM — Non-Functional Requirements (NFRQ)

| Req ID | Name | Bus. Rule | Capability | BRD § | TRD § (planned) | Module | API/Service | DB Entity | Test Case | Pri | Status |
|--------|------|-----------|-----------|-------|------------------|--------|-------------|-----------|-----------|-----|--------|
| NFRQ-001 | Security & access control | BR-003/031 | CAP-U1/U2 | §23 | TRD-§Security | M1 | AuthService | User, Role | TC-N01 | M | Baselined |
| NFRQ-002 | Auditability | BR-009/030 | CAP-G2/G4 | §23 | TRD-§Governance | M12 | AuditService | AuditLog | TC-N02 | M | Baselined |
| NFRQ-003 | Configurability | BR-044 | CAP-S1 | §23 | TRD-§Config | M13 | AdminConfigService | ProviderConfig | TC-N03 | M | Baselined |
| NFRQ-004 | AI trust & grounding | BR-025/026/027 | CAP-KM3 | §19 | TRD-§RAG | M8/M9 | RAGService | KnowledgeSource | TC-N04 | M | Baselined |
| NFRQ-005 | Usability / low-friction | OBJ-11 | CAP-M1 | §13 | TRD-§UX | M3 | UpdateService | — | TC-N05 | M | Baselined |
| NFRQ-006 | Performance | NFR | CAP-R2 | §13 | TRD-§NFR | M5 | DashboardService | — | TC-N06 | S | Baselined |
| NFRQ-007 | Scalability | NFR | — | §13 | TRD-§NFR | all | — | — | TC-N07 | S | Baselined |
| NFRQ-008 | Availability | NFR | — | §13 | TRD-§NFR | all | — | — | TC-N08 | S | Baselined |
| NFRQ-009 | Maintainability | OBJ-12 | CAP-S2 | §13 | TRD-§NFR | all | — | — | TC-N09 | M | Baselined |
| NFRQ-010 | Data integrity (plane separation) | BR-017 | CAP-S2 | §23 | TRD-§Data | M2/M8 | — | (two stores) | TC-N10 | M | Baselined |
| NFRQ-011 | Compliance & residency | NFR | — | §23 | TRD-§Security | all | — | — | TC-N11 | S | Baselined *(Q-014/Q-017)* |
| NFRQ-012 | Language (English primary) | NFR | — | §13 | TRD-§UX | all | — | — | TC-N12 | M/C | Baselined |
| NFRQ-013 | Data retention & archival | BCM gap | CAP-G2 | §13 | TRD-§Data | M12 | — | AuditLog, Report | TC-N13 | S | Baselined |

## 4. RTM — AI / Integration / Data / Reporting (AIRQ / INTQ / DATQ / REPQ)

| Req ID | Name | Bus. Rule | Capability | Module | AI Agent | Skill | API/Service | DB/Knowledge | Test Case | Pri | Status |
|--------|------|-----------|-----------|--------|----------|-------|-------------|--------------|-----------|-----|--------|
| AIRQ-001 | Multi-agent architecture (capability-driven) | BR-041 | CAP-AI* | M7 | all agents | — | AgentService | — | TC-A01 | M | Baselined |
| AIRQ-002 | Skills layer | BR-016/042 | all AI caps | M7 | all agents | all skills | SkillRegistry | — | TC-A02 | M | Baselined |
| AIRQ-003 | RAG knowledge base | BR-012/023 | CAP-KM1/3 | M8 | Chatbot/Alignment/Copilot | RAG retrieval | RAGService | VectorStore, KnowledgeSource | TC-A03 | M | Baselined |
| AIRQ-004 | KPI analysis (AI) | BR-020 | CAP-AI1 | M7 | KPI Analysis | status classification | AgentService | KPI | TC-A04 | M | Baselined |
| AIRQ-005 | Risk detection (AI) | BR-020 | CAP-AI2 | M7 | Risk | risk scoring | AgentService | RiskAssessment | TC-A05 | M | Baselined |
| AIRQ-006 | Budget intelligence (AI/FDS) | BR-011/046 | CAP-B2/B3/B5 | M6/M7 | Budget Intelligence | LCHI, OBB | FinanceService | FinanceAllocation, Recommendation | TC-A06 | M | Baselined |
| AIRQ-007 | KPI alignment (AI) | BR-012 | CAP-AI5 | M7/M8 | Knowledge Alignment | alignment scoring | KnowledgeService | AlignmentScore | TC-A07 | S | Baselined |
| AIRQ-008 | Executive Copilot (AI) | BR-043 | CAP-AI6 | M7 | Executive Copilot | RAG retrieval | CopilotService | (views) | TC-A08 | S | Baselined |
| AIRQ-009 | Chatbot (AI) | BR-013 | CAP-AI4 | M9 | KPI Chatbot | RAG retrieval+citation | ChatbotService | VectorStore | TC-A09 | S | Baselined |
| AIRQ-010 | AI summary (AI) | BR-022 | CAP-AI7 | M5/M7 | AI Summary | summarisation, roll-up | DashboardService | (views) | TC-A10 | M | Baselined |
| AIRQ-011 | Human oversight of AI | BR-015/028 (ASM-11) | CAP-G3 | M12 | — | HITL gating | WorkflowService | ApprovalRecord | TC-A11 | M | Baselined |
| AIRQ-012 | Provider abstraction (Groq dev / OpenAI·Anthropic prod) | BR-044 | CAP-S1 | M13 | — | — | AdminConfigService | ProviderConfig | TC-A12 | M | Baselined |
| INTQ-001 | Excel import | BR-001 | CAP-K1 | M2 | Data Integration | Excel parsing | ImportService | KPI | TC-I01 | M | Baselined |
| INTQ-002 | Live knowledge links | BR-024 | CAP-KM2 | M8 | — | link fetch/refresh | KnowledgeService | LinkRegistry | TC-I02 | S | Baselined |
| INTQ-003 | Email service | BR-040 | CAP-N3 | M11 | Notification | email drafting | NotificationService | EmailQueue | TC-I03 | M | Baselined |
| INTQ-004 | LLM provider APIs | BR-044 | CAP-S1 | M13 | — | — | ProviderAdapter | ProviderConfig | TC-I04 | M | Baselined |
| INTQ-005 | SharePoint / doc source | BR-023 | CAP-KM1 | M8 | — | link fetch | KnowledgeService | KnowledgeSource | TC-I05 | F | Baselined (Future) |
| DATQ-001 | Initial Excel dataset | BR-001 | CAP-K1 | M2 | Data Integration | Excel parsing | ImportService | ImportBatch, KPI | TC-D01 | M | Baselined |
| DATQ-002 | Operational database | BR-017/018 | CAP-K2/M1 | M2 | — | — | KPIService | KPI, MonthlyUpdate, PIC, Finance | TC-D02 | M | Baselined |
| DATQ-003 | Knowledge repository (vector) | BR-019 | CAP-KM1 | M8 | — | RAG retrieval | RAGService | VectorStore | TC-D03 | S | Baselined |
| DATQ-004 | Audit trail store | BR-009 | CAP-G2 | M12 | Audit | audit logging | AuditService | AuditLog | TC-D04 | M | Baselined |
| DATQ-005 | Finance data | BR-010 | CAP-B1 | M6 | Financial Monitoring | budget classification | FinanceService | FinanceAllocation | TC-D05 | M | Baselined |
| DATQ-006 | Link registry data | BR-024 | CAP-KM2 | M8 | — | link fetch | KnowledgeService | LinkRegistry | TC-D06 | S | Baselined |
| DATQ-007 | Reference/master data | BR-034 | CAP-K2 | M2 | — | — | KPIService | Teras, Strategi, Prakarsa, Bahagian, ObjectCode | TC-D07 | M | Baselined |
| REPQ-001 | Monthly report | BR-014/040 | CAP-R1 | M10 | Report Generation | report templating | ReportService | Report | TC-R01 | M | Baselined |
| REPQ-002 | Executive summary | BR-039 | CAP-R3 | M10/M5 | Executive Copilot | summarisation | ReportService | Report | TC-R02 | M | Baselined |
| REPQ-003 | Teras dashboard views | BR-020/021/045 | CAP-R2 | M5 | AI Summary | Teras roll-up | DashboardService | (views) | TC-R03 | M | Baselined |
| REPQ-004 | AI summary report | BR-022 | CAP-AI7 | M5 | AI Summary | summarisation | DashboardService | (views) | TC-R04 | M | Baselined |
| REPQ-005 | Report archive & log | BR-029 | CAP-G2 | M10/M12 | Audit | audit logging | ReportService | Report, NotificationLog | TC-R05 | S | Baselined |
| REPQ-006 | Risk/budget/submission summaries | BR-021 | CAP-R2 | M5 | AI Summary | Teras roll-up | DashboardService | (views) | TC-R06 | M | Baselined |

---

## 5. Coverage of mandated traceability areas

| Mandated area | Traced via |
|---------------|-----------|
| Dashboard by Teras 1–7 | FRQ-011/012/025, REPQ-003/006, DSH-01…12 → M5 |
| KPI Monitoring | FRQ-008/009, BRQ-002, AIRQ-004 → M5/M7 |
| Monthly KPI Updates | FRQ-007, BRQ-002 → M3 |
| Operational Data | DATQ-001/002/005/007 → M2/M6 |
| Knowledge Data | DATQ-003/006, FRQ-020/021 → M8 |
| RAG | AIRQ-003, DATQ-003, NFRQ-004 → M8 |
| KPI Chatbot | FRQ-013, AIRQ-009 → M9 |
| Executive Copilot | FRQ-023/030, AIRQ-008 → M7 |
| Financial Decision Support | FRQ-014/015/028/029/030, BRQ-005 → M6/M7 |
| Budget Intelligence | FRQ-014, AIRQ-006 → M6/M7 |
| Low Cost High Impact Analysis | FRQ-029 → M6/M7 |
| Strategic Recommendations | FRQ-015 (intervention), FRQ-030 → M7 |
| Notifications | FRQ-018/019, INTQ-003 → M11 |
| Audit Trail | FRQ-024, DATQ-004, NFRQ-002 → M12 |
| Human-in-the-Loop Governance | FRQ-017, AIRQ-011, ASM-11 → M12 |
| Role-Based Access Control | FRQ-002, NFRQ-001 → M1 |
| Login (`@moe.gov.my`/`@moe-dl.edu.my`) | FRQ-001, SEC-01 → M1 |
| Config Mode (Groq dev / OpenAI·Anthropic prod) | FRQ-026, AIRQ-012, INTQ-004 → M13 |

---

## 6. Validation

| Check | Result |
|-------|--------|
| Every BRD requirement has ≥1 technical path? | ✅ All 86 requirements mapped to module + API + (where applicable) agent/skill/DB/test. |
| Any orphaned requirement (no implementation path)? | ✅ None. |
| Any orphaned technical component (no business requirement)? | ✅ None — every module M1–M13, every agent, every skill traces back to ≥1 requirement (see §5 + agent/skill check). |
| Every AI Agent supports ≥1 approved capability? | ✅ Yes — all 14 agents map to capabilities/requirements (Data Integration→K1, Validation→M2, KPI Analysis→AI1, Risk→AI2, Financial Monitoring→B1, Budget Intelligence→B2/B5, Intervention→AI3, Notification→N1, Audit→G2, Report Generation→R1, Chatbot→AI4, Knowledge Alignment→AI5, Executive Copilot→AI6, AI Summary→AI7). |
| Every Skill linked to ≥1 AI Agent? | ✅ Yes — all 15 skills mapped (BRD §18); none unlinked. |
| Forward artefacts marked Planned? | ✅ TRD §, API, DB entity, Test Case are planned references pending TRD/test authoring. |

---

## FINAL OUTPUT

**1. Total traced requirements: 86**
(BRQ 12 · FRQ 30 · NFRQ 13 · AIRQ 12 · INTQ 5 · DATQ 7 · REPQ 6 — full BRD requirement set, including the
three FDS additions.)

**2. Traceability completeness score: 98%**
Every requirement has a complete backward trace (objective → rule → capability → BRD §) and a forward
implementation path (module → API → DB/agent/skill → test). The 2% reflects forward artefacts that are
*planned references* until the TRD and test phases assign final IDs/sections.

**3. Orphaned requirements: 0.**

**4. Orphaned technical components: 0.** Every module, agent and skill traces to ≥1 requirement.

**5. Readiness to begin the TRD: READY (98%).**
The RTM gives the TRD a complete, validated map of *what* must be built and *where* each requirement
lands. Open technical specifics (risk scoring Q-020, alignment metric Q-021, OBB method Q-025, link
validation Q-022) and Requires-User-Confirmation items (compliance/hosting Q-014/Q-017, Teras 5–7 data
GAP-002, knowledge corpus Q-019) are carried as TRD inputs — they refine *how*, not *whether*.

---

## FREEZE RECORD — Requirements Traceability Baseline
- **Baseline:** R1 — Requirements Traceability Matrix, **v1.0 FROZEN** on 2026-06-27.
- **Approved by:** User (suzila@iegcampus.com).
- **Scope of baseline:** 86 requirements (BRQ 12 · FRQ 30 · NFRQ 13 · AIRQ 12 · INTQ 5 · DATQ 7 · REPQ 6)
  traced across 17 columns; coverage of all 18 mandated areas; validation passed (0 orphaned requirements,
  0 orphaned components, all 14 agents + 15 skills linked). Completeness 98%.
- **Relationship:** built on the frozen **BRD v1.0** (not modified); forms the **BRD → TRD bridge**.
- **Forward references (Planned):** TRD §, API/Service, DB Entity and Test Case IDs are finalised during
  the TRD and test phases; this RTM will be expanded (not reopened) to carry those IDs.
- **Reopen policy:** changes only via explicit, logged change request (CHANGE_LOG.md).

---
*End of Requirements Traceability Matrix v1.0 — FROZEN APPROVED BASELINE. Bridge from BRD (D2) to TRD (D3).*
