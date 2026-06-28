# AI_RULES.md

> **Single Source of Truth — AI-Specific Rules**
> Status: `LIVING DOCUMENT` · Version: 0.1 (DRAFT) · Last updated: 2026-06-27

---

## Purpose
Records the rules that govern **AI behaviour**: human review, RAG, skills, multi-agent design,
provider switching and prompt engineering. These bind the AI Agent Architecture, Skills Layer and
RAG/Knowledge Base designs.

## When updated
- When an AI behaviour rule, guardrail or evaluation standard is confirmed.

## Relationship with other documents
- **Feeds:** AI Agent Architecture, Skills Layer Design, RAG & Knowledge Base Design.
- **Constrained by:** `BUSINESS_RULES.md` (esp. BR-015 HITL), `TECHNICAL_RULES.md` (provider switching).

## ID convention
`AIR-NNN`.

---

### Human-in-the-loop
| ID | Rule | Status |
|----|------|--------|
| AIR-001 | Human review is **mandatory before** any formal action, report approval, or email send. AI proposes; a human disposes. | Confirmed (BR-015) |
| AIR-002 | No agent may autonomously send email, approve a report, or trigger formal action. | Confirmed (derived) |

### RAG & Knowledge Base
| ID | Rule | Status |
|----|------|--------|
| AIR-010 | RAG uses **RPM 2026–2035 as the main reference document**. | Confirmed (BR-012) |
| AIR-011 | Latest authoritative corpus = "TERKINI 19 DISEMBER 2025" PT PPPM 2026-2035 (Teras 1–7); used as chatbot retrieval source. | Confirmed (user) |
| AIR-012 | Executive/AI answers should be **grounded and traceable** to source (citation standard TBC). | Proposed |
| AIR-013 | Knowledge Data (RPM, guidelines, circulars, notes, supporting docs, **links**) is ingested into RAG; operational data is NOT used as knowledge documents and vice versa. | Confirmed (BR-017/019) |
| AIR-014 | RAG must support **two source types**: Static (uploaded docs, manual notes) and **Live/Updated** (URLs/links, updated sources). | Confirmed (BR-023, D3B) |
| AIR-015 | Link sources carry metadata (title, URL, category, last-checked) and are **admin-refreshable/reprocessable**; prefer official/trusted sources. | Confirmed (BR-024) |
| AIR-016 | RAG/chatbot answers must **cite the source(s) used**. | Confirmed (BR-025) |
| AIR-017 | If a source/link is inaccessible, return a clear message — **never fabricate**. | Confirmed (BR-026) |

### Chatbot grounding & fallback
| ID | Rule | Status |
|----|------|--------|
| AIR-070 | The chatbot answers using: **KPI database, monthly KPI updates, uploaded knowledge docs, RPM 2026–2035, and live links/updated sources where available**. | Confirmed (D3B) |
| AIR-071 | Mandatory fallback string when info is absent: **"I cannot find this information in the available KPI data or knowledge sources."** | Confirmed (BR-027) |

### Main-page AI summary
| ID | Rule | Status |
|----|------|--------|
| AIR-060 | The main page must generate an **AI summary** answering the 7 management questions (overall KPI status; highest-KPI Teras; highest-risk Teras; most-missing-info Teras; most-budget-issue Teras; KPI needing immediate attention; recommended monthly management focus). | Confirmed (D3A §4) |
| AIR-061 | The AI summary must be grounded on **KPI database + monthly updates + budget status + RPM 2026–2035 + other uploaded knowledge**. | Confirmed (D3A §4) |

### Skills Layer
| ID | Rule | Status |
|----|------|--------|
| AIR-020 | The system must include a **skills layer** of discrete, reusable, testable capabilities. | Confirmed (BR-016) |
| AIR-021 | Skills should be **deterministic and independently testable** where possible (vs. agent orchestration). | Proposed |

### Multi-Agent
| ID | Rule | Status |
|----|------|--------|
| AIR-030 | The system uses **multiple specialised agents** (confirmed: Budget Intelligence Agent + KPI Chatbot). | Confirmed |
| AIR-031 | Budget Intelligence Agent must apply the **Low Cost High Impact Matrix**. | Confirmed (BR-011) |
| AIR-032 | Candidate agents to confirm: Monitoring/Completeness, Notification/Reminder, Intervention, Reporting, Executive Copilot. | Proposed |
| AIR-033 | **Knowledge Alignment Agent** confirmed: aligns KPIs with RPM 2026–2035 and supporting knowledge (KPI mapping, alignment strength, context). | Confirmed (D3A §1B) |
| AIR-034 | **Executive Copilot** confirmed as a management-facing decision-support assistant drawing on operational + knowledge data. | Confirmed (D3A §1B) |

### AI Provider Switching
| ID | Rule | Status |
|----|------|--------|
| AIR-040 | Dev = **Groq**; Prod/golive = **OpenAI or Anthropic** via `config.md`. | Confirmed (TR-001/002) |
| AIR-041 | Provider must be swappable without code change (provider abstraction). | Confirmed (TR-003) |

### Prompt Engineering
| ID | Rule | Status |
|----|------|--------|
| AIR-050 | Project follows a structured prompt-engineering methodology (role assignment → understand → document → audit → freeze → build), per `Prompts_Engg_For_VIbeCoding`. | Confirmed |
| AIR-051 | Prompt/guardrail standards for each agent to be defined in AI Agent Architecture. | Proposed |
