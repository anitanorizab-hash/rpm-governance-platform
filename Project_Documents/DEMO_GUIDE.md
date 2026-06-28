# Demonstration Guide — Agentic AI Strategic Governance Platform (v1.0.0)

A recommended **15-minute** guided walkthrough. AI is advisory; a human approves every formal action.

## Startup
```
# Terminal 1 — backend
cd backend
alembic upgrade head            # first run only
python scripts/seed_demo.py     # load demonstration data (idempotent)
uvicorn app.main:app --port 8000

# Terminal 2 — frontend
cd frontend
npm run dev                     # http://localhost:5173
```

## Demo users (password: `Demo@2026`)
| Role | Email | Demonstrates |
|------|-------|--------------|
| Super Admin | superadmin@moe.gov.my | Full access; role assignment; admin module |
| JPN Administrator | jpnadmin@moe.gov.my | Full KPI/report/notification management |
| Executive Management | executive@moe.gov.my | Dashboard + Executive Copilot; read-only governance |
| Sector Administrator | sector@moe.gov.my | Sector-scoped data only |
| KPI PIC | pic@moe.gov.my | Sees only assigned KPI; submits monthly update |
| Read Only | readonly@moe.gov.my | View-only; no edit/approve controls |

## 15-minute flow
1. **Login** (00:00) — sign in as Super Admin; note MOE-domain restriction on the register page.
2. **Dashboard** (01:00) — populated Teras overview; achievement, risk and budget summaries.
3. **Teras 1–7 overview** (02:30) — bar chart of KPI counts by Teras; risk pie; high-risk list.
4. **KPI Management** (04:00) — filter by Teras/status/completeness; open a KPI; show completeness card.
5. **Monthly Update** (05:30) — log in as **KPI PIC**; show the single assigned KPI; submit an update; status + risk auto-derived; audit entry created.
6. **Financial Decision Support** (07:00) — back as Admin; open FDS; pick a KPI; show Budget Intelligence + OBB.
7. **Low Cost / High Impact Matrix** (08:00) — highlight the KPI's quadrant; show low-cost alternatives + advisory recommendation.
8. **Reports** (09:00) — open the archived report (full draft→review→approved→archived trail); note **no approve button** on the page.
9. **Notifications** (10:00) — show the queued (dry-run "Sent") notification and one pending review; dry-run banner.
10. **Chatbot** (10:45) — ask *"What are the strategic priorities of RPM 2026–2035?"* → **grounded answer + citation**; then ask an off-topic question → **fixed fallback message**.
11. **Executive Copilot** (12:00) — log in as **Executive**; Generate Briefing (risks, FDS insight, advisory-only + human-review banners); show a recommendation draft routed for approval.
12. **Admin Module** (13:00) — Super Admin → Users (assign a role), Knowledge (the RPM source; Pelan-Taktikal-not-RAG reminder).
13. **Audit Trail** (13:45) — Admin → Audit; filter by entity; show append-only notice (no edit/delete).
14. **Human Approval Workflow** (14:15) — recap: every AI output is advisory and routes to the approval engine; final states are immutable.
15. **Closing Summary** (14:45) — one platform replaces scattered Excel; disciplined monthly updates; advisory AI with mandatory human approval; full audit trail.

## Talking points
- **Governance first:** no AI agent approves, amends, deletes or sends — everything routes to a human.
- **Traceability:** every official action is in the append-only audit log.
- **Grounded AI:** answers cite sources or return a fixed "cannot find" message — never guesses.
- **Role security:** PIC sees only their KPI; read-only cannot edit; Admin gated to Super/JPN Admin.

## Reset between demos
`python backend/scripts/seed_demo.py` re-applies the dataset (delete `app_dev.db` + `alembic upgrade head` first for a pristine run).
