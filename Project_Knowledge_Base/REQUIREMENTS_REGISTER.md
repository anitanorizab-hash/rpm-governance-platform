# REQUIREMENTS_REGISTER.md

> **Single Source of Truth — Master Requirements List**
> Status: `LIVING DOCUMENT` · Version: 0.1 (DRAFT) · Last updated: 2026-06-27

---

## Purpose
A master list of **all identified requirements** (business, functional, non-functional), each with a
stable ID, so the BRD/TRD draw from one authoritative inventory and every requirement is traceable to
a source rule and forward to a test case.

## When updated
- As requirements are elicited from documents and confirmed.
- Status changes as items move Proposed → Confirmed → In BRD → In TRD → Implemented → Verified.

## Relationship with other documents
- **Draws from:** `BUSINESS_RULES.md`, `TECHNICAL_RULES.md`, `AI_RULES.md`, source documents.
- **Feeds:** BRD, TRD, `TRACEABILITY_REGISTER.md`.

## ID conventions
- Business requirement: `BRQ-NNN`
- Functional requirement: `FRQ-NNN`
- Non-functional requirement: `NFRQ-NNN`
- AI requirement: `AIRQ-NNN`

## Columns
`ID | Requirement | Type | Source rule(s) | Priority | Status`

---

### Business requirements (seed)
| ID | Requirement | Source | Priority | Status |
|----|-------------|--------|----------|--------|
| BRQ-001 | Provide KPI monitoring across JPN/PPD (and school as applicable). | Context | High | Proposed |
| BRQ-002 | Enforce monthly in-system KPI updates by PICs. | BR-002 | High | Proposed |
| BRQ-003 | Enforce July/October-only amendment of KPI statement/indicator/target. | BR-008 | High | Proposed |
| BRQ-004 | Maintain a complete audit trail of amendments. | BR-009 | High | Proposed |
| BRQ-005 | Track allocation status per the six-value finance vocabulary. | BR-010 | High | Proposed |

### Functional requirements (seed)
| ID | Requirement | Source | Priority | Status |
|----|-------------|--------|----------|--------|
| FRQ-001 | Import Pelan Taktikal from Excel (import-once). | BR-001, TR-007 | High | Proposed |
| FRQ-002 | Detect & warn on incomplete information. | BR-005, BR-006 | High | Proposed |
| FRQ-003 | Send reminders to PICs (incomplete data + monthly updates). | BR-007 | High | Proposed |
| FRQ-004 | Generate monthly reports. | BR-014 | High | Proposed |
| FRQ-005 | Provide KPI chatbot. | BR-013 | Medium | Proposed |
| FRQ-006 | Provide a **Teras-centric main dashboard** summarising/mapping all KPIs by Teras 1–7. | BR-020 | High | Proposed |
| FRQ-007 | Dashboard per-Teras metrics: total KPIs, count, achievement, risk, completion, missing info, monthly submission, budget status, Low Cost High Impact summary, RPM alignment strength. | BR-021 | High | Proposed |
| FRQ-008 | Dashboard KPI mapping table: KPI → Teras → PIC → Sector → Status → Risk → Budget Status. | BR-021 | High | Proposed |
| FRQ-009 | Dashboard charts (bar/stacked/heatmap by Teras); cards/tables acceptable for V1, charts later. | BR-021, D3A §3 | Medium | Proposed |
| FRQ-010 | Executive summary section for management on main page. | BR-021 | High | Proposed |
| FRQ-011 | Separate ingestion: operational import-once → DB; knowledge docs/links → RAG pipeline. | BR-017, BR-019 | High | Proposed |

### Non-functional requirements (seed)
| ID | Requirement | Source | Priority | Status |
|----|-------------|--------|----------|--------|
| NFRQ-001 | Restrict login to MOE domains. | BR-003, TR-008 | High | Proposed |
| NFRQ-002 | Auditability/traceability of changes. | BR-009 | High | Proposed |
| NFRQ-003 | Configurable LLM provider without code change. | TR-003 | High | Proposed |

### AI requirements (seed)
| ID | Requirement | Source | Priority | Status |
|----|-------------|--------|----------|--------|
| AIRQ-001 | RAG grounded on RPM 2026–2035. | BR-012, AIR-010 | High | Proposed |
| AIRQ-002 | Budget Intelligence via Low Cost High Impact Matrix. | BR-011, AIR-031 | High | Proposed |
| AIRQ-003 | Human-in-the-loop gate before formal action/report/email. | BR-015, AIR-001 | High | Proposed |
| AIRQ-004 | Main-page AI summary answering the 7 management questions, grounded on DB + updates + budget + RPM + knowledge. | BR-022, AIR-060/061 | High | Proposed |
| AIRQ-005 | Knowledge Alignment Agent (KPI ↔ RPM alignment, mapping, alignment strength). | AIR-033 | Medium | Proposed |
| AIRQ-006 | Executive Copilot for management decision support. | AIR-034 | Medium | Proposed |
| AIRQ-007 | RAG supports static + live/link sources; link registry with title/URL/category/last-checked + admin refresh. | BR-023, BR-024, AIR-014/015 | High | Proposed |
| AIRQ-008 | Chatbot grounds on DB + monthly updates + uploaded docs + RPM + live links; cites sources used. | BR-025, AIR-070 | High | Proposed |
| AIRQ-009 | Inaccessible-source message + fixed fallback string; never fabricate. | BR-026, BR-027, AIR-017/071 | High | Proposed |

> Register is intentionally seeded, not complete. Expanded during full document analysis and BRD.
