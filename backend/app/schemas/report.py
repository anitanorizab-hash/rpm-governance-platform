"""Report schemas (CP17)."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ReportGenerateIn(BaseModel):
    period: str = Field(min_length=4)        # e.g. 2026-01
    type: str = "monthly"


class ReportPatchIn(BaseModel):
    title: str | None = None
    summary: str | None = None


class ReportOut(BaseModel):
    id: str
    title: str | None = None
    period: str | None = None
    type: str | None = None
    status: str
    summary: str | None = None
    reject_reason: str | None = None
    approval_id: str | None = None
    generated_by: str | None = None
    content: dict = {}


class SubmitForReviewOut(BaseModel):
    report_id: str
    approval_id: str
    approval_state: str
    report_status: str
