# RAG & KNOWLEDGE BASE DESIGN BLUEPRINT
### Agentic AI Strategic Governance Platform — RPM 2026–2035
#### Implementation guide for `/knowledge`, `/rag`, and document-processing

| Field | Value |
|-------|-------|
| Document | A4 — RAG & Knowledge Base Design Blueprint |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Audience | Developers implementing `/knowledge`, `/rag`, document-processing |
| Baselines (frozen, not modified) | HMW v1.0, BRD v1.0, RTM v1.0, TRD v1.0, A1, A2, A3 |
| Boundary | Architecture only — **no code**; implements frozen baselines (no new requirements). |

> **Non-negotiables.** Operational data and Knowledge data are **separate planes** (BR-017/AD-004).
> **Pelan Taktikal JPN/PPD are operational input only** (BR-001/018) — never RAG sources. RPM 2026–2035 is
> the **main reference** (BR-012). LLM and embedding providers are **independent** (TRD §17.2). Answers are
> **source-cited** (BR-025); inaccessible source → clear message, never guess (BR-026); no grounding → the
> **fixed fallback string** (BR-027). Live links are **admin-validated** (BR-024). All AI knowledge activity
> is **logged** (BR-029).

---

## 1. Knowledge Architecture Overview

The Knowledge Layer (L4) is the platform's **grounding engine**. It ingests reference material into a
vector-searchable knowledge base and serves **cited context** to AI agents so their output is grounded in
authoritative sources rather than model memory. It powers the **KPI Chatbot**, **Knowledge Alignment Agent**,
**Executive Copilot**, **KPI→RPM mapping**, **AI summaries**, and **report narrative context**. It is
strictly separate from the operational database and **never** stores operational KPI records.

```
[Knowledge sources] → [Ingestion pipeline] → [Vector store + metadata] → [Retrieval+Citation]
        → consumed by: Chatbot · Knowledge Alignment · Executive Copilot · Report · (KPI Analysis context)
```

---

## 2. Knowledge Source Classification

| Class | Sources | Plane | Used for | Ingested to RAG? |
|-------|---------|-------|----------|------------------|
| **Operational input (NOT knowledge)** | Pelan Taktikal JPN, Pelan Taktikal PPD (.xlsx) | **Operational** | KPI DB, updates, dashboard, reports, audit | ❌ No (import-once → DB) |
| **Main reference** | **RPM 2026–2035** | Knowledge | KPI↔RPM mapping, grounding, alignment | ✅ Yes (primary) |
| **Uploaded documents** | PDF, DOCX, TXT, MD | Knowledge | chatbot, copilot, explanations | ✅ Yes |
| **Supporting knowledge** | Guidelines, circulars, meeting notes, policy docs | Knowledge | context, mapping, summaries | ✅ Yes |
| **Live knowledge links** | Official URLs, updated reference links, shared live docs (accessible) | Knowledge | current info; chatbot/copilot | ✅ Yes (admin-validated) |

> **Hard rule:** Pelan Taktikal is **operational input only**; everything else above (RPM, docs, links) is a
> **RAG knowledge source**. The two never cross planes.

### 2.1 Classification diagram (text)
```
                         ┌──────────────── DATA ────────────────┐
                         ▼                                       ▼
            OPERATIONAL PLANE (DB)                     KNOWLEDGE PLANE (RAG)
            ───────────────────────                   ───────────────────────
            Pelan Taktikal JPN/PPD  ──import-once──►   (NOT ingested as knowledge)
            KPI · MonthlyUpdate · Finance · Audit      RPM 2026–2035 (MAIN reference)
                                                       Uploaded docs (PDF/DOCX/TXT/MD)
                                                       Guidelines · Circulars · Notes · Policy
                                                       Live links (admin-validated)
```

---

## 3. Document Ingestion Pipeline

```
[Upload file]  /  [Register link]
        ▼
[Validate]  type/size (files) · admin validation + reachability (links) · classify source
        ▼
[Extract Text]  PDF/DOCX/TXT/MD parsers · link content fetch (clean HTML→text)
        ▼
[Chunk]  semantic/size-based chunks with overlap · keep source + position metadata
        ▼
[Embed]  Provider Adapter embedding() (independent of LLM) — §4
        ▼
[Store]  Vector store (Chroma dev / pgvector prod) + KnowledgeSource/Chunk metadata
        ▼
[Index]  vector index (+ keyword index for fallback)
        ▼
[Retrieve]  top-k by query (vector or keyword) → cited context to agents
```
- **Idempotent:** re-ingesting the same source replaces its chunks (no duplicates).
- **Operational exclusion:** the pipeline rejects Pelan Taktikal/operational files (routed to ImportService instead).
- **Metadata captured per chunk:** source id, title, type, category, url (if link), last_checked, position, reliability tag.

---

## 4. Embedding Strategy

**LLM provider and embedding provider are independent** (TRD §17.2; Groq has no embeddings API).
| Environment | LLM (`chat()`) | Embeddings (`embedding()`) | Vector |
|-------------|----------------|-----------------------------|--------|
| Development | **Groq** | **Local Sentence Transformer** or **OpenAI Embeddings** (config) | Chroma / **keyword fallback** |
| Production | **OpenAI or Anthropic** | **OpenAI Embeddings** (or approved provider) | pgvector |
- **V1 fallback:** if vector search isn't ready, **keyword search** serves retrieval (TR-012); enable embeddings later, no architecture change.
- **Consistency:** one embedding model per index; **re-embed on model change**; embeddings refreshed on source change.
- **Batching/cost:** batch embed at ingestion; cache query embeddings where useful.

---

## 5. Vector Store Strategy

- **Development:** **Chroma** (standalone) — easy local setup; or keyword fallback.
- **Production:** **pgvector** inside PostgreSQL — single managed store, in a **separate schema** from
  operational tables (preserves plane separation).
- **Metadata filtering:** retrieval can filter by source type/category/reliability/recency.
- **Source tracking:** every chunk links to its `KnowledgeSource` (for citation + refresh + deletion).
- **Index hygiene:** rebuild/refresh on source add/update/delete; orphan chunks removed with their source.

---

## 6. RPM 2026–2035 as Main Reference

RPM 2026–2035 is the **primary policy reference** and is always present in the corpus (BR-012). It is the
authority for **KPI↔RPM alignment** (S8/Knowledge Alignment Agent) and the preferred grounding source for
policy questions. Retrieval **prioritises RPM** for alignment/policy queries (via metadata weighting), while
still drawing on supporting docs and live links for breadth. RPM chunks carry a **high reliability tag**.

---

## 7. Live Link Handling

```
[Admin registers URL] → URL registration (title, url, category)
        ▼
[Admin validation]  approve/reject; prefer official/trusted (BR-024)
        ▼
[Reachability check] fetch → if OK: extract→chunk→embed→store ; record last_checked
        ▼
[Refresh schedule]  periodic re-fetch (configurable) → re-ingest if changed (idempotent)
        ▼
[Access failure]  mark unreachable; show clear message at query time; never guess (BR-026)
        ▼
[Reliability tagging]  official / trusted / unverified — influences retrieval weighting & display
```
- **Stored per link:** title, URL, category, **last_checked date**, validated_by, status (active/unreachable), reliability.
- Only **admin-validated** links are used by the chatbot/copilot.

---

## 8. Retrieval and Grounding

```
[Query] → embed query (or keyword terms if fallback)
        ▼
[Retrieve top-k] from vector store (filter by metadata; weight RPM for policy/alignment)
        ▼
[Assemble context] selected chunks + source metadata
        ▼
[Ground] pass cited context to LLM via Provider Adapter chat()
        ▼
[Answer] grounded, with citations (S10) — or fixed fallback if no relevant context
```
- **Grounding order (chatbot, BR-013/AIR-070):** KPI DB (role-scoped) → monthly updates → uploaded docs → RPM → live links.
- Retrieval is **read-only** on the knowledge plane; operational data is fetched via services (role-scoped), never mixed into the vector store.

---

## 9. Citation and Source Display

- Every grounded answer **shows the source(s) used** (title + type; URL for links; section/page where available) — S10 Citation skill enforces this (BR-025).
- Operational figures cited as "KPI data (system of record)"; knowledge claims cited to their document/link.
- UI displays citations beneath the answer; clicking a link source opens the registered URL (if accessible).

---

## 10. Fallback Behaviour

- If retrieval yields no relevant grounding (and operational data lacks the answer), the chatbot returns the
  **exact fixed string** (BR-027): **"I cannot find this information in the available KPI data or knowledge sources."**
- If a specific source is **inaccessible**, the system shows a **clear message** (e.g. "source X is currently
  unavailable") and never fabricates content (BR-026).

---

## 11. Role-Based Knowledge Access

- **Knowledge documents** (RPM, guidelines, etc.) are generally readable by authenticated users.
- **Operational KPI data surfaced via the chatbot is role-scoped** — a user only sees KPI data their role
  permits (PIC=own; PPD/Sector=their scope; JPN/Exec=wider) per RBAC (BR-003/031/032).
- The Chatbot Agent enforces scope **before** retrieval/answer assembly; citations never leak out-of-scope data.
- Admin-only knowledge operations (link management, reprocessing, deletion) are RBAC-restricted.

---

## 12. Knowledge Update Workflow (admin)

```
[Admin] ── add ──► upload doc / register link → validate → ingest (pipeline §3)
        ── update ─► replace doc / re-fetch link → re-ingest (idempotent; re-embed)
        ── reprocess ─► force re-chunk/re-embed (e.g. after model/config change)
        ── delete ─► remove source + its chunks/embeddings (index cleaned)
   All operations RBAC-restricted (admin) and logged (§14).
```

---

## 13. RAG Use by Agents (Agent-to-RAG mapping)

| Agent | Uses RAG? | How |
|-------|:--------:|-----|
| **KPI Chatbot Agent** | ✅ Core | grounding order; cited answers; fallback |
| **Knowledge Alignment Agent** | ✅ Core | retrieve RPM context → KPI↔RPM mapping + alignment strength |
| **Executive Copilot Agent** | ✅ | ground executive insight in RPM/guidelines/links (cited) |
| **Report Generation Agent** | ◑ Optional | narrative/policy context for report sections (cited) |
| **KPI Analysis Agent** | ◑ Where relevant | optional policy context for interpretation (not for status calc) |
| FDS / Strategic Recommendation | ◑ Optional | RPM-aligned options for recommendations (cited) |
> Skills used: **S9 RAG Retrieval** + **S10 Citation/Grounding** (and **S8 RPM Alignment** for mapping).

---

## 14. Knowledge Audit and Logging

Logged events (BR-029) → AuditService / logs:
| Event | Logged data |
|-------|-------------|
| Upload | source id, type, uploader, timestamp |
| Link refresh | link id, last_checked, status (ok/unreachable), changed? |
| Retrieval | query, top-k source ids, mode (vector/keyword), timestamp |
| Chatbot answer generation | question, sources cited, provider/model, timestamp |
| Failed retrieval | query, reason (no grounding / source inaccessible), fallback emitted |
| Citation used | answer id ↔ source ids |
- Admin knowledge operations (add/update/reprocess/delete) are audited with actor + before/after.

---

## 15. RAG Validation (testing)

| Test | Method | Pass criteria |
|------|--------|---------------|
| **Retrieval accuracy** | curated query→expected-source set | relevant chunks in top-k |
| **Citation accuracy** | check answers cite the sources actually used | citations match retrieved sources (S10) |
| **Fallback behaviour** | query with no corpus support | returns exact fixed fallback string (BR-027) |
| **Role-based access** | query KPI data as different roles | only in-scope data returned; no leakage |
| **Answer grounding** | claims vs sources | no uncited/fabricated claims; inaccessible→clear message |
| **Live link** | unreachable/refresh | clear message; last_checked updated; idempotent re-ingest |
- Tests align with TRD §38 (AI Response Validation, RAG Validation) and trace to RTM (AIRQ-003/008/009, NFRQ-004).

---

## Diagrams (consolidated)

**D1 — Knowledge source classification:** see §2.1.
**D2 — RAG pipeline:** see §3.
**D3 — Live link refresh workflow:** see §7.

**D4 — Chatbot answer generation**
```
[User question + role] → Chatbot Agent
   → enforce role scope → grounding order (KPI DB → updates → docs → RPM → links)
   → S9 retrieve (vector/keyword) → S10 cite
   → Provider Adapter chat() → grounded answer + citations
   → if none: fixed fallback ; if source down: clear message
   → log Q&A + sources (S13/audit)
```

**D5 — KPI-to-RPM alignment flow**
```
[KPI statement/indicator] → Knowledge Alignment Agent
   → S9 retrieve RPM context (RPM weighted, main reference)
   → S8 RPM Alignment (map + strength score) → S10 cite RPM source
   → AlignmentScore (advisory, display on dashboard DSH-12)
   → log (audit)
```

---

## FINAL OUTPUT

1. **Complete RAG & Knowledge Base Blueprint** — §1–§15 above.
2. **Knowledge source classification table** — §2 (operational-input vs RPM-main vs uploaded vs supporting vs live links).
3. **RAG pipeline diagram** — §3 (Upload/Link → Validate → Extract → Chunk → Embed → Store → Index → Retrieve).
4. **Agent-to-RAG mapping** — §13 (Chatbot/Alignment/Copilot core; Report/KPI-Analysis/FDS optional).
5. **Implementation order** (`/knowledge`, `/rag`, document-processing):
   1. **KnowledgeSource/Chunk schema + metadata** (knowledge plane).
   2. **Text extraction** (PDF/DOCX/TXT/MD) + ingestion pipeline scaffold.
   3. **Keyword retrieval (V1 fallback)** — get grounding working without embeddings.
   4. **Embedding via Provider Adapter** + **Chroma (dev)** vector store.
   5. **S9 Retrieval + S10 Citation/Grounding** integration.
   6. **Live link registry + admin validation + refresh** (§7/§12).
   7. **Chatbot grounding order + role scoping + fallback** (§8/§10/§11).
   8. **KPI↔RPM alignment** (S8) using RPM-weighted retrieval (§6).
   9. **Copilot/Report RAG context** integration.
   10. **pgvector (prod)** migration + **RAG validation tests** (§15).

---
*End of RAG & Knowledge Base Design Blueprint v0.1 — DRAFT. No code. Frozen baselines unmodified. Awaiting approval.*
