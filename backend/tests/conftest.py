"""Shared test fixtures (CP4): isolated in-memory DB + TestClient with dependency override."""
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Deterministic JWT secret for tests (never used in production).
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")

from app.db.base import Base
import app.models  # noqa: F401  (populate metadata)
from app.db.seed import seed_reference_data
from app.db.session import get_db
from app.main import app

# Hermetic tests: importing the app runs load_dotenv(), which would pull a developer's real LLM keys
# from backend/.env into the environment. Scrub them so AI-assisted skills/agents take their
# deterministic fallback path (no external API calls, no flakiness) — matching the "without key" tests.
for _provider_key in ("GROQ_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
    os.environ.pop(_provider_key, None)


@pytest.fixture()
def db_session():
    # StaticPool => one shared in-memory connection across threads (TestClient runs in a worker thread).
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)
    with TestingSession() as s:
        seed_reference_data(s)
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def make_admin(db_session):
    """Promote a registered user to super_admin directly (DB), bypassing the API."""
    from app.repositories.user_repository import UserRepository

    def _promote(email: str):
        repo = UserRepository(db_session)
        user = repo.get_by_email(email)
        role = repo.get_role_by_name("super_admin")
        repo.set_roles(user, ["super_admin"])
        db_session.commit()
        return user
    return _promote
