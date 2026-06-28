"""Declarative Base, naming convention, and shared mixins (CP3).

No model imports here (avoids circular imports). Models import from this module;
`app.models` aggregates every model so Base.metadata is complete for Alembic/create_all.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base

# Stable naming convention → deterministic constraint names (good for migrations).
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

Base = declarative_base()
Base.metadata.naming_convention = NAMING_CONVENTION


def _now() -> datetime:
    return datetime.now(timezone.utc)


def uuid_pk() -> Column:
    """Return a fresh UUID (string) primary key Column."""
    return Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))


def fk_uuid(target: str, **kw) -> Column:
    """Foreign key column holding a UUID string."""
    from sqlalchemy import ForeignKey
    return Column(String(36), ForeignKey(target), **kw)


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now, nullable=False)


class CreatedAtMixin:
    """For append-only tables (e.g. AuditLog) — no updated_at by design."""
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)
