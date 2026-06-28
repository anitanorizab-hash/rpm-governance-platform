"""Aggregate all models so Base.metadata is complete (for Alembic / create_all)."""
from app.models import operational  # noqa: F401
from app.models import knowledge    # noqa: F401
from app.models import ai           # noqa: F401
