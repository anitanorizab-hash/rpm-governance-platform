"""Groq LLM provider (CP2 — development default).

SDK is imported lazily so the app/tests run without the package or a key. chat() raises a clear
ProviderConfigurationError when the key is missing; it never crashes silently or leaks the key.
"""
from __future__ import annotations

from app.core.env import get_secret, has_secret
from app.providers.base import BaseLLMProvider, ProviderConfigurationError


class GroqProvider(BaseLLMProvider):
    name = "groq"
    env_key = "GROQ_API_KEY"

    def chat(self, messages: list[dict], model: str | None = None, **kwargs) -> str:
        if not has_secret(self.env_key):
            raise ProviderConfigurationError(
                "Groq is the active LLM provider but GROQ_API_KEY is not set. "
                "Add it to .env (never to config.md)."
            )
        try:
            from groq import Groq  # lazy import; installed when Groq is actually used
        except ImportError as exc:
            raise ProviderConfigurationError(
                "Groq SDK not installed. Run: pip install groq"
            ) from exc
        client = Groq(api_key=get_secret(self.env_key))
        resp = client.chat.completions.create(
            model=model or "llama-3.3-70b-versatile", messages=messages, **kwargs
        )
        return resp.choices[0].message.content

    def health_check(self) -> dict:
        configured = has_secret(self.env_key)
        return {
            "provider": self.name,
            "kind": "llm",
            "configured": configured,
            "status": "configured" if configured else "not_configured",
        }
