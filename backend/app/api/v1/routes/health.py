"""Health check API (A6 G18). CP1 — liveness + readiness stub."""
from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict:
    """Liveness: returns status, app name, mode, version."""
    s = get_settings()
    return {
        "status": "ok",
        "app_name": s.get("app_name"),
        "mode": s.get("mode"),
        "version": s.get("version"),
    }


@router.get("/ready")
def ready() -> dict:
    """Readiness stub (DB/provider/vector checks wired in later coding prompts)."""
    return {"status": "ready", "checks": {"db": "pending", "provider": "pending", "vector": "pending"}}


@router.get("/providers")
def providers() -> dict:
    """Active LLM + embedding provider health (CP2). No secrets, no network calls."""
    from app.providers.provider_factory import providers_health

    return providers_health()

