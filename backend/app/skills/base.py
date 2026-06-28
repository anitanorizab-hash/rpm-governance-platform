"""Skill base (CP12). Skills are reusable, modular, structured-output capabilities.

Rules: skills compute/draft only — they NEVER approve/delete/amend/send official outputs.
Deterministic skills must not call a provider; AI-assisted skills use the provider adapter only
and return a safe fallback when the provider is unavailable.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Skill(ABC):
    name: str = "base"
    description: str = ""
    deterministic: bool = True
    uses_provider: bool = False
    version: str = "1.0"

    @abstractmethod
    def run(self, payload: dict) -> dict:
        """Return a structured result dict. Pure where possible (no DB side-effects)."""

    def metadata(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "deterministic": self.deterministic,
            "uses_provider": self.uses_provider,
            "version": self.version,
        }


def safe_chat(messages: list[dict], *, fallback: str) -> dict:
    """Call the LLM via the provider adapter; return safe fallback if unavailable.

    Returns {"text": str, "source": "ai"|"fallback"}. Never raises for missing key/SDK.
    """
    try:
        from app.providers.provider_factory import get_llm_provider
        from app.providers.base import ProviderConfigurationError
        provider = get_llm_provider()
        try:
            text = provider.chat(messages)
            return {"text": text, "source": "ai"}
        except ProviderConfigurationError:
            return {"text": fallback, "source": "fallback"}
    except Exception:
        # Any provider/import error → safe fallback (never crash a skill).
        return {"text": fallback, "source": "fallback"}
