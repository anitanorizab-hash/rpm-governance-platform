# DATABASE ARCHITECTURE BLUEPRINT
### Agentic AI Strategic Governance Platform — RPM 2026–2035
#### Implementation guide for the `/database` module

| Field | Value |
|-------|-------|
| Document | A5 — Database Architecture Blueprint |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Audience | Developers implementing `/database` |
| Baselines (frozen, not modified) | HMW v1.0, BRD v1.0, RTM v1.0, TRD v1.0, A1, A2, A3, A4 |
| Boundary | Conceptual data model — **no SQL, no code**; implements frozen baselines (no new requirements). |

> **Foundations.** SQLite (dev) / PostgreSQL (prod) via SQLAlchemy (TRD §12). **Operational** and
> **Knowledge** are separate planes (BR-017/AD-004) — in prod, knowledge/vector tables live in a separate
> schema. **AI Metadata** is a logging/observability group (advisory outputs + cost/audit), distinct from
> the operational system of record. Append-only **AuditLog** (BR-009/029). Vectors themselves live in the
> vector store (Chroma/pgvector); only **embedding metadata** is modelled here. Retention items marked
> **RUC** await government data-retention policy (NFRQ-013).
> PK = primary key. Owner = accountable business/role for the data.

---

## 1. Database overview & grouping

```
┌──────────── OPERATIONAL DB (system of record) ────────────┐
│ Access: User, Role                                         │
│ Structure: Teras, Strategy/Enabler, Prakarsa, Department   │
│ KPI core: KPI, KPI_Indicator, KPI_Target, PIC, Activity    │
│ Monitoring: KPI_Monthly_Update, Risk_Assessment            │
│ Finance/FDS: Financial_Allocation, Budget_Status(ref),     │
│              OBB_Analysis, Low_Cost_High_Impact_Analysis,   │
│              Strategic_Recommendation                       │
│ Governance: Amendment_Window, KPI_Amendment, Approval,      │
│             Report, Notification, Audit_Log                 │
│ Cross-plane link: Alignment_Score (KPI ↔ RPM source ref)    │
└────────────────────────────────────────────────────────────┘
┌──────────── KNOWLEDGE METADATA (separate plane) ──────────┐
│ Knowledge_Source, Document, Live_Link, Chunk,              │
│ Embedding_Metadata, Citation, Refresh_History              │
│ (vectors stored in Chroma/pgvector; here = metadata only)  │
└────────────────────────────────────────────────────────────┘
┌──────────── AI METADATA (logging / observability) ────────┐
│ Agent_Execution, Skill_Execution, Chat_Session,            │
│ AI_Conversation, AI_Recommendation, AI_Cost_Log,           │
│ Provider_Usage                                             │
└────────────────────────────────────────────────────────────┘
```

---

## 2. Operational Database — Entity Catalogue

| Entity | Purpose | PK | Major fields | Key relationships | Owner | Retention |
|--------|---------|----|--------------|-------------------|-------|-----------|
| **User** | System accounts | user_id | email(@moe domains), name, role_id, scope, active | →Role; ←Audit | Super Admin/IT | Life of system (RUC) |
| **Role** | RBAC roles | role_id | name, permissions | ←User | Super Admin | Life of system |
| **Teras** | 7 strategic pillars (master) | teras_id | number(1–7), name | ←Strategy,KPI | JPN/MOE | Permanent |
| **Strategy_Enabler** | Strategy/Enabler under Teras | strategy_id | teras_id, code, type, name | →Teras; ←Prakarsa | JPN | Permanent |
| **Prakarsa** | Initiative under strategy | prakarsa_id | strategy_id, code, name | →Strategy; ←KPI | JPN | Permanent |
| **Department** | Bahagian/implementing div. (master) | dept_id | name, code | ←KPI,PIC | MOE | Permanent |
| **PIC** | Person-in-charge | pic_id | name, email, sector, dept_id | →Department; ←KPI | Sector/PPD Admin | Life of system |
| **KPI** | Core KPI record | kpi_id | code(`TSx.Sy.Pz.KPIn`), teras_id, prakarsa_id, statement, keberhasilan, dept_id, sector, pic_id, quick_win, year_assigned, status, risk_level | →Teras/Prakarsa/Dept/PIC; ←Indicator/Target/Update/Finance/Risk/Recommendation/Alignment/Amendment | JPN/Sector | 2026–2035 + statutory |
| **KPI_Indicator** | KPI indicator (amendment-controlled) | indicator_id | kpi_id, indicator_text, unit | →KPI | JPN | Versioned via Amendment |
| **KPI_Target** | TOV + target (amendment-controlled) | target_id | kpi_id, year, target_value, tov, tov_type("value"/"KPI Baharu") | →KPI | JPN | Versioned via Amendment |
| **Activity** | Main/supporting activities | activity_id | kpi_id, type(utama/sokongan), description, milestone, nota_pengiraan | →KPI; ←Financial_Allocation | Sector/PIC | 2026–2035 |
| **KPI_Monthly_Update** | In-system monthly entry | update_id | kpi_id, period(YYYY-MM), achievement, finance_status_id, evidence_ref, remarks, submitted_by, submitted_at | →KPI; →Budget_Status | KPI PIC | 2026–2035 + audit |
| **Risk_Assessment** | KPI risk rating | risk_id | kpi_id, period, risk_level, method, computed_at | →KPI | System/Sector | 2026–2035 |
| **Financial_Allocation** | Budget per KPI/activity | allocation_id | kpi_id, activity_id, object_code(OS…), amount, jan…dec, jumlah, frequency, budget_status_id, warrant, expenditure | →KPI/Activity; →Budget_Status | Finance | 2026–2035 + audit |
| **Budget_Status** | Six-value vocabulary (ref) | status_id | code{received, will be received, pending, not received, not required, insufficient} | ←Allocation/Update | Finance | Permanent (ref) |
| **OBB_Analysis** | Value-for-money (FDS) | obb_id | kpi_id, period, vfm_indicator, rationale, computed_at | →KPI | Finance/Exec | 2026–2035 |
| **Low_Cost_High_Impact_Analysis** | LCHI placement (FDS) | lchi_id | kpi_id, activity_id, cost, impact, quadrant, recommendation_ref, computed_at | →KPI/Activity; →Strategic_Recommendation | Finance/Sector | 2026–2035 |
| **Strategic_Recommendation** | Human-reviewed recommendation (FDS/Intervention) | recommendation_id | kpi_id, type(LCHI/Intervention/ResourceOpt/OBB), content, rationale, priority, status, reviewed_by, source_ai_rec_id | →KPI; ↔AI_Recommendation | Sector/Exec | 2026–2035 |
| **Amendment_Window** | Jul/Oct windows (ref) | window_id | year, month(Jul/Oct), open | ←KPI_Amendment | Super Admin | Permanent |
| **KPI_Amendment** | Amendment history (BR-008) | amendment_id | kpi_id, field, old_value, new_value, window_id, actor, reason, timestamp | →KPI/Window | JPN/Admin | Permanent (audit) |
| **Approval** | HITL decisions | approval_id | item_type, item_id, decision(approve/reject), actor, decided_at, comment | polymorphic →Report/Notification/Recommendation | Exec/Admin | Permanent (audit) |
| **Report** | Monthly reports | report_id | period, type, status(draft/approved), generated_by, approved_by, approved_at, archive_ref | ←Approval | JPN/Exec | 2026–2035 + statutory |
| **Notification** | Reminders/alerts/emails | notification_id | type, recipient, content_ref, status(draft/approved/sent/failed), approved_by, sent_at, retry_count | ←Approval | Admin/System | RUC (e.g. 24m) |
| **Audit_Log** | Append-only audit trail | audit_id | entity_type, entity_id, action, actor, before, after, reason, timestamp | polymorphic (all) | Internal Audit | Permanent (full horizon) |
| **Alignment_Score** | KPI↔RPM alignment (cross-plane ref) | alignment_id | kpi_id, rpm_source_id(→Knowledge), strength, computed_at | →KPI; →Knowledge_Source | JPN/Exec | 2026–2035 |

---

## 3. Knowledge Metadata — Entity Catalogue (separate plane)

| Entity | Purpose | PK | Major fields | Key relationships | Owner | Retention |
|--------|---------|----|--------------|-------------------|-------|-----------|
| **Knowledge_Source** | A knowledge item (doc or link) | source_id | type(static/live), title, category, reliability(official/trusted/unverified), status, validated_by, created_at | ←Document/Live_Link/Chunk | Admin | Life of system (RUC) |
| **Document** | Uploaded file metadata | document_id | source_id, filename, format(PDF/DOCX/TXT/MD), size, uploaded_by, uploaded_at | →Knowledge_Source; ←Chunk | Admin | Life of system |
| **Live_Link** | Registered URL | link_id | source_id, url, last_checked, refresh_schedule, status(active/unreachable) | →Knowledge_Source; ←Refresh_History | Admin | Life of system |
| **Chunk** | Text chunk for retrieval | chunk_id | source_id, document_id?, text, position, metadata | →Source/Document; ←Embedding_Metadata/Citation | System | Until source deleted |
| **Embedding_Metadata** | Embedding bookkeeping (vector in store) | embedding_id | chunk_id, model, dimensions, vector_ref(store id), created_at | →Chunk | System | Until re-embed/delete |
| **Citation** | Source used in an answer | citation_id | conversation_id/answer_ref, chunk_id, source_id, used_at | →Chunk/Source; →AI_Conversation | System | With conversation (RUC) |
| **Refresh_History** | Live-link check log | refresh_id | link_id, checked_at, status, changed(bool) | →Live_Link | System | RUC (e.g. 24m) |

> Vectors are stored in **Chroma (dev) / pgvector (prod, separate schema)**; this group holds **metadata only**.
> **No operational KPI data here** (plane separation). Pelan Taktikal is **never** a Knowledge_Source.

---

## 4. AI Metadata — Entity Catalogue (logging / observability)

| Entity | Purpose | PK | Major fields | Key relationships | Owner | Retention |
|--------|---------|----|--------------|-------------------|-------|-----------|
| **Agent_Execution** | One agent run | exec_id | agent_name, trigger, inputs_ref, outputs_ref, status, started_at, ended_at | ←Skill_Execution/AI_Cost_Log | System/IT | RUC (e.g. 12–24m) |
| **Skill_Execution** | One skill invocation | skill_exec_id | skill_name, version, agent_exec_id, inputs_ref, outputs_ref, timestamp | →Agent_Execution | System/IT | RUC |
| **Chat_Session** | A chatbot session | session_id | user_id, started_at, ended_at | →User; ←AI_Conversation | System | RUC (e.g. 12m) |
| **AI_Conversation** | A message turn (Q/A) | conversation_id | session_id, user_id, question, answer_ref, grounded(bool), fallback(bool), created_at | →Chat_Session; ←Citation | System | RUC |
| **AI_Recommendation** | Raw AI-generated draft/log | ai_rec_id | type, content, rationale, linked_entity, provider, model, status(draft), created_at | ↔Strategic_Recommendation (operational) | System | RUC |
| **AI_Cost_Log** | Per-call cost/tokens | cost_id | agent_exec_id, provider, model, tokens_in, tokens_out, cost, latency, timestamp | →Agent_Execution | IT/Finance | RUC (e.g. 24m) |
| **Provider_Usage** | Aggregate usage | usage_id | provider, mode(dev/prod), period, calls, tokens, cost | — | IT | RUC |

> **AI_Recommendation vs Strategic_Recommendation (no duplication):** `AI_Recommendation` is the **raw,
> advisory AI output (log)**; `Strategic_Recommendation` (operational) is the **human-reviewed record** that
> may be acted upon. They are linked 1:1/1:0 via `source_ai_rec_id`, with distinct ownership and lifecycle.

---

## 5. Relationship Diagrams (text)

### 5.1 Overall ER (cross-group)
```
[User]→[Role]                         OPERATIONAL                         KNOWLEDGE
   │                                                                       
[Teras]→[Strategy_Enabler]→[Prakarsa]→[KPI]───┬───[KPI_Indicator]          [Knowledge_Source]
[Department]→[PIC]──────────────────────►[KPI]│   [KPI_Target]              ├─[Document]→[Chunk]→[Embedding_Metadata]
                                              ├───[Activity]→[Financial_Allocation]→[Budget_Status]   └─[Live_Link]→[Refresh_History]
                                              ├───[KPI_Monthly_Update]→[Budget_Status]                 [Chunk]←[Citation]
                                              ├───[Risk_Assessment]
                                              ├───[OBB_Analysis] [Low_Cost_High_Impact_Analysis]→[Strategic_Recommendation]
                                              ├───[KPI_Amendment]→[Amendment_Window]
                                              └───[Alignment_Score]──────────────────────────────────►[Knowledge_Source] (cross-plane ref)
[Report]←[Approval]→[Notification]      [Audit_Log] (polymorphic: logs all)
                                                                          AI METADATA
                                [AI_Conversation]→[Citation]               [Agent_Execution]←[Skill_Execution]
                                [Chat_Session]→[AI_Conversation]           [Agent_Execution]←[AI_Cost_Log]
                                [AI_Recommendation]↔[Strategic_Recommendation]   [Provider_Usage]
```

### 5.2 Operational data relationships
```
Teras 1..7 ─< Strategy_Enabler ─< Prakarsa ─< KPI ─< KPI_Indicator
                                              │     ─< KPI_Target
   Department ─< PIC ──assigned──────────────┤     ─< Activity ─< Financial_Allocation >─ Budget_Status
                                              ├─< KPI_Monthly_Update >─ Budget_Status
                                              ├─< Risk_Assessment
                                              ├─< OBB_Analysis
                                              ├─< Low_Cost_High_Impact_Analysis >─ Strategic_Recommendation
                                              └─< KPI_Amendment >─ Amendment_Window
   Report >─ Approval ─< Notification          Audit_Log (append-only; references any entity)
```

### 5.3 Knowledge metadata relationships
```
Knowledge_Source ─┬─< Document ─< Chunk ─< Embedding_Metadata
                  └─< Live_Link ─< Refresh_History
Chunk ─< Citation >─ AI_Conversation        (vectors live in Chroma/pgvector; metadata here)
```

### 5.4 AI metadata relationships
```
Chat_Session ─< AI_Conversation ─< Citation
Agent_Execution ─< Skill_Execution
Agent_Execution ─< AI_Cost_Log
AI_Recommendation ↔ Strategic_Recommendation (operational)
Provider_Usage (aggregate)
```

---

## 6. Validation

| Check | Result |
|-------|--------|
| No duplicated entities? | ✅ AI_Recommendation (log) vs Strategic_Recommendation (operational) explicitly distinguished; Budget_Status is a reference table, not duplicated as a field+entity. |
| Proper normalization? | ✅ 3NF-oriented: reference tables (Teras, Department, Budget_Status, Amendment_Window); indicators/targets separated from KPI for amendment history; no repeating groups (monthly values modelled per Financial_Allocation columns Jan–Dec as defined fields, consistent with source). |
| Traceable to TRD/RTM? | ✅ entities map to TRD §13 + RTM DB column (KPI, KPI_Monthly_Update, Financial_Allocation, Audit_Log, Knowledge_Source, etc.). |
| Supports Teras 1–7? | ✅ Teras master (1–7) → Strategy → Prakarsa → KPI; dashboard roll-ups by teras_id. |
| Supports Financial Decision Support? | ✅ Financial_Allocation, Budget_Status, OBB_Analysis, Low_Cost_High_Impact_Analysis, Strategic_Recommendation. |
| Supports Human-in-the-Loop? | ✅ Approval (polymorphic), draft/approved statuses on Report/Notification/Recommendation, Audit_Log. |
| Supports RAG? | ✅ Knowledge_Source/Document/Live_Link/Chunk/Embedding_Metadata/Citation/Refresh_History; vectors in store. |
| Plane separation? | ✅ Operational vs Knowledge groups; prod separate schema; Pelan Taktikal operational-only. |
| No new requirements? | ✅ implements frozen baselines only. |

---

## 7. Suggested Implementation Order (`/database`)

1. **Reference/master:** Role, Teras, Strategy_Enabler, Prakarsa, Department, Budget_Status, Amendment_Window.
2. **Access:** User (→Role).
3. **KPI core:** PIC, KPI, KPI_Indicator, KPI_Target, Activity.
4. **Monitoring:** KPI_Monthly_Update, Risk_Assessment.
5. **Finance/FDS:** Financial_Allocation, OBB_Analysis, Low_Cost_High_Impact_Analysis, Strategic_Recommendation.
6. **Governance:** Audit_Log (early — many write to it), KPI_Amendment, Approval, Report, Notification.
7. **Cross-plane:** Alignment_Score.
8. **Knowledge metadata:** Knowledge_Source, Document, Live_Link, Chunk, Embedding_Metadata, Citation, Refresh_History.
9. **AI metadata:** Agent_Execution, Skill_Execution, Chat_Session, AI_Conversation, AI_Recommendation, AI_Cost_Log, Provider_Usage.
> Use SQLAlchemy models + migrations (Alembic); build SQLite (dev) first, validate on PostgreSQL (+pgvector) early; knowledge/vector tables in a separate schema in prod. Test each group before the next (TR-006).

---

## Final Output (summary)
1. **Complete Database Blueprint** — §1–§7.
2. **Entity Catalogue** — §2 (Operational, 24), §3 (Knowledge, 7), §4 (AI, 7) = **38 entities**, each with Purpose/PK/Fields/Relationships/Owner/Retention.
3. **Relationship Diagrams** — overall ER (§5.1) + operational (§5.2) + knowledge (§5.3) + AI (§5.4).
4. **Implementation order** — §7.

> Retention items marked **RUC** await the government data-retention/classification policy (NFRQ-013/RUC-02).

---
*End of Database Architecture Blueprint v0.1 — DRAFT. No SQL, no code. Frozen baselines unmodified. Awaiting approval.*
