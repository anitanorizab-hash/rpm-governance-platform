# API ARCHITECTURE BLUEPRINT
### Agentic AI Strategic Governance Platform — RPM 2026–2035
#### Implementation guide for `/routes`, `/services` (FastAPI backend)

| Field | Value |
|-------|-------|
| Document | A6 — API Architecture Blueprint |
| Version | 0.1 (DRAFT — awaiting approval) |
| Date | 2026-06-27 |
| Status | Draft → (pending) Approval |
| Audience | Developers implementing `/routes`, `/services` |
| Baselines (frozen/approved) | HMW v1.0, BRD v1.0, RTM v1.0, TRD v1.0, A1, A2, A3, A4, A5 |
| Boundary | Architecture only — **no code**; implements frozen baselines (no new requirements). |

> **Global API rules.** All routes under **`/api/v1`**. Protected routes require **JWT** (Bearer); **RBAC**
> enforced server-side on every route (FastAPI dependency). **AI APIs are advisory** — they never approve/
> amend/delete/send official outputs (BR-028/ASM-11); world-affecting actions pass the **HITL approval** API.
> **Reports/notifications send only after human approval** (BR-015/040). **Chatbot** answers are grounded +
> cited, with the fixed fallback (BR-025/027). **Monthly updates** are keyed in-system (BR-002); **Excel** is
> initial import only (BR-001/018). Consistent error envelope `{code,message,details,correlation_id}`. All
> mutations + AI calls **audited** (BR-009/029). Design supports future production deployment.

---

## 1. API Group Catalogue (overview)

| # | API Group | Base path | Primary service | Core role(s) |
|---|-----------|-----------|-----------------|--------------|
| 1 | Auth | `/api/v1/auth` | AuthService | all (login) |
| 2 | User & Role | `/api/v1/admin/users`,`/roles` | AdminService | Super Admin |
| 3 | KPI | `/api/v1/kpis` | KpiService | JPN/Sector/PPD Admin |
| 4 | Initial Import | `/api/v1/import` | ImportService | Super/JPN Admin |
| 5 | Monthly Update | `/api/v1/kpis/{id}/updates` | UpdateService | KPI PIC |
| 6 | Dashboard | `/api/v1/dashboard` | DashboardService | all (scoped) |
| 7 | Financial Decision Support | `/api/v1/fds` | FinanceService | Finance/Exec |
| 8 | AI Agent | `/api/v1/ai` | AgentOrchestrationService | scoped |
| 9 | Skills | `/api/v1/skills` | (internal) SkillRegistry | system/admin |
| 10 | Knowledge / RAG | `/api/v1/knowledge` | KnowledgeService | Admin (write), all (read) |
| 11 | Chatbot | `/api/v1/chatbot` | ChatbotService | all (scoped) |
| 12 | Executive Copilot | `/api/v1/copilot` | CopilotService | Executive |
| 13 | Report | `/api/v1/reports` | ReportService | JPN/Exec |
| 14 | Notification | `/api/v1/notifications` | NotificationService | Admin/JPN |
| 15 | Approval | `/api/v1/approvals` | WorkflowService | Exec/Admin |
| 16 | Audit | `/api/v1/audit` | AuditService | Internal Audit/Admin |
| 17 | Configuration | `/api/v1/admin/config` | AdminConfigService | Super Admin |
| 18 | Health Check | `/api/v1/health` | (infra) | public/none |

---

## 2. API Group Specifications

> Per group: Purpose · Endpoints (method/path/role) · Service · DB entities · Agents/Skills · RTM · Validation · Audit.

### G1 — Auth API
- **Purpose:** authenticate MOE users; issue/refresh JWT.
- **Endpoints:** `POST /auth/login` (all) · `POST /auth/refresh` (token) · `POST /auth/logout` (auth) · `GET /auth/me` (auth).
- **Service:** AuthService. **DB:** User, Role. **RTM:** FRQ-001/002, NFRQ-001.
- **Validation:** email ∈ {@moe.gov.my,@moe-dl.edu.my} (BR-003); valid credentials; token validity.
- **Audit:** login/logout logged.

### G2 — User & Role API
- **Purpose:** manage users, roles, scopes.
- **Endpoints:** `GET/POST /admin/users` · `GET/PUT/DELETE /admin/users/{id}` · `GET/POST /admin/roles` (Super Admin).
- **Service:** AdminService. **DB:** User, Role. **RTM:** FRQ-027, BR-031/032/033.
- **Validation:** unique email; valid role/scope; admin-only.
- **Audit:** user/role changes logged.

### G3 — KPI API
- **Purpose:** manage KPI master records, indicators, targets, PIC assignment.
- **Endpoints:** `GET /kpis` (scoped) · `GET /kpis/{id}` · `POST /kpis` · `PUT /kpis/{id}` · `POST /kpis/{id}/assign-pic` · `PUT /kpis/{id}/indicator` · `PUT /kpis/{id}/target` · `GET /kpis/{id}/completeness`.
- **Service:** KpiService, ValidationService. **DB:** KPI, KPI_Indicator, KPI_Target, PIC, Teras, Prakarsa. **Agents/Skills:** Validation Agent / S2. **RTM:** FRQ-004/005/006/010.
- **Validation:** PIC name/sector/email (BR-004); **indicator/target edits only in Jul/Oct** (BR-008) → else 409; completeness rules.
- **Audit:** create/update + amendments (before/after) logged.

### G4 — Initial Import API
- **Purpose:** one-time Excel import of Pelan Taktikal JPN/PPD.
- **Endpoints:** `POST /import/pelan-taktikal` (multipart) · `GET /import/{batch_id}/report` (Super/JPN Admin).
- **Service:** ImportService. **DB:** KPI, Teras, Strategy, Prakarsa, Activity, PIC, Financial_Allocation. **Agents/Skills:** Data Integration (ImportService) + `excel_parsing`, Validation/S2. **RTM:** FRQ-003, INTQ-001, DATQ-001.
- **Validation:** file type/size; reject non-operational/knowledge files; **import-once** (subsequent edits in-system, BR-002/018).
- **Audit:** import batch logged (rows imported, warnings).

### G5 — Monthly Update API
- **Purpose:** in-system monthly KPI updates by PIC.
- **Endpoints:** `POST /kpis/{id}/updates` · `GET /kpis/{id}/updates?period=` · `PUT /kpis/{id}/updates/{updateId}` (KPI PIC, own).
- **Service:** UpdateService, ValidationService. **DB:** KPI_Monthly_Update, Evidence, Budget_Status. **Agents/Skills:** Validation/S2, KPI Analysis/S1 (post-save), Risk/S3. **RTM:** FRQ-007.
- **Validation:** achievement/finance_status (six-value); completeness; period rules; **no monthly Excel upload**.
- **Audit:** every save logged (who/what/when).

### G6 — Dashboard API
- **Purpose:** Teras 1–7 summaries + mapping + AI summary.
- **Endpoints:** `GET /dashboard/teras` · `GET /dashboard/teras/{n}` · `GET /dashboard/summary` (AI) · `GET /dashboard/high-risk` (all, scoped).
- **Service:** DashboardService. **DB:** KPI, KPI_Monthly_Update, Risk_Assessment, Financial_Allocation, Alignment_Score. **Agents/Skills:** AI Summary (Copilot) / S14, S1. **RTM:** FRQ-011/012/025, REPQ-003/006, BR-020/021/022.
- **Validation:** role-scoped; all 7 Teras represented (RUC-03 partial allowed).
- **Audit:** read access optionally logged; AI summary generation logged.

### G7 — Financial Decision Support API
- **Purpose:** budget status, Low Cost High Impact, OBB, recommendations (advisory).
- **Endpoints:** `GET /fds/budget-status` · `POST /fds/analyze` · `GET /fds/low-cost-high-impact` · `GET /fds/obb` · `GET /fds/recommendations` (Finance/Exec).
- **Service:** FinanceService. **DB:** Financial_Allocation, Budget_Status, OBB_Analysis, Low_Cost_High_Impact_Analysis, Strategic_Recommendation. **Agents/Skills:** FDS Agent / S4,S5,S6,S7,S15. **RTM:** FRQ-014/028/029/030, AIRQ-006, BR-046.
- **Validation:** six-value status; **advisory only** (no implementation without HITL).
- **Audit:** analyses + recommendations logged.

### G8 — AI Agent API
- **Purpose:** invoke advisory agents (analysis/risk/intervention/alignment).
- **Endpoints:** `POST /ai/analyze` · `POST /ai/risk` · `POST /ai/recommend` · `POST /ai/align` (scoped).
- **Service:** AgentOrchestrationService. **DB:** KPI, Risk_Assessment, AI_Recommendation, Agent_Execution. **Agents/Skills:** KPI Analysis, Risk, Strategic Recommendation, Knowledge Alignment + skills. **RTM:** AIRQ-001/004/005/007.
- **Validation:** **advisory only** — never approves/amends/sends (BR-028); outputs are drafts/logs.
- **Audit:** Agent_Execution + AI output logged (BR-029).

### G9 — Skills API (internal)
- **Purpose:** expose skill registry/metadata (mostly internal; admin/system).
- **Endpoints:** `GET /skills` (list/version) · `POST /skills/{name}/run` (system/internal, guarded).
- **Service:** SkillRegistry (internal). **DB:** Skill_Execution. **Agents/Skills:** S1–S15. **RTM:** AIRQ-002, BR-042.
- **Validation:** skills compute only; never write official records (rule 5); internal/guarded.
- **Audit:** Skill_Execution logged.

### G10 — Knowledge / RAG API
- **Purpose:** manage knowledge sources + retrieval.
- **Endpoints:** `POST /knowledge/documents` (upload) · `POST /knowledge/links` (register) · `POST /knowledge/links/{id}/validate` · `POST /knowledge/{id}/reprocess` · `DELETE /knowledge/{id}` · `POST /knowledge/retrieve` (internal) — write=Admin, read=all.
- **Service:** KnowledgeService. **DB:** Knowledge_Source, Document, Live_Link, Chunk, Embedding_Metadata, Refresh_History. **Agents/Skills:** S9 RAG, S10 Citation, `link_fetch_refresh`. **RTM:** FRQ-020/021/022, AIRQ-003, INTQ-002.
- **Validation:** file types (PDF/DOCX/TXT/MD); **links admin-validated** (BR-024); reject operational files.
- **Audit:** uploads/refresh/reprocess/delete + retrieval logged.

### G11 — Chatbot API
- **Purpose:** grounded, cited Q&A.
- **Endpoints:** `POST /chatbot/query` · `GET /chatbot/sessions/{id}` (all, scoped).
- **Service:** ChatbotService. **DB:** Chat_Session, AI_Conversation, Citation. **Agents/Skills:** KPI Chatbot Agent + S9/S10/S15. **RTM:** FRQ-013, AIRQ-009, BR-013/025/027.
- **Validation:** **role-scoped** KPI data; cite sources; fixed fallback if none; clear message if source down.
- **Audit:** Q&A + sources logged.

### G12 — Executive Copilot API
- **Purpose:** synthesised executive insight (advisory).
- **Endpoints:** `POST /copilot/insight` · `GET /copilot/sessions/{id}` (Executive).
- **Service:** CopilotService. **DB:** AI_Conversation, AI_Recommendation, Citation. **Agents/Skills:** Executive Copilot + S1/S3/S4/S8/S9/S10/S14/S15. **RTM:** FRQ-023/030, AIRQ-008.
- **Validation:** advisory; cited; final approval with officers (ASM-11).
- **Audit:** insight + sources logged.

### G13 — Report API
- **Purpose:** generate, review, issue monthly reports (HITL).
- **Endpoints:** `POST /reports/generate` · `GET /reports` · `GET /reports/{id}` · `POST /reports/{id}/submit-for-approval` · `GET /reports/{id}/archive` (JPN prepares; Exec approves).
- **Service:** ReportService, WorkflowService. **DB:** Report, Approval, Audit_Log. **Agents/Skills:** Report Generation + S11/S1/S3/S4/S10/S15. **RTM:** FRQ-016, REPQ-001/002/005, BR-014/015/040.
- **Validation:** report is DRAFT until approved; **issue only after approval** (G15).
- **Audit:** generation + approval + issuance logged.

### G14 — Notification API
- **Purpose:** draft/queue/send approved notifications & reminders.
- **Endpoints:** `POST /notifications` (draft) · `GET /notifications/queue` · `POST /notifications/{id}/send` (post-approval) · `GET /notifications/{id}` (Admin/JPN).
- **Service:** NotificationService, WorkflowService. **DB:** Notification, Approval. **Agents/Skills:** Notification Agent + S12. **RTM:** FRQ-018/019, BR-007/040.
- **Validation:** **send only after human approval** (BR-015); escalation rules; queue + **retry on failure**.
- **Audit:** draft/approve/send/delivery + retries logged.

### G15 — Approval API (Human-in-the-Loop)
- **Purpose:** approve/reject formal actions (reports, notifications, recommendations).
- **Endpoints:** `GET /approvals/pending` (scoped) · `POST /approvals/{id}/approve` · `POST /approvals/{id}/reject` (Exec/Admin per item).
- **Service:** WorkflowService. **DB:** Approval, (target entity). **Agents/Skills:** none (human action). **RTM:** FRQ-017, AIRQ-011, BR-015/ASM-11.
- **Validation:** only authorised role for the item type; decision recorded with actor + comment.
- **Audit:** every decision logged (mandatory).

### G16 — Audit API
- **Purpose:** query the audit trail (read-only).
- **Endpoints:** `GET /audit?entity=&id=&actor=&from=&to=` · `GET /audit/{id}` (Internal Audit/Admin, scoped).
- **Service:** AuditService. **DB:** Audit_Log (append-only). **RTM:** FRQ-024, NFRQ-002, BR-009/030.
- **Validation:** read-only; role-scoped; no mutation possible.
- **Audit:** audit reads optionally logged.

### G17 — Configuration API
- **Purpose:** manage `config.md`-backed settings, provider/profile, amendment windows.
- **Endpoints:** `GET /admin/config` · `PUT /admin/config` · `POST /admin/amendment-windows` (Super Admin).
- **Service:** AdminConfigService. **DB:** (config store), Amendment_Window, Provider_Usage. **RTM:** FRQ-026, BR-044, TR-013/018.
- **Validation:** provider/profile valid; **secrets in `.env` only** (never via API); business logic provider-agnostic.
- **Audit:** config changes logged (rule 5 / §14).

### G18 — Health Check API
- **Purpose:** liveness/readiness for deployment & monitoring.
- **Endpoints:** `GET /health` (liveness) · `GET /health/ready` (DB/provider/vector reachability).
- **Service:** infra. **DB:** none (or light ping). **RTM:** NFRQ-006/008 (ops).
- **Validation:** no auth for basic liveness; readiness may be restricted.
- **Audit:** not required (operational metric).

---

## 3. Diagrams

### 3.1 API request lifecycle
```
[Client] → HTTPS → [/api/v1/...] → [JWT middleware] → [RBAC dependency]
   → [Router] → [Pydantic validation] → [Business Service] → [Repository/DB | Agent | RAG]
   → [Service result] → [Response envelope] → [Client]
   (mutations + AI calls → AuditService;  errors → {code,message,details,correlation_id})
```

### 3.2 Auth & RBAC flow
```
POST /auth/login {email,password}
   → domain check (@moe.gov.my/@moe-dl.edu.my) → verify → issue access(JWT)+refresh
Subsequent: Authorization: Bearer <access>
   → JWT verify → load role+scope → RBAC check per route → allow/deny(403)
POST /auth/refresh (HttpOnly cookie) → new access token
```

### 3.3 KPI monthly update flow
```
PIC → POST /api/v1/kpis/{id}/updates {achievement,finance_status,evidence,remarks}
   → RBAC(own KPI) → validate(completeness; period) → UpdateService save
   → DB(KPI_Monthly_Update) → AuditService log
   → trigger KPI Analysis(S1)/Risk(S3) → Dashboard refresh
   (statement/indicator/target edits → 409 unless Jul/Oct, BR-008)
```

### 3.4 AI agent request flow
```
POST /api/v1/ai/recommend {kpi_id|scope}
   → RBAC → AgentOrchestrationService → Agent(s) + Skills → (RAG if needed)
   → advisory draft (AI_Recommendation log) → response
   → NO direct approve/amend/send; Agent_Execution + output AUDITED
```

### 3.5 RAG chatbot request flow
```
POST /api/v1/chatbot/query {question}
   → RBAC(scope) → ChatbotService → enforce role scope
   → grounding order (KPI DB→updates→docs→RPM→links) → S9 retrieve → S10 cite
   → ProviderAdapter.chat() → grounded answer + citations
   → none → fixed fallback ; source down → clear message → log Q&A+sources
```

### 3.6 Report approval & email queue flow
```
POST /reports/generate → Report Generation Agent → DRAFT (Report)
   → POST /reports/{id}/submit-for-approval → Approval(pending)
   → Exec: POST /approvals/{id}/approve → Report.status=approved
   → POST /notifications/{id}/send (cover) → Email Queue → SMTP (retry on fail)
   → delivery + approval + issuance AUDITED
   (reject → returned for revision; nothing sent without approval)
```

---

## 4. Endpoint Summary Table (selected)

| Method | Path | Group | Role | Service | RTM |
|--------|------|-------|------|---------|-----|
| POST | `/api/v1/auth/login` | Auth | all | AuthService | FRQ-001 |
| POST | `/api/v1/import/pelan-taktikal` | Import | Super/JPN | ImportService | FRQ-003 |
| POST | `/api/v1/kpis/{id}/updates` | Monthly | PIC | UpdateService | FRQ-007 |
| GET | `/api/v1/dashboard/teras` | Dashboard | all(scoped) | DashboardService | FRQ-011 |
| POST | `/api/v1/fds/analyze` | FDS | Finance/Exec | FinanceService | FRQ-014/029 |
| POST | `/api/v1/ai/recommend` | AI Agent | scoped | AgentOrchestration | AIRQ-001 |
| POST | `/api/v1/chatbot/query` | Chatbot | all(scoped) | ChatbotService | FRQ-013 |
| POST | `/api/v1/copilot/insight` | Copilot | Exec | CopilotService | FRQ-023 |
| POST | `/api/v1/reports/generate` | Report | JPN/Exec | ReportService | FRQ-016 |
| POST | `/api/v1/approvals/{id}/approve` | Approval | Exec/Admin | WorkflowService | FRQ-017 |
| POST | `/api/v1/notifications/{id}/send` | Notification | Admin/JPN | NotificationService | FRQ-019 |
| GET | `/api/v1/audit` | Audit | Audit/Admin | AuditService | FRQ-024 |
| PUT | `/api/v1/admin/config` | Config | Super Admin | AdminConfigService | FRQ-026 |
| GET | `/api/v1/health` | Health | public | infra | NFRQ-008 |

---

## 5. Service-to-API Mapping

| Service (L2) | API group(s) | Module |
|--------------|--------------|--------|
| AuthService | G1 | M1 |
| AdminService / AdminConfigService | G2, G17 | M13 |
| KpiService | G3 | M2 |
| ImportService | G4 | M2 |
| UpdateService / ValidationService | G5 (G3 completeness) | M3/M4 |
| DashboardService | G6 | M5 |
| FinanceService | G7 | M6 |
| AgentOrchestrationService | G8 | M7 |
| SkillRegistry (internal) | G9 | M7 |
| KnowledgeService | G10 | M8 |
| ChatbotService | G11 | M9 |
| CopilotService | G12 | M7 |
| ReportService | G13 | M10 |
| NotificationService | G14 | M11 |
| WorkflowService | G15 (+ G13/G14 gating) | M12 |
| AuditService | G16 (+ cross-cutting) | M12 |
| infra | G18 | M13/ops |

---

## 6. Important-rule compliance

| Rule | Compliance |
|------|-----------|
| 1 JWT on protected APIs | §3.2; all groups except G1 login / G18 liveness. |
| 2 RBAC enforced | server-side dependency on every route. |
| 3 AI APIs don't approve/amend/send | G8/G9/G11/G12 advisory; actions via G15. |
| 4 Report send via human approval | G13→G15→G14. |
| 5 Chatbot grounded + cited | G11 (S9/S10), fixed fallback. |
| 6 FDS advisory | G7 outputs advisory; HITL before implementation. |
| 7 Monthly updates in-system | G5; no monthly Excel. |
| 8 Excel initial import only | G4 import-once. |
| 9 `/api/v1` versioning | all paths. |
| 10 Production-ready | health checks (G18), config profiles, stateless JWT. |

---

## 7. Suggested Implementation Order (`/routes`,`/services`)

1. **G18 Health** + app scaffold (FastAPI, `/api/v1`, error envelope).
2. **G1 Auth** + JWT/RBAC middleware (foundation for all).
3. **G2 User & Role** + **G17 Configuration** (admin foundation).
4. **G3 KPI** + **G4 Import** (data in).
5. **G5 Monthly Update** (+ completeness/validation).
6. **G16 Audit** (wire early; many write to it) + **G15 Approval** (HITL).
7. **G6 Dashboard** (read models).
8. **G7 FDS** + **G8 AI Agent** + **G9 Skills** (AI core).
9. **G10 Knowledge/RAG** + **G11 Chatbot** + **G12 Copilot**.
10. **G13 Report** + **G14 Notification** (HITL-gated outputs).
> Build + test each group before the next (TR-006); secure by default (JWT/RBAC) from G1.

---

## Final Output (summary)
1. **Complete API Blueprint** — §1–§7.
2. **API group catalogue** — §1 (18 groups).
3. **Endpoint summary table** — §4.
4. **Service-to-API mapping** — §5.
5. **Implementation order** — §7.

---
*End of API Architecture Blueprint v0.1 — DRAFT. No code. Frozen baselines unmodified. Awaiting approval.*
