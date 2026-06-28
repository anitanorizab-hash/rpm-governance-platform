"""Demo seed (CP22) — populates a presentation-ready dataset using existing services only.

NO new business logic: this script only calls the same services/repositories the API uses.
Run against a migrated dev DB:

    cd backend
    set PYTHONPATH=.        (PowerShell: $env:PYTHONPATH=".")
    python scripts/seed_demo.py

It creates 6 demo users (one per role), enriches KPIs to cover every risk/finance state,
generates FDS recommendations + OBB + LCHI, registers & processes an RPM knowledge source
(for grounded + fallback RAG demos), and produces report / notification / chatbot / copilot
history with the human-in-the-loop approval trail.
"""
from __future__ import annotations

import os
import types

from app.db.session import SessionLocal
from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.repositories.kpi_repository import KPIRepository
from app.services.import_service import ImportService
from app.services.monthly_update_service import MonthlyUpdateService
from app.services.fds_service import FDSService
from app.services.approval_service import ApprovalService
from app.services.knowledge_service import KnowledgeService
from app.services.chatbot_service import ChatbotService
from app.services.executive_copilot_service import ExecutiveCopilotService
from app.services.report_service import ReportService
from app.services.notification_service import NotificationService
from app.models.operational.finance import FinancialAllocation
import uuid

JPN_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "Data", "PELAN TAKTIKAL JPN.xlsx"
)
SECTOR = "Sektor Pengurusan Sekolah"
PW = "Demo@2026"

DEMO_USERS = [
    ("superadmin@moe.gov.my", "Dr. Aminah (Super Admin)", "super_admin", None),
    ("jpnadmin@moe.gov.my", "En. Faizal (JPN Admin)", "jpn_admin", None),
    ("executive@moe.gov.my", "Datuk Rahman (Executive)", "executive", None),
    ("sector@moe.gov.my", "Pn. Siti (Sector Admin)", "sector_admin", SECTOR),
    ("pic@moe.gov.my", "Cik Lina (KPI PIC)", "kpi_pic", None),
    ("readonly@moe.gov.my", "Encik Tan (Read Only)", "read_only", None),
]

# (achievement vs target=100, finance_status) → produces varied risk + finance distribution
UPDATE_PLAN = [
    ("100", "received"),         # achieved      -> low risk
    ("90", "will_be_received"),  # on_track      -> low risk
    ("65", "pending"),           # at_risk       -> medium risk
    ("30", "insufficient"),      # off_track     -> high risk
    ("20", "not_received"),      # off_track     -> high risk
    ("100", "not_required"),     # achieved      -> low risk
]

RPM_CONTENT = (
    "Rancangan Pemajuan Malaysia (RPM) 2026-2035 is the national strategic education plan. "
    "Its strategic priorities span seven Teras: access to quality education, equity, "
    "education quality, efficiency of delivery, talent development, governance, and "
    "financial sustainability. Each Teras defines KPIs that JPN, PPD and schools must "
    "monitor monthly. Budget allocation follows outcome-based budgeting (OBB) principles, "
    "favouring low-cost high-impact interventions. Human review and approval is mandatory "
    "before any official report is issued or notification is sent."
)


def actor(u):
    return u  # User model already exposes id / email / scope / role_names


def main():
    db = SessionLocal()
    try:
        urepo = UserRepository(db)
        krepo = KPIRepository(db)

        # 1) Import operational data (60 KPIs, Teras 1-4)
        with open(os.path.abspath(JPN_FILE), "rb") as f:
            res = ImportService(db).execute(file_bytes=f.read(), filename="PELAN TAKTIKAL JPN.xlsx",
                                            plan_type="jpn", actor_id=None, override=True)
        print("Import:", res.get("status"), "->", res.get("rows_imported"), "KPIs")

        # 2) Demo users
        users = {}
        for email, name, role, scope in DEMO_USERS:
            u = urepo.get_by_email(email)
            if not u:
                u = urepo.create_user(email=email, name=name, password_hash=hash_password(PW), scope=scope)
            if scope and not u.scope:
                u.scope = scope
            r = urepo.get_role_by_name(role)
            if r and role not in u.role_names:
                urepo.assign_role(u, r)
            users[role] = u
        db.commit()
        admin = users["super_admin"]
        print("Users:", ", ".join(users.keys()))

        # 3) Enrich a set of KPIs: complete records, target=100, PIC + sector
        kpis = krepo.list(limit=8)
        enriched = kpis[:6]
        for i, k in enumerate(enriched):
            krepo.set_indicator(k, f"Peratus pencapaian sasaran KPI {k.code}")
            krepo.set_target(k, "100")
            pic_email = "pic@moe.gov.my" if i == 0 else f"pic{i}@moe.gov.my"
            pic = krepo.get_or_create_pic(name="Cik Lina (KPI PIC)" if i == 0 else f"PIC {i}",
                                          email=pic_email, sector=SECTOR if i == 0 else None)
            k.pic_id = pic.id
            if i == 0:
                k.sector = SECTOR
        db.commit()

        # 4) Financial allocations: one high-cost (Strategic Investment) + one low-cost (Priority Action)
        db.add(FinancialAllocation(id=str(uuid.uuid4()), kpi_id=enriched[0].id, amount=120000.0, expenditure=90000.0))
        db.add(FinancialAllocation(id=str(uuid.uuid4()), kpi_id=enriched[1].id, amount=8000.0, expenditure=5000.0))
        db.commit()

        # 5) Monthly updates -> varied achievement status, risk, finance status
        mu = MonthlyUpdateService(db)
        for k, (ach, fin) in zip(enriched, UPDATE_PLAN):
            mu.create(current_user=actor(admin),
                      data={"kpi_id": k.id, "reporting_year": 2026, "reporting_month": 6,
                            "achievement_value": ach, "finance_status": fin,
                            "evidence_ref": f"DOC-{k.code}", "remarks": "Demo monthly update",
                            "issue_description": "Demo issue" if ach in ("30", "20") else None,
                            "proposed_action": "Reallocate / intervene" if ach in ("30", "20") else None},
                      override=True)
        print("Monthly updates: 6 (low/medium/high risk; all finance states)")

        # 6) FDS: generate recommendations (creates OBB + LCHI + StrategicRecommendation)
        fds = FDSService(db)
        rec_ids = []
        for k in enriched[:4]:
            out = fds.generate(current_user=actor(admin), kpi_id=k.id)
            if out and out.get("recommendation_id"):
                rec_ids.append(out["recommendation_id"])
        print("FDS recommendations generated:", len(rec_ids))

        # one submitted-for-approval (pending), one submitted + approved (HITL trail)
        if rec_ids:
            fds.submit_for_approval(current_user=actor(admin), rec_id=rec_ids[0])
        if len(rec_ids) > 1:
            sub = fds.submit_for_approval(current_user=actor(admin), rec_id=rec_ids[1])
            # approve via CP9 (super_admin override since requester == approver in demo)
            ApprovalService(db).approve(approval_id=sub["approval_id"], actor=actor(admin), override=True)

        # 7) Knowledge base: register + process an RPM source (grounded + fallback demo)
        ks = KnowledgeService(db)
        src = ks.create_source(actor_id=admin.id, data={
            "type": "static", "title": "RPM 2026-2035 Strategic Overview",
            "category": "rpm", "format": "txt", "reliability": "trusted",
            "content": RPM_CONTENT,
        })
        ks.process_source(actor_id=admin.id, source_id=src.id)
        print("Knowledge source registered + processed:", src.title)

        # 8) Chatbot history: a grounded question + a fallback question
        cb = ChatbotService(db)
        sess = cb.create_session(actor(admin))
        cb.send_message(current_user=actor(admin), session_id=sess.id,
                        message="What are the strategic priorities of RPM 2026-2035?")
        cb.send_message(current_user=actor(admin), session_id=sess.id,
                        message="What is the population of Mars?")  # -> fallback
        print("Chatbot session seeded (grounded + fallback)")

        # 9) Executive Copilot history: briefing + grounded ask + fallback ask + draft rec
        exec_user = users["executive"]
        cop = ExecutiveCopilotService(db)
        cop.briefing(current_user=actor(exec_user))
        cop.ask(current_user=actor(exec_user), question="What are the RPM strategic priorities and OBB principles?")
        cop.ask(current_user=actor(exec_user), question="What time does the moon rise tomorrow?")  # fallback
        crec = cop.create_recommendation(current_user=actor(exec_user),
                                         data={"kpi_id": enriched[0].id,
                                               "content": "Protect funding for high-impact low-cost interventions.",
                                               "rationale": "Aligns with OBB and Teras priorities.", "priority": 1})
        cop.submit_for_approval(current_user=actor(exec_user), rec_id=crec.id)
        print("Executive Copilot history seeded")

        # 10) Reports: one archived (full HITL trail) + one left pending_review
        rs = ReportService(db)
        r1 = rs.generate(current_user=actor(admin), period="2026-06", type_="monthly")
        s1 = rs.submit_for_review(current_user=actor(admin), report_id=r1["id"])
        ApprovalService(db).approve(approval_id=s1["approval_id"], actor=actor(admin), override=True)
        rs.archive(current_user=actor(admin), report_id=r1["id"])
        r2 = rs.generate(current_user=actor(admin), period="2026-05", type_="monthly")
        rs.submit_for_review(current_user=actor(admin), report_id=r2["id"])
        print("Reports: 1 archived + 1 pending_review")

        # 11) Notifications: one queued (dry-run sent) + one pending_review
        ns = NotificationService(db)
        n1 = ns.draft(current_user=actor(admin),
                      data={"type": "reminder", "recipient": "pic@moe.gov.my",
                            "subject": "Monthly KPI update due", "detail": "Please submit June update."})
        sn1 = ns.submit_for_review(current_user=actor(admin), notification_id=n1.id)
        ApprovalService(db).approve(approval_id=sn1["approval_id"], actor=actor(admin), override=True)
        ns.queue(current_user=actor(admin), notification_id=n1.id)
        n2 = ns.draft(current_user=actor(admin),
                      data={"type": "escalation", "recipient": "jpnadmin@moe.gov.my",
                            "subject": "High-risk KPIs need attention", "detail": "Escalation demo."})
        ns.submit_for_review(current_user=actor(admin), notification_id=n2.id)
        print("Notifications: 1 queued (dry-run) + 1 pending_review")

        print("\nDEMO SEED COMPLETE. Users password:", PW)
    finally:
        db.close()


if __name__ == "__main__":
    main()
