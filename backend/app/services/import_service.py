"""Import service (CP6): preview + execute the one-time Pelan Taktikal Excel import.

Excel is INITIAL input only (BR-001/018). Execute writes operational entities, records warnings for
missing fields (no silent failure), enforces an import-once lock by file hash (admin override allowed),
creates an audited ImportBatch. Does NOT create monthly updates or AI recommendations.
"""
from __future__ import annotations

import hashlib
import json

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.repositories.import_repository import ImportRepository
from app.services.audit_service import AuditService
from app.skills import excel_parsing_skill as parser


def _to_int_teras(value) -> int | None:
    try:
        return int(str(value).strip().split()[-1])  # "Teras 1" / "1" → 1
    except Exception:
        return None


class ImportService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ImportRepository(db)
        self.audit = AuditService(db)

    # ---------- parsing ----------
    @staticmethod
    def _hash(file_bytes: bytes) -> str:
        return hashlib.sha256(file_bytes).hexdigest()

    def _parse(self, file_bytes: bytes) -> dict:
        return parser.parse_workbook(file_bytes)

    # ---------- preview ----------
    def preview(self, *, file_bytes: bytes, plan_type: str) -> dict:
        parsed = self._parse(file_bytes)
        rows = parsed["rows"]
        file_hash = self._hash(file_bytes)

        warnings, to_create = [], {"kpi": 0, "pic": 0, "department": 0, "indicator": 0, "target": 0, "activity": 0}
        seen_pics, seen_depts = set(), set()
        for i, rec in enumerate(rows, start=1):
            miss = parser.missing_fields(rec)
            if miss:
                warnings.append({"row": i, "kpi_code": rec.get("kpi_code"), "missing_fields": miss})
            if rec.get("kpi_code") or rec.get("kpi_statement"):
                to_create["kpi"] += 1
            if rec.get("indicator"):
                to_create["indicator"] += 1
            if rec.get("target"):
                to_create["target"] += 1
            if rec.get("activity"):
                to_create["activity"] += 1
            if rec.get("pic_email") and rec["pic_email"] not in seen_pics:
                seen_pics.add(rec["pic_email"]); to_create["pic"] += 1
            if rec.get("department") and rec["department"] not in seen_depts:
                seen_depts.add(rec["department"]); to_create["department"] += 1

        duplicate = self.repo.find_completed_batch_by_hash(file_hash) is not None
        return {
            "plan_type": plan_type,
            "total_rows": len(rows),
            "sheets_parsed": parsed["sheets"],
            "skipped_sheets": parsed["skipped_sheets"],
            "records_to_create": to_create,
            "warnings": warnings,
            "duplicate_risk": duplicate,
            "file_hash": file_hash,
        }

    # ---------- execute ----------
    def execute(self, *, file_bytes: bytes, filename: str, plan_type: str,
                actor_id: str | None, override: bool = False,
                context: AuditContext | None = None) -> dict:
        file_hash = self._hash(file_bytes)
        existing = self.repo.find_completed_batch_by_hash(file_hash)
        if existing and not override:
            return {
                "batch_id": existing.id, "plan_type": plan_type, "rows_total": existing.rows_total,
                "rows_imported": existing.rows_imported, "warnings_count": existing.warnings_count,
                "status": "blocked", "blocked": True,
                "message": "This file was already imported. Use override=true (admin) to re-import.",
            }

        parsed = self._parse(file_bytes)
        rows = parsed["rows"]
        warnings, imported = [], 0

        for i, rec in enumerate(rows, start=1):
            miss = parser.missing_fields(rec)
            if miss:
                warnings.append({"row": i, "kpi_code": rec.get("kpi_code"), "missing_fields": miss})
            # require at least a KPI code or statement to create a record (else skip with warning)
            if not (rec.get("kpi_code") or rec.get("kpi_statement")):
                continue

            teras = self.repo.get_teras_by_number(_to_int_teras(rec.get("teras"))) if rec.get("teras") else None
            dept = self.repo.get_or_create_department(str(rec["department"])) if rec.get("department") else None
            pic = None
            if rec.get("pic_email"):
                pic = self.repo.get_or_create_pic(
                    name=str(rec.get("pic_name") or ""), email=str(rec["pic_email"]),
                    sector=str(rec.get("department") or "") or None, dept_id=(dept.id if dept else None),
                )

            code = str(rec.get("kpi_code") or f"AUTO-{i}")
            kpi = self.repo.get_kpi_by_code(code)
            if kpi and not override:
                # idempotent: skip existing KPI on a normal run
                continue
            if not kpi:
                kpi = self.repo.create_kpi(
                    code=code, teras_id=(teras.id if teras else None),
                    statement=(str(rec.get("kpi_statement")) if rec.get("kpi_statement") else None),
                    department_id=(dept.id if dept else None),
                    sector=(str(rec.get("department")) if rec.get("department") else None),
                    pic_id=(pic.id if pic else None),
                )
                if rec.get("indicator"):
                    self.repo.add_indicator(kpi.id, str(rec["indicator"]))
                if rec.get("target"):
                    self.repo.add_target(kpi.id, str(rec["target"]),
                                         str(rec.get("tov")) if rec.get("tov") else None)
                if rec.get("activity"):
                    self.repo.add_activity(kpi.id, str(rec["activity"]))
                imported += 1

        batch = self.repo.create_batch(
            filename=filename, file_hash=file_hash, plan_type=plan_type,
            rows_total=len(rows), rows_imported=imported, warnings_count=len(warnings),
            status="completed", warnings=json.dumps(warnings), imported_by=actor_id,
        )
        self.audit.record(
            entity_type="import_batch", entity_id=batch.id, action="import_execute",
            actor_id=actor_id, after={"plan_type": plan_type, "rows_imported": imported,
                                      "warnings": len(warnings), "override": override},
            context=context, commit=False,
        )
        self.db.commit()
        return {
            "batch_id": batch.id, "plan_type": plan_type, "rows_total": len(rows),
            "rows_imported": imported, "warnings_count": len(warnings),
            "status": "completed", "blocked": False,
        }
