"""Audit repository (CP5) — read + append only. Intentionally NO update/delete methods."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operational.governance import AuditLog


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, audit_id: str) -> AuditLog | None:
        return self.db.get(AuditLog, audit_id)

    def list(
        self,
        *,
        actor_id: str | None = None,
        entity_type: str | None = None,
        action: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AuditLog]:
        stmt = select(AuditLog)
        if actor_id:
            stmt = stmt.where(AuditLog.actor_id == actor_id)
        if entity_type:
            stmt = stmt.where(AuditLog.entity_type == entity_type)
        if action:
            stmt = stmt.where(AuditLog.action == action)
        stmt = stmt.order_by(AuditLog.created_at.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(stmt))

    # NOTE: no update()/delete() — AuditLog is append-only (BR-009/029).
