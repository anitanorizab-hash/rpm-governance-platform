"""Completeness service (CP7): detect missing mandatory KPI fields (BR-004/005/006)."""
from __future__ import annotations

MANDATORY = ("statement", "indicator", "target", "pic_name", "pic_email", "department", "teras")


def kpi_missing_fields(kpi) -> list[str]:
    """Return missing mandatory fields for a KPI model (with relationships loaded)."""
    missing = []
    if not kpi.statement:
        missing.append("statement")
    if not (kpi.indicators and any(i.indicator_text for i in kpi.indicators)):
        missing.append("indicator")
    if not (kpi.targets and any(t.target_value for t in kpi.targets)):
        missing.append("target")
    pic = kpi.pic
    if not (pic and pic.name):
        missing.append("pic_name")
    if not (pic and pic.email):
        missing.append("pic_email")
    if not (kpi.sector or kpi.department_id):
        missing.append("department")
    if not kpi.teras_id:
        missing.append("teras")
    return missing


def is_complete(kpi) -> bool:
    return not kpi_missing_fields(kpi)
