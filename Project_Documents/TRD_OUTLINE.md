# TECHNICAL REQUIREMENTS DOCUMENT (TRD) — OUTLINE / STRUCTURE
### Agentic AI Strategic Governance Platform — RPM 2026–2035

| Field | Value |
|-------|-------|
| Document | T1 — TRD Outline (structure only) |
| Version | 1.0 (APPROVED) |
| Date | 2026-06-27 |
| Status | **APPROVED** (outline) — TRD authoring proceeds against this structure |
| Purpose | Define the **structure** of the TRD (D3) before writing it |
| Baselines (frozen, not modified) | HMW v1.0, BRD v1.0, RTM v1.0 |
| Boundary | Outline only — **no TRD content written.** Describes *how*; introduces **no new business requirements**. |

### Approved Technical Stack (CL-031 / AD-007) — default for the TRD
| Layer | Technology |
|-------|-----------|
| Frontend (L1) | React · Vite · Tailwind CSS · **ShadCN UI** · **Recharts** |
| Backend (L2) | Python · **FastAPI** · **SQLAlchemy** |
| Database (L5) | **SQLite (dev)** · **PostgreSQL (prod)** |
| Vector/RAG (L4) | **Chroma or pgvector** (per architecture) · **keyword-search fallback** for V1 |
| AI Provider (L3) | Groq (dev) · OpenAI/Anthropic (prod) via `config.md` + `.env` |
| Hosting (L6) | Local (dev) · Cloud/government-approved (prod) — **Requires User Confirmation** for compliance/residency |

> **Review outcome:** the 31 proposed sections are sound. I recommend **4 added sections** (Data Ingestion
> & Import Pipeline; Monthly KPI Workflow; Non-Functional/Performance & Scalability; Backup, Retention &
> DR) and confirm coverage of all mandatory topics, capabilities, AI capabilities and the 13 RTM modules.
> Net structure = **35 numbered sections**, each mapped to one or more of the 6 architecture layers.

---

## Layer legend
**L1 Presentation · L2 Application · L3 AI · L4 Knowledge · L5 Data · L6 Infrastructure**

---

## 1. Complete TRD Table of Contents (purpose · layer)

### Front matter & overview
1. **Document Control** — version, authors, approvers, sign-off, change control, traceability to BRD/RTM. *(—)*
2. **Executive Technical Overview** — one-page technical synthesis of the solution. *(all)*
3. **Technical Objectives** — translate OBJ-01…12 into technical goals (no new requirements). *(all)*
4. **Overall Solution Architecture** — high-level architecture, context diagram, component map. *(all)*
5. **Layered System Architecture** — the 6 layers (L1–L6), responsibilities, dependencies. *(all)*

### Presentation & application
6. **Frontend Architecture** — React + Vite + Tailwind (BRD §6, TR-P01); component model, state, routing. *(L1)*
7. **Backend Architecture** — application services, orchestration, workflow engine. *(L2)*
8. **Monthly KPI Workflow** [ADDED] — technical realisation of Phase 3 (login→achievement→finance→evidence→save→audit) + amendment-window enforcement. *Justification: the core operational loop (FRQ-007/010) needs a dedicated technical section; otherwise split across backend/data.* *(L2/L5)*
9. **Data Ingestion & Import Pipeline** [ADDED] — one-time Excel import (parse Teras sheets, validate, load), import-once enforcement. *Justification: FRQ-003/INTQ-001/DATQ-001 is a distinct one-time subsystem (Data Integration Agent + parsing skill) not covered by "Integration" or "Data Model".* *(L2/L5)*

### Data & knowledge
9.→10. **Database Architecture** — DBMS choice, operational store design, indexing, transactions. *(L5)*
11. **Data Model** — entities (KPI, Teras, PIC, MonthlyUpdate, FinanceAllocation, AuditLog, etc. per RTM), relationships, reference/master data. *(L5)*
12. **Operational Data vs Knowledge Data (Dual Data Plane)** [mandatory] — strict separation (BR-017/AD-004); what lives where; integrity controls. *(L5/L4)*

### AI & knowledge layer
13. **AI Architecture** — AI layer design, provider-agnostic core, orchestration, advisory+HITL flow. *(L3)*
14. **Multi-Agent Architecture** — capability-driven agents (current roster; count may evolve), agent lifecycle, inter-agent flow, **Human-in-the-Loop Governance** subsection. *(L3)*
15. **Skills Architecture** — reusable skills registry, interfaces, agent-skill binding, testability. *(L3)*
16. **RAG / Knowledge Architecture** — ingestion (uploaded docs + live links), chunking, embedding, vector store, retrieval+citation, fallback; **link validation by admin** (Q-022 resolution). *(L4)*
17. **Financial Decision Support (FDS) Architecture** [mandatory, top-level] — Budget Intelligence (status/funding-gap/risk), **Low Cost High Impact Analysis**, Intervention Recommendation, **Executive Financial Insight**, resource-optimisation; OBB method. *(L3/L2)*
18. **KPI Chatbot Architecture** [mandatory] — chatbot service, grounding order, citation, fallback string. *(L3/L4)*
19. **Executive Copilot Architecture** [mandatory] — synthesis of operational + knowledge signals; advisory output. *(L3)*

### Presentation (analytics) & access
20. **Dashboard Architecture (Teras 1–7)** [mandatory] — aggregation/roll-up by Teras, DSH-01…12 components, charts (phased), drill-down, role-scoping. *(L1/L2)*
21. **Authentication & Role-Based Access Control** — MOE-domain auth (`@moe.gov.my`/`@moe-dl.edu.my`), RBAC model, permission enforcement. *(L2/L6)*
22. **API Architecture** — service/endpoint catalogue (per RTM API column), contracts, versioning, error envelope. *(L2)*

### Configuration & infrastructure
23. **Configuration Strategy** [mandatory] — `config.md`, **Config Mode Switching** (dev→Groq, prod→OpenAI/Anthropic), **AI Provider Abstraction** layer. *(L6/L3)*
24. **Environment Configuration** — `.env`, API keys, secrets management. *(L6)*
25. **Integration Architecture** — Excel, live links, email, LLM provider APIs, future SharePoint (INTQ-001…005). *(L6/L2)*
26. **Notification & Email Architecture** [mandatory] — reminder/alert engine, escalation, email queue, approved distribution. *(L2)*
27. **Audit Trail & Version History** [mandatory] — append-only audit store, **Version Control** & **Change History** of KPI/amendments/decisions. *(L5)*
28. **Security Architecture** — auth, data protection, plane separation, knowledge-source trust, compliance/residency (Q-014/Q-017 inputs). *(L6)*
29. **Logging & Monitoring** — application/AI logging, observability, alerting. *(L6)*
30. **Error Handling Strategy** — error taxonomy, graceful failure (incl. inaccessible knowledge source → clear message). *(L2/L6)*
31. **Non-Functional & Performance/Scalability Architecture** [ADDED] — realise NFRQ-006/007/008 (performance, scalability, availability). *Justification: NFRs need a technical home; otherwise untraceable.* *(L6/all)*
32. **Backup, Retention & Disaster Recovery** [ADDED] — data retention (NFRQ-013), backup/restore, DR over the 10-yr horizon. *Justification: government 10-year system; retention/DR not covered elsewhere.* *(L6/L5)*
33. **Deployment Architecture** — environments (dev/prod), hosting (gov-cloud/on-prem — Q-014), CI/CD, build-by-layer alignment. *(L6)*
34. **Technical Testing Strategy** — per-layer testing, test-case scheme (TC-* from RTM), AI/RAG evaluation, UAT. *(all)*

### Closure
35. **Technical Risks · Technical Assumptions · Technical Traceability · Appendices** — risks; assumptions (ASM-07/08/09 technical items); RTM forward-mapping (TRD §→component→API→test); appendices (entity list, API catalogue, agent/skill specs, config schema).
   - 35.1 Technical Risks · 35.2 Technical Assumptions · 35.3 Technical Traceability · 35.4 Appendices.

> Original §1–§31 preserved; added §8, §9 (import), §31, §32; mandatory topics given dedicated sections
> (Chatbot §18, Copilot §19, Dual Data Plane §12). Rendered as 35 numbered sections.

---

## 2. Layer → Section map

| Layer | Sections |
|-------|----------|
| **L1 Presentation** | 6 Frontend, 20 Dashboard |
| **L2 Application** | 7 Backend, 8 Monthly Workflow, 9 Import, 21 RBAC, 22 API, 26 Notification, 30 Error handling |
| **L3 AI** | 13 AI Arch, 14 Multi-Agent, 15 Skills, 17 FDS, 18 Chatbot, 19 Copilot, 23 Provider abstraction |
| **L4 Knowledge** | 12 Dual plane, 16 RAG/Knowledge |
| **L5 Data** | 10 Database, 11 Data Model, 12 Dual plane, 27 Audit/Version, 32 Backup/Retention |
| **L6 Infrastructure** | 23 Config, 24 Env, 25 Integration, 28 Security, 29 Logging/Monitoring, 31 NFR/Perf, 33 Deployment |

---

## 3. Coverage Review (before finalising)

**Every Business Capability → technical section:**
| Capability domain | TRD section |
|-------------------|-------------|
| D1 Governance | §14 (HITL), §27 (audit) |
| D2 KPI Management | §9 (import), §10/§11 (data), §8 (workflow) |
| D3 Monthly Monitoring | §8, §20 |
| D4 Financial Decision Support | §17 |
| D5 Knowledge Management | §16, §12 |
| D6 AI Decision Support | §13/§14/§15/§17/§18/§19 |
| D7 Reporting & Analytics | §20, §26, (reporting in §7/§22) |
| D8 User & Security | §21, §28 |
| D9 Notification & Comms | §26 |
| D10 System Administration | §23, §24, §33 |

**Every AI capability → implementation section:** KPI Analysis/Risk/Intervention/Alignment/Chatbot/Copilot/AI-Summary → §13/§14/§17/§18/§19; Budget Intelligence/Low Cost High Impact/OBB → §17.

**Every RTM module (M1–M13) → technical home:** M1→§21; M2→§9/§10/§11; M3→§8; M4→§16/§8; M5→§20; M6→§17; M7→§14; M8→§16; M9→§18; M10→§7/§26; M11→§26; M12→§27; M13→§23/§24/§33. ✅ All 13 mapped.

**No new business requirements introduced:** ✅ confirmed — the TRD describes *how* only; every section traces to existing BRD/RTM IDs.

**Mandatory topics:** all present — Dashboard Teras 1–7 (§20), Operational vs Knowledge (§12), FDS (§17), Budget Intelligence/Low Cost High Impact (§17), Executive Copilot (§19), KPI Chatbot (§18), HITL (§14), Config Mode Switching/Provider Abstraction (§23), RAG docs+live links (§16), Monthly KPI Workflow (§8), Audit Trail (§27), Email/Notification (§26), Version Control/Change History (§27).

---

## 4. Recommended Writing Order

1. **§2–§5** (overview → solution → layered architecture) — set the frame.
2. **§10–§12** (Database, Data Model, Dual Plane) — data foundation everything depends on.
3. **§9, §8** (Import pipeline, Monthly workflow) — core operational backbone.
4. **§7, §22, §21** (Backend, API, Auth/RBAC) — application + access spine.
5. **§13–§17** (AI, Agents, Skills, RAG, FDS) — the AI/knowledge core.
6. **§18, §19, §20** (Chatbot, Copilot, Dashboard) — AI-facing surfaces.
7. **§23–§26** (Config, Env, Integration, Notification) — configuration & integration.
8. **§27–§33** (Audit, Security, Logging, Errors, NFR, Backup, Deployment) — cross-cutting & ops.
9. **§34** (Testing) — once components are defined.
10. **§35** (Risks, Assumptions, Traceability, Appendices) — closure.
11. **§2 Executive Technical Overview** refined last; **§1 Document Control** finalised at freeze.

---

## 5. Estimated Page Count

| Block | Sections | Est. pages |
|-------|----------|-----------|
| Overview & architecture | 1–5 | 10–14 |
| App, workflow, import | 6–9 | 12–16 |
| Data & knowledge | 10–12, 16 | 14–18 |
| AI core (agents/skills/FDS/chatbot/copilot) | 13–15, 17–19 | 18–24 |
| Dashboard, auth, API | 20–22 | 10–14 |
| Config, env, integration, notification | 23–26 | 10–14 |
| Audit, security, ops, NFR, backup, deploy | 27–33 | 14–18 |
| Testing & closure | 34–35 | 8–12 |
| **Total** | | **~96–130 pages** |

> Enterprise Agentic-AI TRD with diagrams, data model, API and agent specs. A V1-scoped TRD
> (Must-have components, referencing RTM rather than reproducing it) would be **~60–80 pages**.

---

## 6. Readiness to begin writing the TRD

**READY.** The structure covers every capability, AI capability, RTM module and mandatory topic; maps cleanly
to the 6 layers; introduces no new business requirements; and remains fully traceable to the frozen BRD/RTM.

**Two inputs that sharpen specific sections (not blockers — can be written with documented assumptions):**
- §28/§33 — government **hosting/compliance/residency** (Q-014/Q-017).
- §11/§16 — **backend stack & vector store** choice (frontend = React/Vite/Tailwind confirmed; backend Q-013).
Recommend confirming the **backend stack + hosting** before §7/§10/§33, or I proceed with a recommended
default (e.g., Python/FastAPI + PostgreSQL + a vector store) flagged as a technical assumption.

---
*End of TRD Outline v0.1 — DRAFT. Full TRD NOT written. Awaiting approval.*
