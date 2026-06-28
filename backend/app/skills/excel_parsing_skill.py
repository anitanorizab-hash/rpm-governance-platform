"""Excel parsing skill (CP6) — reusable, deterministic, independently testable.

Reads a Pelan Taktikal workbook into canonical row dicts via a synonym-based column map.
Auto-detects the header row. Used ONLY by the one-time import pipeline (Excel = initial input only).
"""
from __future__ import annotations

import io
import re

import openpyxl

# Canonical fields → accepted header synonyms (normalised lower-case).
COLUMN_MAP: dict[str, list[str]] = {
    "teras": ["teras"],
    "kpi_code": ["kpi code", "kod kpi", "kod"],
    "kpi_statement": ["kpi statement", "kpi", "penyataan kpi"],
    "indicator": ["indicator", "petunjuk", "indikator"],
    "target": ["target", "sasaran", "sasaran 2026"],
    "tov": ["tov", "pencapaian 2025", "baseline"],
    "pic_name": ["pic name", "nama pic", "pegawai", "pic"],
    "pic_email": ["pic email", "emel pic", "email"],
    "department": ["department", "bahagian", "sector", "sektor"],
    "activity": ["activity", "aktiviti", "aktiviti utama"],
    "object_code": ["object code", "kod objek", "os code"],
    "amount": ["amount", "jumlah", "jumlah (rm)", "amaun"],
}

MANDATORY_FIELDS = (
    "kpi_statement", "indicator", "target", "pic_name", "pic_email", "department", "teras",
)


def _norm(s) -> str:
    return re.sub(r"\s+", " ", str(s or "").strip().lower())


def _build_header_index(header_cells: list) -> dict[int, str]:
    """Map column index → canonical field for a candidate header row."""
    mapping: dict[int, str] = {}
    for idx, cell in enumerate(header_cells):
        text = _norm(cell)
        if not text:
            continue
        for canonical, synonyms in COLUMN_MAP.items():
            if text in synonyms and canonical not in mapping.values():
                mapping[idx] = canonical
                break
    return mapping


def _find_header_row(rows: list[list], scan: int = 20) -> tuple[int, dict[int, str]]:
    best_row, best_map = -1, {}
    for i, row in enumerate(rows[:scan]):
        m = _build_header_index(row)
        if len(m) > len(best_map):
            best_row, best_map = i, m
    return best_row, best_map


def parse_sheet(rows: list[list]) -> list[dict]:
    """Parse one sheet's rows (list of lists) into canonical row dicts."""
    header_row, header_map = _find_header_row(rows)
    if header_row < 0 or len(header_map) < 2:
        return []
    parsed: list[dict] = []
    for row in rows[header_row + 1:]:
        record = {field: None for field in COLUMN_MAP}
        has_value = False
        for idx, field in header_map.items():
            val = row[idx] if idx < len(row) else None
            if val not in (None, ""):
                record[field] = val
                has_value = True
        if has_value:
            parsed.append(record)
    return parsed


def parse_workbook(source, sheet_names: list[str] | None = None) -> dict:
    """Parse a workbook (path or bytes) → {"rows": [...], "sheets": n, "skipped_sheets": [...]}.

    Skips obvious reference sheets (Reference / SENARAI KPI) unless explicitly requested.
    """
    if isinstance(source, (bytes, bytearray)):
        wb = openpyxl.load_workbook(io.BytesIO(source), data_only=True, read_only=True)
    else:
        wb = openpyxl.load_workbook(source, data_only=True, read_only=True)

    all_rows: list[dict] = []
    used, skipped = 0, []
    for ws in wb.worksheets:
        if sheet_names is not None and ws.title not in sheet_names:
            continue
        if sheet_names is None and re.search(r"reference|senarai", ws.title, re.I):
            skipped.append(ws.title)
            continue
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
        sheet_rows = parse_sheet(rows)
        if sheet_rows:
            used += 1
            all_rows.extend(sheet_rows)
    return {"rows": all_rows, "sheets": used, "skipped_sheets": skipped}


def missing_fields(record: dict) -> list[str]:
    """Return the list of missing mandatory fields for a parsed record."""
    return [f for f in MANDATORY_FIELDS if not record.get(f)]
