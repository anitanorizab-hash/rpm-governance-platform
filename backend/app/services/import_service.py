"""Import service (CP6; V1.1.1 organisation-aware, dual-layout).

Excel is INITIAL input only (BR-001/018). Detects the organisation from the filename (JPN or a PPD),
get-or-creates it (PPDs parented to the JPN root), and imports KPIs + activities (Aktiviti Utama /
Sokongan / Milestone) + PIC. KPI codes are unique PER organisation. Continuation rows (extra activity
lines under one KPI) are carried forward. Import-once lock by file hash (admin override). Audited.
"""
from __future__ import annotations

import hashlib
import json
import os
import re

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.repositories.import_repository import ImportRepository
from app.services.audit_service import AuditService
from app.skills import excel_parsing_skill as parser


def _to_int_teras(value) -> int | None:
    try:
        return int(str(value).strip().split()[-1])
    except Exception:
        return None


def detect_organisation(filename: str) -> dict:
    """Derive {type, code, name} from a Pelan Taktikal filename.

    'PELAN TAKTIKAL JPN.xlsx' -> JPN; '07 - PPD KINTA UTARA (TERAS 1-TERAS 7).xlsx' -> PPD Kinta Utara.
    """
    base = re.sub(r"\.(xlsx|xls|xlsm)$", "", os.path.basename(filename or ""), flags=re.I)
    if re.search(r"\bPPD\b", base, re.I):
        core = re.sub(r"\(.*?\)", "", base)               # drop "(TERAS 1-TERAS 7)"
        core = re.sub(r"^\s*\d+\s*[-.]?\s*", "", core)     # drop leading "07 - "
        core = re.sub(r"(?i)\bPPD\b", "", core)            # drop "PPD"
        core = re.sub(r"\s+", " ", core).strip(" -")
        code = "PPD-" + re.sub(r"\s+", "-", core.upper()) if core else "PPD-UNKNOWN"
        name = ("PPD " + core.title()) if core else "PPD (Unknown)"
        return {"type": "PPD", "code": code, "name": name}
    return {"type": "JPN", "code": "JPN", "name": "Jabatan Pendidikan Negeri"}


class ImportService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ImportRepository(db)
        self.audit = AuditService(db)

    @staticmethod
    def _hash(file_bytes: bytes) -> str:
        return hashlib.sha256(file_bytes).hexdigest()

    def _parse(self, file_bytes: bytes) -> dict:
        return parser.parse_workbook(file_bytes)

    # ---------- preview ----------
    def preview(self, *, file_bytes: bytes, plan_type: str | None = None, filename: str = "") -> dict:
        parsed = self._parse(file_bytes)
        rows = parsed["rows"]
        file_hash = self._hash(file_bytes)
        org = detect_organisation(filename) if filename else {"type": (plan_type or "jpn").upper()}

        warnings, to_create = [], {"kpi": 0, "pic": 0, "indicator": 0, "target": 0, "activity": 0}
        seen_pics = set()
        for i, rec in enumerate(rows, start=1):
            if parser.derive_statement(rec):
                miss = parser.missing_fields(rec)
                if miss:
                    warnings.append({"row": i, "kpi_code": parser.derive_code(rec), "missing_fields": miss})
                to_create["kpi"] += 1
                if rec.get("indicator"):
                    to_create["indicator"] += 1
                if rec.get("target"):
                    to_create["target"] += 1
                name = parser.derive_pic_name(rec)
                if name and name not in seen_pics:
                    seen_pics.add(name); to_create["pic"] += 1
            if rec.get("aktiviti_utama") or rec.get("milestone"):
                to_create["activity"] += 1
            if rec.get("aktiviti_sokongan") or rec.get("pic_support"):
                to_create["activity"] += 1

        duplicate = self.repo.find_completed_batch_by_hash(file_hash) is not None
        return {
            "plan_type": org.get("type", "JPN").lower(),
            "organisation_type": org.get("type"), "organisation_name": org.get("name"),
            "total_rows": len(rows), "sheets_parsed": parsed["sheets"],
            "skipped_sheets": parsed["skipped_sheets"], "records_to_create": to_create,
            "warnings": warnings, "duplicate_risk": duplicate, "file_hash": file_hash,
        }

    # ---------- activity helper ----------
    def _add_activities(self, kpi_id: str, rec: dict) -> int:
        added = 0
        utama = rec.get("aktiviti_utama")
        milestone = rec.get("milestone")
        status = rec.get("status_pelaksanaan")
        remarks = rec.get("catatan")
        nota = rec.get("nota_pengiraan")
        if any(v not in (None, "") for v in (utama, milestone, status, remarks, nota)):
            self.repo.add_activity(
                kpi_id, type="utama",
                description=(str(utama) if utama else None),
                milestone=(str(milestone) if milestone else None),
                status=(str(status) if status else None),
                remarks=(str(remarks) if remarks else None),
                nota_pengiraan=(str(nota) if nota else None),
            )
            added += 1
        # Aktiviti Sokongan (JPN) or Penyokong KPI (PPD supporting unit) → a sokongan activity.
        sokongan = rec.get("aktiviti_sokongan") or rec.get("pic_support")
        if sokongan not in (None, ""):
            self.repo.add_activity(kpi_id, type="sokongan", description=str(sokongan))
            added += 1
        return added

    def _resolve_pic(self, rec: dict, dept):
        name = parser.derive_pic_name(rec)
        email = rec.get("pic_email")
        if not name and not email:
            return None
        return self.repo.get_or_create_pic(
            name=(name or "(unspecified)"), email=(str(email) if email else None),
            sector=(str(rec.get("department")) if rec.get("department") else None),
            dept_id=(dept.id if dept else None),
        )

    # ---------- execute ----------
    def execute(self, *, file_bytes: bytes, filename: str, plan_type: str | None = None,
                actor_id: str | None, override: bool = False,
                context: AuditContext | None = None) -> dict:
        file_hash = self._hash(file_bytes)
        existing = self.repo.find_completed_batch_by_hash(file_hash)
        if existing and not override:
            return {
                "batch_id": existing.id, "plan_type": existing.plan_type,
                "organisation_id": existing.organisation_id,
                "rows_total": existing.rows_total, "rows_imported": existing.rows_imported,
                "warnings_count": existing.warnings_count, "status": "blocked", "blocked": True,
                "message": "This file was already imported. Use override=true (admin) to re-import.",
            }

        org_info = detect_organisation(filename)
        parent_id = self.repo.jpn_root_id() if org_info["type"] == "PPD" else None
        org = self.repo.get_or_create_organisation(
            code=org_info["code"], name=org_info["name"], type=org_info["type"], parent_id=parent_id)

        parsed = self._parse(file_bytes)
        rows = parsed["rows"]
        warnings, imported = [], 0
        used_codes: set[str] = set()
        current_kpi = None

        for i, rec in enumerate(rows, start=1):
            stmt = parser.derive_statement(rec)
            if not stmt:
                # continuation row: extra activity lines belong to the current KPI
                if current_kpi is not None:
                    self._add_activities(current_kpi.id, rec)
                continue

            miss = parser.missing_fields(rec)
            if miss:
                warnings.append({"row": i, "kpi_code": parser.derive_code(rec), "missing_fields": miss})

            teras = self.repo.get_teras_by_number(_to_int_teras(rec.get("teras"))) if rec.get("teras") else None
            dept = self.repo.get_or_create_department(str(rec["department"])) if rec.get("department") else None
            pic = self._resolve_pic(rec, dept)

            raw_code = parser.derive_code(rec) or f"AUTO-{org.code}-{i}"
            existing_kpi = self.repo.get_kpi_by_code(raw_code, org.id)
            if existing_kpi:
                # Already present for this org → never duplicate (composite unique). Override re-imports
                # the file (bypasses the hash lock); it does not duplicate existing KPIs.
                current_kpi = existing_kpi
                continue
            code = raw_code
            n = 2
            while code in used_codes or self.repo.get_kpi_by_code(code, org.id) is not None:
                code = f"{raw_code}#{n}"; n += 1

            kpi = self.repo.create_kpi(
                code=code, organisation_id=org.id, teras_id=(teras.id if teras else None),
                statement=stmt, department_id=(dept.id if dept else None),
                sector=(str(rec.get("department")) if rec.get("department") else None),
                pic_id=(pic.id if pic else None),
            )
            used_codes.add(code)
            current_kpi = kpi
            imported += 1
            if rec.get("indicator"):
                self.repo.add_indicator(kpi.id, str(rec["indicator"]))
            if rec.get("target"):
                self.repo.add_target(kpi.id, str(rec["target"]),
                                     str(rec.get("tov")) if rec.get("tov") else None)
            self._add_activities(kpi.id, rec)

        batch = self.repo.create_batch(
            filename=filename, file_hash=file_hash, plan_type=org_info["type"].lower(),
            organisation_id=org.id, rows_total=len(rows), rows_imported=imported,
            warnings_count=len(warnings), status="completed", warnings=json.dumps(warnings),
            imported_by=actor_id,
        )
        self.audit.record(
            entity_type="import_batch", entity_id=batch.id, action="import_execute",
            actor_id=actor_id, after={"organisation": org.code, "organisation_type": org_info["type"],
                                      "rows_imported": imported, "warnings": len(warnings),
                                      "override": override},
            context=context, commit=False,
        )
        self.db.commit()
        return {
            "batch_id": batch.id, "plan_type": org_info["type"].lower(),
            "organisation_id": org.id, "organisation_name": org.name,
            "rows_total": len(rows), "rows_imported": imported,
            "warnings_count": len(warnings), "status": "completed", "blocked": False,
        }

    # ---------- batch import (reused by script + admin endpoint) ----------
    def execute_path(self, *, path: str, actor_id: str | None, override: bool = False,
                     context: AuditContext | None = None) -> dict:
        with open(path, "rb") as fh:
            data = fh.read()
        return self.execute(file_bytes=data, filename=os.path.basename(path),
                            actor_id=actor_id, override=override, context=context)

    def import_data_folder(self, *, data_dir: str, actor_id: str | None, override: bool = False,
                           context: AuditContext | None = None) -> dict:
        """Import the JPN plan + every PPD plan found under data_dir. Reuses execute() per file."""
        results = []
        jpn = os.path.join(data_dir, "PELAN TAKTIKAL JPN.xlsx")
        if os.path.exists(jpn):
            results.append(self.execute_path(path=jpn, actor_id=actor_id, override=override, context=context))
        ppd_dir = os.path.join(data_dir, "PELAN TAKTIKAL PPD")
        if os.path.isdir(ppd_dir):
            for fn in sorted(os.listdir(ppd_dir)):
                if fn.lower().endswith((".xlsx", ".xls")) and not fn.startswith("~$"):
                    results.append(self.execute_path(path=os.path.join(ppd_dir, fn),
                                                     actor_id=actor_id, override=override, context=context))
        return {"files": len(results), "results": results}
