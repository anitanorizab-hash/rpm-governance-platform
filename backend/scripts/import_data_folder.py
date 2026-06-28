"""V1.1.1 batch import: seed reference + demo users, then import the JPN plan and ALL PPD plans
from the repo Data folder. Idempotent-ish (uses override for re-runs). Run:  python scripts/import_data_folder.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # backend on path

from sqlalchemy import func, select  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.db.knowledge_seed import seed_rpm_knowledge  # noqa: E402
from app.db.seed import seed_reference_data  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.models.operational.kpi import KPI, Activity  # noqa: E402
from app.models.operational.organisation import Organisation  # noqa: E402
from app.repositories.user_repository import UserRepository  # noqa: E402
from app.services.import_service import ImportService  # noqa: E402

DATA_DIR = str(Path(__file__).resolve().parents[2] / "Data")
PW = "Demo@2026"
SECTOR = "Sektor Pengurusan Sekolah"
DEMO_USERS = [
    ("superadmin@moe.gov.my", "Dr. Aminah (Super Admin)", "super_admin", None),
    ("jpnadmin@moe.gov.my", "En. Faizal (JPN Admin)", "jpn_admin", None),
    ("executive@moe.gov.my", "Datuk Rahman (Executive)", "executive", None),
    ("sector@moe.gov.my", "Pn. Siti (Sector Admin)", "sector_admin", SECTOR),
    ("pic@moe.gov.my", "Cik Lina (KPI PIC)", "kpi_pic", None),
    ("readonly@moe.gov.my", "Encik Tan (Read Only)", "read_only", None),
]


def main():
    db = SessionLocal()
    try:
        seed_reference_data(db)
        urepo = UserRepository(db)
        for email, name, role, scope in DEMO_USERS:
            u = urepo.get_by_email(email)
            if not u:
                u = urepo.create_user(email=email, name=name, password_hash=hash_password(PW), scope=scope)
            r = urepo.get_role_by_name(role)
            if r and role not in u.role_names:
                urepo.assign_role(u, r)
        db.commit()

        seed_rpm_knowledge(db)   # V1.1.2: RPM policy reference for the RAG chatbot
        res = ImportService(db).import_data_folder(data_dir=DATA_DIR, actor_id=None, override=True)
        print(f"\nImported {res['files']} file(s).")
        print("\nOrganisation                     Type  KPIs")
        print("-" * 52)
        total_kpi = 0
        for o in db.scalars(select(Organisation).order_by(Organisation.type.desc(), Organisation.name)):
            n = db.scalar(select(func.count()).select_from(KPI).where(KPI.organisation_id == o.id)) or 0
            total_kpi += n
            print(f"  {o.name[:30]:30} {o.type:4}  {n}")
        ppd_count = db.scalar(select(func.count()).select_from(Organisation).where(Organisation.type == "PPD"))
        acts = db.scalar(select(func.count()).select_from(Activity)) or 0
        print("-" * 52)
        print(f"PPD organisations: {ppd_count} | total KPIs: {total_kpi} | total activities: {acts}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
