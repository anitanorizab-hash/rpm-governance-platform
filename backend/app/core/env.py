"""Environment / secrets loader (CP2).

Secrets live ONLY in .env (never in config.md or code). This module loads them and exposes
presence checks. It NEVER returns or logs secret values except to the provider that needs them.
"""
from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    # backend/.env (one level above app/)
    _ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=_ENV_PATH)
except Exception:  # dotenv optional; env vars may be set by the OS/secrets manager
    pass

# Known secret names (documented in .env.example).
SECRET_NAMES = (
    "GROQ_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "JWT_SECRET_KEY",
    "DATABASE_URL",
)


def get_secret(name: str) -> str | None:
    """Return a secret value for internal use by the component that needs it (never logged)."""
    return os.getenv(name)


def has_secret(name: str) -> bool:
    """True if the secret is set and non-empty."""
    val = os.getenv(name)
    return bool(val and val.strip())


def secret_status() -> dict[str, str]:
    """Masked status for diagnostics: 'set' or 'missing' — NEVER the value."""
    return {name: ("set" if has_secret(name) else "missing") for name in SECRET_NAMES}
