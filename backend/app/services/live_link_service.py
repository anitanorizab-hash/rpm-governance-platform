"""Live link service (CP14): register + admin-validate. Links are used by RAG only after validation."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.audit import AuditContext
from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.audit_service import AuditService


class LiveLinkService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = KnowledgeRepository(db)
        self.audit = AuditService(db)

    def register(self, *, actor_id, data: dict, context: AuditContext | None = None):
        # Source starts pending_validation → excluded from retrieval until validated.
        source = self.repo.create_source(
            type="live", title=data.get("title"), category=data.get("category"),
            reliability=data.get("reliability", "unverified"), status="pending_validation",
        )
        link = self.repo.create_live_link(source_id=source.id, url=data["url"],
                                           refresh_schedule=data.get("refresh_schedule"))
        self.audit.record(entity_type="live_link", entity_id=link.id, action="live_link_register",
                          actor_id=actor_id, after={"url": data["url"], "status": "pending_validation"},
                          context=context, commit=False)
        self.db.commit()
        return {"source_id": source.id, "link_id": link.id, "status": "pending_validation"}

    def validate(self, *, actor_id, link_id, context: AuditContext | None = None):
        link = self.repo.get_live_link(link_id)
        if not link:
            return None
        source = self.repo.get_source(link.source_id)
        self.repo.set_status(source, "active", validated_by=actor_id)
        link.status = "active"
        link.last_checked = datetime.now(timezone.utc)
        self.audit.record(entity_type="live_link", entity_id=link_id, action="live_link_validate",
                          actor_id=actor_id, after={"status": "active"}, context=context, commit=False)
        self.db.commit()
        return {"link_id": link_id, "source_id": source.id, "status": "active"}
