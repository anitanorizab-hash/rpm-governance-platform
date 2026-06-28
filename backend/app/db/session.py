"""Database engine & session (CP3). Base now lives in app.db.base."""
from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.db.base import Base  # re-exported for convenience

# Resolution order: DATABASE_URL (.env, prod) → config.md database_url → sqlite dev default.
_settings = get_settings()
DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or _settings.get("database_url")
    or "sqlite:///./app_dev.db"
)

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

__all__ = ["engine", "SessionLocal", "Base", "get_db", "DATABASE_URL"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
