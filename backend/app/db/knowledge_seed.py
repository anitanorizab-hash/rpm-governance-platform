"""RPM 2026-2035 knowledge seed (V1.1.2) — registers + processes a demo policy reference so the
RAG chatbot can answer policy questions (e.g. infrastructure). Idempotent. Uses KnowledgeService,
so the content is chunked and keyword/embedding searchable, and answers carry a citation.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.knowledge.knowledge import KnowledgeSource

RPM_TITLE = "RPM 2026-2035 Strategic Overview"

# Demo strategic-overview sample (clearly labelled). Covers all seven Teras, including infrastructure.
RPM_CONTENT = (
    "RPM 2026-2035 (Rancangan Pemajuan Malaysia) — Strategic Overview. "
    "The national education plan is organised into seven strategic pillars (Teras):\n"
    "Teras 1 — Access to Quality Education: equitable enrolment and retention across all regions.\n"
    "Teras 2 — Equity and Inclusion: closing achievement gaps for B40, rural and special-needs pupils.\n"
    "Teras 3 — Education Quality: curriculum, pedagogy, assessment and teacher competency.\n"
    "Teras 4 — Efficiency of Delivery and Infrastructure: this Teras focuses on school infrastructure, "
    "physical facilities, and digital infrastructure. It covers building and upgrading classrooms and "
    "learning facilities, internet connectivity, ICT devices and digital learning platforms for schools.\n"
    "Teras 5 — Talent Development: leadership, professional development and future-ready skills.\n"
    "Teras 6 — Governance and Accountability: data-driven monitoring, audit and transparency.\n"
    "Teras 7 — Financial Sustainability: outcome-based budgeting (OBB) and low-cost high-impact investment.\n"
    "On infrastructure: RPM prioritises safe school buildings, adequate classrooms and reliable digital "
    "infrastructure (connectivity, devices and learning platforms). Infrastructure, facilities and digital "
    "infrastructure are addressed under Teras 4 (Efficiency of Delivery and Infrastructure). "
    "Human review and approval is mandatory before any official report or notification is issued."
)


def seed_rpm_knowledge(db: Session, actor_id: str | None = None) -> str:
    """Create (if missing) + process the RPM knowledge source. Returns the source id."""
    from app.services.knowledge_service import KnowledgeService  # local import (avoids cycles)
    svc = KnowledgeService(db)
    existing = db.scalar(select(KnowledgeSource).where(KnowledgeSource.title == RPM_TITLE))
    if existing:
        svc.process_source(actor_id=actor_id, source_id=existing.id)
        return existing.id
    src = svc.create_source(actor_id=actor_id, data={
        "type": "static", "title": RPM_TITLE, "category": "rpm",
        "format": "md", "content": RPM_CONTENT,
    })
    svc.process_source(actor_id=actor_id, source_id=src.id)
    return src.id
