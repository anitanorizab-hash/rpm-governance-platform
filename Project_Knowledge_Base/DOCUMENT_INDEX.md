# DOCUMENT_INDEX.md

> **Single Source of Truth — Document Register & Status**
> Status: `LIVING DOCUMENT` · Version: 0.1 (DRAFT) · Last updated: 2026-06-27

---

## Purpose
Tracks **every project document** and its lifecycle status, so it is always clear what is drafted,
under review, approved or frozen. The control panel for the documentation roadmap.

## Status values
`Draft` · `Under Review` · `Approved` · `Frozen` · `Not Started`

## When updated
- When a document moves between statuses (also log freezes in `CHANGE_LOG.md`).

## Relationship with other documents
- **References:** every artifact; pairs with `CHANGE_LOG.md` for freeze history.

---

### Knowledge Base documents
| # | Document | Status | Version | Notes |
|---|----------|--------|---------|-------|
| 1 | PROJECT_CONTEXT.md | Draft | 0.1 | Living |
| 2 | PROJECT_GLOSSARY.md | Draft | 0.1 | Living |
| 3 | BUSINESS_RULES.md | Draft | 0.1 | Living |
| 4 | TECHNICAL_RULES.md | Draft | 0.1 | Living |
| 5 | AI_RULES.md | Draft | 0.1 | Living |
| 6 | ARCHITECTURE_DECISIONS.md | Draft | 0.1 | Living |
| 7 | QUESTIONS_AND_GAPS.md | Draft | 0.1 | Living |
| 8 | REQUIREMENTS_REGISTER.md | Draft | 0.1 | Living |
| 9 | TRACEABILITY_REGISTER.md | Draft | 0.1 | Living |
| 10 | CHANGE_LOG.md | Draft | 0.1 | Living |
| 11 | DOCUMENT_INDEX.md | Draft | 0.1 | This file |

### Architecture blueprints (post-TRD)
| # | Document | Status | Notes |
|---|----------|--------|-------|
| A5 | Database Architecture Blueprint (`Project_Documents/10_DATABASE_ARCHITECTURE.md`) | **APPROVED v1.0** ✅ | Approved 2026-06-27 | 38 entities across Operational(24)/Knowledge(7)/AI(7); 4 ER diagrams; validation; implementation order. Guide for `/database` |
| A6 | API Architecture Blueprint (`Project_Documents/11_API_ARCHITECTURE.md`) | **APPROVED v1.0** ✅ | Approved 2026-06-27 | 18 API groups (FastAPI `/api/v1`), endpoint catalogue, service-to-API map, 6 flow diagrams, implementation order. Guide for `/routes`, `/services` |
| A7 | Implementation Prep (`Project_Documents/12_IMPLEMENTATION_PREP.md`) + **`CLAUDE.md`** (root dev instruction file) | **APPROVED v1.0** ✅ | Approved 2026-06-27 | Final pre-coding package. |
| A8 | Development Dependency Map (`Project_Documents/13_DEVELOPMENT_DEPENDENCY_MAP.md`) | **APPROVED v1.0** ✅ | Approved 2026-06-27 | Build-dependency map (24 items), build order, parallel tracks, blocking rules, CP1 prompt |
| D9 | Development CLAUDE.md (`./CLAUDE.md`) | **APPROVED v1.0** ✅ | Approved 2026-06-27 | Canonical coding instruction file (15 rule sections, stack, build sequence, control checklist) |

### Project deliverables (roadmap)
| # | Document | Status | Gate | Notes |
|---|----------|--------|------|-------|
| D1 | HMW & Problem Discovery (`Project_Documents/02_PAIN_POINTS_HMW.md`) | **FROZEN v1.0** ✅ | Frozen 2026-06-27 | Approved baseline. 18 pain points, 13 problem statements, 25 HMW, 12 stakeholders; overall quality 96% |
| B4 | As-Is Business Process Analysis (`Project_Documents/AS_IS_BUSINESS_PROCESS.md`) | Draft v0.1 | Awaiting approval | 9 actors, 10 workflow steps, 14 pain points, 10 risks; scores 94%/90% |
| B5 | To-Be Business Process Design (`Project_Documents/TO_BE_BUSINESS_PROCESS.md`) | Draft v0.1 | Awaiting approval | 7 phases, 8 human + system actors, proposed 14-agent roster, skills layer, dashboard/knowledge/AI workflows; overall 95%. Master blueprint for BRD/TRD/Arch |
| B6 | Business Capability Model (`Project_Documents/BUSINESS_CAPABILITY_MODEL.md`) | Draft v0.1 | Awaiting approval | 10 domains, ~35 capabilities, full AI mapping, maturity, traceability, gap analysis; scores 95%/95%/96%/96% |
| B7 | Business Rules Catalogue (`Project_Documents/BUSINESS_RULES_CATALOGUE.md`) | Draft v0.1 | Awaiting approval | 45 rules (BR-001…045) in 10 domains + traceability; BR-028…045 pending confirm-into-master. Completeness 96%, traceability 95% |
| B8 | Master Requirements Catalogue (`Project_Documents/MASTER_REQUIREMENTS_CATALOGUE.md`) | Draft v0.1 | Awaiting approval | 83 requirements across 7 categories (BRQ/FRQ/NFRQ/AIRQ/INTQ/DATQ/REPQ), MoSCoW, full traceability to capability/BR/module. Readiness 96% |
| B9 | BRD Outline (`Project_Documents/BRD_OUTLINE.md`) | Draft v0.1 | Awaiting approval | 34-section BRD structure (30 top-level), 31 orig + 4 added + 2 merged, full requirement coverage map, writing order, ~72–99 pp est. |
| D2 | BRD (`Project_Documents/03_BRD.md`) | **FROZEN v1.0** ✅ | Frozen 2026-06-27 (Gate 1) | Approved baseline. §1–§30 + App A–H; OBJ-01…12; 86 reqs incl. FDS; 45 rules incl. BR-046; ASM-01…11; FDS = top-level capability. Foundation for TRD (D3). |
| T1 | TRD Outline (`Project_Documents/TRD_OUTLINE.md`) | **APPROVED v1.0** | Approved 2026-06-27 | 35-section structure; approved stack (AD-007) embedded |
| D3 | TRD (`Project_Documents/04_TRD.md`) | **FROZEN v1.0** ✅ | Frozen 2026-06-27 (Gate 2) | Approved technical baseline. §1–§42; six-layer arch, JWT, LLM/embedding separation, FDS, config profiles, prod at-rest encryption. 0 orphans. Foundation for Solution Architecture & Development. |
| D4 | System Architecture Blueprint (`Project_Documents/06_SYSTEM_ARCHITECTURE_BLUEPRINT.md`) | Draft v0.1 | Awaiting approval | Developer implementation guide: overall arch, component diagram, layer interaction, external services, request/monthly/FDS/AI workflows, deployment view (all text diagrams) |
| D5 | AI Agent Architecture Blueprint (`Project_Documents/07_AI_AGENT_ARCHITECTURE.md`) | Draft v0.1 | Awaiting approval | 11 primary agents (12 attributes each), 6 orchestration diagrams, dependency matrix, design-rule compliance, validation, implementation order. Capability-driven; maps to RTM. Guide for `/agents` |
| D6 | Skills Layer Design Blueprint (`Project_Documents/08_SKILLS_LAYER_DESIGN.md`) | Draft v0.1 | Awaiting approval | 15 skills (12 attributes each) + 2 utility skills; skill-to-agent matrix, dependency diagram, implementation order, design-rule compliance. Guide for `/skills` |
| D7 | RAG & Knowledge Base Design Blueprint (`Project_Documents/09_RAG_KNOWLEDGE_BASE_DESIGN.md`) | Draft v0.1 | Awaiting approval | 15 sections + 5 diagrams: source classification, ingestion pipeline, embedding/vector strategy, RPM main ref, live links, retrieval/grounding/citation/fallback, role-based access, update workflow, agent-to-RAG map, audit, validation, implementation order. Guide for `/knowledge`, `/rag` |
| R1 | Requirements Traceability Matrix (`Project_Documents/05_REQUIREMENTS_TRACEABILITY_MATRIX.md`) | **FROZEN v1.0** ✅ | Frozen 2026-06-27 | Approved baseline. 86 requirements × 17 columns; 0 orphans; completeness 98%; bridge BRD→TRD. Expand (not reopen) with TRD/test IDs later. |
| D8 | Traceability Matrix (full, expanded with TRD/test IDs) | Superseded-by R1 (interim) | — | R1 is the BRD→TRD RTM; expand with component/API/test IDs during TRD/test |
| D9 | Development CLAUDE.md | Not Started | — | Only after all above approved |

### Source documents analysed (Discovery)
| # | Source | Analysed? | Notes |
|---|--------|-----------|-------|
| S1 | Prompts_Engg_For_VIbeCoding (1).txt | Registered | Methodology (process, not requirements) |
| S2 | PELAN TAKTIKAL JPN.xlsx | Pending full 7-step | Inspected; sheets: Teras 1&2, 3&4, Reference, SENARAI KPI |
| S3 | PELAN TAKTIKAL PPD (12 files) | Not started | After JPN |
| S4 | PT PPPM 2026-2035 Teras 1–7 (Drive, latest) | Not readable locally | RAG/chatbot knowledge source |
| S5 | project_structure.pptx | Analysed (2026-06-27) | Draft structure: 10 pain points, 10 HMW, 12 draft BR, 12 draft TR, traceability (10 agents), 6 user stories, modules; "14 AI agents"; React+Vite+Tailwind. Treated as DRAFT input pending Q-027. |
