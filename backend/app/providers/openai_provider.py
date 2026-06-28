"""OpenAI LLM provider (CP2 — production option). Lazy SDK import; safe missing-key handling."""
from __future__ import annotations

from app.core.env import get_secret, has_secret
from app.providers.base import BaseLLMProvider, ProviderConfigurationError


class OpenAIProvider(BaseLLMProvider):
    name = "openai"
    env_key = "OPENAI_API_KEY"

    def chat(self, messages: list[dict], model: str | None = None, **kwargs) -> str:
        if not has_secret(self.env_key):
            raise ProviderConfigurationError(
                "OpenAI is the active LLM provider but OPENAI_API_KEY is not set. Add it to .env."
            )
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ProviderConfigurationError("OpenAI SDK not installed. Run: pip install openai") from exc
        client = OpenAI(api_key=get_secret(self.env_key))
        resp = client.chat.completions.create(
            model=model or "gpt-4o", messages=messages, **kwargs
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
