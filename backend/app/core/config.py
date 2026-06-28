"""Core configuration loader (CP1 minimal).

Reads the active profile's app_name / mode / version from config.md for the health endpoint.
Secrets are read from environment (.env) — NOT from config.md. Full provider/DB wiring lands in CP2/CP3.
"""
from __future__ import annotations

import os
import re
from functools import lru_cache
from pathlib import Path

# config.md lives at the backend root (one level above app/)
CONFIG_MD_PATH = Path(__file__).resolve().parents[2] / "config.md"

# Safe defaults if config.md is missing or unparsable (CP1 must still start).
_DEFAULTS = {
    "app_name": "Agentic AI Strategic Governance Platform",
    "mode": "development",
    "version": "0.1.0",
    "cors_origins": ["http://localhost:5173"],
    # provider defaults (development): LLM=Groq, embeddings=local sentence-transformer
    "llm_provider": "groq",
    "llm_model": "llama-3.3-70b-versatile",
    "embedding_provider": "sentence-transformer",
    "embedding_model": "all-MiniLM-L6-v2",
}

# Keys read from the active profile in config.md (CP2 adds provider keys).
_PROFILE_KEYS = (
    "app_name", "mode", "version",
    "llm_provider", "llm_model", "embedding_provider", "embedding_model",
    "database_url", "vector_store",
)


def _parse_active_profile(text: str) -> str:
    m = re.search(r"##\s*active_profile\s*\n+\s*([A-Za-z0-9_-]+)", text)
    return (m.group(1).strip() if m else os.getenv("APP_PROFILE", "development"))


def _parse_profile_block(text: str, profile: str) -> dict:
    """Extract key: value lines under '### <profile>' until the next heading."""
    pattern = rf"###\s*{re.escape(profile)}\s*\n(.*?)(?=\n#{{1,3}}\s|\Z)"
    m = re.search(pattern, text, re.DOTALL)
    values: dict[str, str] = {}
    if not m:
        return values
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith("-") and ":" in line:
            key, _, val = line[1:].partition(":")
            # drop inline comments
            val = val.split("#", 1)[0].strip()
            values[key.strip()] = val
    return values


@lru_cache(maxsize=1)
def get_settings() -> dict:
    """Return resolved settings for the active profile (CP1 keys only)."""
    settings = dict(_DEFAULTS)
    try:
        text = CONFIG_MD_PATH.read_text(encoding="utf-8")
        profile = os.getenv("APP_PROFILE") or _parse_active_profile(text)
        block = _parse_profile_block(text, profile)
        for key in _PROFILE_KEYS:
            if block.get(key):
                settings[key] = block[key]
        settings["profile"] = profile
    except FileNotFoundError:
        settings["profile"] = os.getenv("APP_PROFILE", "development")
    return settings
