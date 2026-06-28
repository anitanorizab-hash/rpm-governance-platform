# PROJECT_GLOSSARY.md

> **Single Source of Truth — Terms, Abbreviations & Definitions**
> Status: `LIVING DOCUMENT` · Version: 0.1 (DRAFT) · Last updated: 2026-06-27

---

## Purpose
Authoritative definitions for every domain, technical and AI term used in the project, so all
documents and the team use language consistently. Prevents ambiguity in BRD/TRD and traceability.

## When updated
- Whenever a new term appears in an analysed document.
- Whenever a definition is corrected or confirmed by the user.

## Relationship with other documents
- **Referenced by:** every other KB document, BRD, TRD, AI Architecture.
- **Draws from:** source documents (Pelan Taktikal, RPM, prompt guide).

---

## A. Domain & Governance terms
| Term | Status | Definition |
|------|--------|------------|
| RPM | Confirmed (full form TBC) | Rancangan Pendidikan Malaysia 2026–2035 — the national 10-year education roadmap; primary strategic reference. (Note: source files also use **PPPM** — relationship to be confirmed, see gaps.) |
| PPPM | Observed | Pelan Pembangunan Pendidikan Malaysia — appears in file names "PT PPPM 2026-2035". Relationship to "RPM" to be confirmed. |
| Teras Strategik | Confirmed | Strategic Pillar. RPM is organised into **7 Teras** (Teras 1–7). |
| Strategi / Enabler | Observed | Strategy or Enabler under a Teras. |
| Prakarsa | Observed | Initiative under a strategy/enabler. |
| Pelan Taktikal | Confirmed | Tactical Plan — the working plan (per JPN and per PPD) listing KPIs, activities, budget and monthly projections. |
| JPN | Confirmed | Jabatan Pendidikan Negeri — State Education Department. |
| PPD | Confirmed | Pejabat Pendidikan Daerah — District Education Office. |
| KPI | Confirmed | Key Performance Indicator. |
| KOD KPI | Observed | KPI code, e.g. `TS1.S1.P1.KPI2` (Teras.Strategi.Prakarsa.KPI). |
| KPI Baharu | Observed | "New KPI" — a KPI introduced for 2026 with no prior baseline. |
| TOV | Observed | Take-Off Value — baseline value (Pencapaian 2025 / 2025 achievement). |
| Sasaran | Observed | Target (e.g. Sasaran 2026). |
| Keberhasilan | Observed | Outcome / result statement for a KPI. |
| Aktiviti Utama | Observed | Main activity for delivering a KPI. |
| Aktiviti Sokongan | Observed | Supporting activity. |
| Milestone (output) | Observed | Output milestone. |
| Bahagian | Observed | Division/Section (e.g. BPSH, BPK, IPGM) — implementing unit. |
| PIC | Confirmed | Person In Charge — owner accountable for a KPI's data/updates. |
| Sektor / Sector | Confirmed | Organisational sector each KPI is mapped to. |
| Quick Win | Observed | KPI flagged as a quick-win for RPM 2026–2027. |
| AKP | Observed | Appears in Teras 3 KPI ("Pengisian AKP"). Full form to confirm. |
| OS21000 … OS42000 | Observed | Government expenditure object codes (e.g. OS21000 travel/allowance, OS24000 rental, OS29000 professional services, OS42000 domestic grants). Used for budget breakdown. |
| Unjuran | Observed | Projection (monthly projected spend Jan-26 … Dec-26). |

## B. Finance terms
| Term | Status | Definition |
|------|--------|------------|
| Allocation status vocabulary | Confirmed | One of: received / will be received / pending / not received / not required / insufficient. |
| Low Cost High Impact Matrix | Confirmed (mechanics TBC) | Prioritisation matrix to rank KPIs/activities by cost vs. impact. A first-class analysis within Financial Decision Support (not merely a Budget Intelligence sub-feature). |
| Financial Decision Support (FDS) | Confirmed (CL-024) | End-to-end financial decision-support capability broader than Budget Intelligence, comprising: Budget Intelligence (status/funding-gap/risk), Low Cost High Impact Analysis, Intervention Recommendation, and Executive Financial Insight. Advisory + human-reviewed. |

## C. AI & Technical terms
| Term | Status | Definition |
|------|--------|------------|
| RAG | Confirmed | Retrieval-Augmented Generation — grounding AI answers in RPM 2026–2035 corpus. |
| LLM | Confirmed | Large Language Model. |
| Agent | Confirmed | An autonomous AI component that orchestrates/decides within guardrails (proposes, never finally acts). |
| Skill | Confirmed | A discrete, reusable, testable capability invoked by agents. |
| Skills Layer | Confirmed | The collection/registry of skills available to agents. |
| Multi-Agent Architecture | Confirmed | Multiple specialised agents (e.g. Budget Intelligence, Monitoring, Notification, Reporting). |
| Budget Intelligence (Agent) | Confirmed | Agent applying the Low Cost High Impact Matrix to budget/impact data. |
| Executive Copilot | Confirmed | Management-facing decision-support assistant drawing on operational + knowledge data. |
| Knowledge Alignment Agent | Confirmed | Agent that aligns KPIs with RPM 2026–2035 and supporting knowledge (KPI mapping, alignment strength, context). |
| Operational Data | Confirmed | Transactional records stored in the database: Pelan Taktikal JPN/PPD, monthly updates, PIC info, budget status, audit trail, reports. |
| Knowledge Data | Confirmed | Reference documents/links processed into RAG: RPM 2026–2035, guidelines, circulars, notes, supporting docs, links. |
| Static Knowledge Source | Confirmed | Fixed knowledge: RPM PDF, guidelines, circulars, meeting notes, uploaded documents. |
| Live/Updated Knowledge Source | Confirmed | Knowledge from links/online sources that may change: official links, online reference pages, shared updated docs. |
| Link registry | Confirmed | Store of link sources with title, URL, category, last-checked date; admin-refreshable. |
| Source citation | Confirmed | Chatbot must show which source(s) an answer used. |
| Fallback message | Confirmed | Fixed reply when info absent: "I cannot find this information in the available KPI data or knowledge sources." |
| OBB | Observed (confirm) | Outcome-Based Budgeting — "OBB value for money" / "OBB utilisation" analysis (pptx). Relationship to Low Cost High Impact Matrix to confirm (Q-025). |
| Agent Centre | Observed (pptx) | UI/module hosting the AI agents (pptx TR010 references "14 AI agents"). |
| Warrant | Observed (pptx) | Finance term: allocation/warrant/expenditure monitoring (pptx BR005). |
| Modules (pptx) | Observed | Master KPI Records, Dashboard, Agent Centre, Report Archive, Financial Section, Email Engine. |
| Teras-centric dashboard | Confirmed | Main page organised by the 7 Teras with per-Teras summaries, charts, KPI mapping table and AI summary. |
| Human-in-the-loop (HITL) | Confirmed | Mandatory human review before formal action, report approval and email sending. |
| Knowledge Base | Confirmed | Curated corpus (RPM + plans) backing RAG and the chatbot. |
| Provider switching | Confirmed | Dev = Groq; Production/golive = OpenAI or Anthropic, selected via `config.md`. |

## D. Process / methodology terms
| Term | Status | Definition |
|------|--------|------------|
| HMW | Confirmed | How Might We — problem-framing statements produced in Discovery. |
| BRD | Confirmed | Business Requirements Document. |
| TRD | Confirmed | Technical Requirements Document. |
| Freeze / Baseline | Confirmed | Approved, locked version; reopened only via logged change request. |
| Traceability Matrix | Confirmed | Mapping from HMW → BRD → TRD → User Story → Feature → Agent → Skill → API → Frontend → Test. |

> _Terms marked "Observed" are derived from data inspection and await user confirmation._
