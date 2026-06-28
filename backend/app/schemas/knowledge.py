"""Knowledge / RAG schemas (CP14)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class KnowledgeSourceCreateIn(BaseModel):
    type: str = "static"                 # static | live
    title: str
    description: str | None = None
    category: str | None = None          # rpm | policy | guideline | circular | note | project
    reliability: str = "trusted"
    format: str | None = "txt"           # txt | md | pdf | docx
    filename: str | None = None
    content: str | None = None           # raw text (txt/md) or base64 (pdf/docx)


class KnowledgeSourceOut(BaseModel):
    id: str
    type: str
    title: str | None = None
    category: str | None = None
    reliability: str | None = None
    status: str
    validated_by: str | None = None
    created_at: datetime

    @classmethod
    def from_model(cls, m) -> "KnowledgeSourceOut":
        return cls(id=m.id, type=m.type, title=m.title, category=m.category,
                   reliability=m.reliability, status=m.status, validated_by=m.validated_by,
                   created_at=m.created_at)


class LiveLinkCreateIn(BaseModel):
    title: str
    url: str
    category: str | None = None
    reliability: str = "unverified"
    refresh_schedule: str | None = None


class QueryIn(BaseModel):
    query: str
    top_k: int = 5


class QueryOut(BaseModel):
    query: str
    grounded: bool
    fallback: bool
    answer: str
    citations: list[dict] = []
    mode: str
