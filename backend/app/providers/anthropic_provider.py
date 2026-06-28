"""Anthropic LLM provider (CP2 — production option). Lazy SDK import; safe missing-key handling."""
from __future__ import annotations

from app.core.env import get_secret, has_secret
from app.providers.base import BaseLLMProvider, ProviderConfigurationError


class AnthropicProvider(BaseLLMProvider):
    name = "anthropic"
    env_key = "ANTHROPIC_API_KEY"

    def chat(self, messages: list[dict], model: str | None = None, max_tokens: int = 1024, **kwargs) -> str:
        if not has_secret(self.env_key):
            raise ProviderConfigurationError(
                "Anthropic is the active LLM provider but ANTHROPIC_API_KEY is not set. Add it to .env."
            )
        try:
            import anthropic
        except ImportError as exc:
            raise ProviderConfigurationError(
                "Anthropic SDK not installed. Run: pip install anthropic"
            ) from exc
        client = anthropic.Anthropic(api_key=get_secret(self.env_key))
        # Anthropic separates system from messages; pass through simply for CP2.
        resp = client.messages.create(
            model=model or "claude-3-5-sonnet-latest",
            max_tokens=max_tokens,
            messages=messages,
            **kwargs,
        )
        return resp.content[0].text

    def health_check(self) -> dict:
        configured = has_secret(self.env_key)
        return {
            "provider": self.name,
            "kind": "llm",
            "configured": configured,
            "status": "configured" if configured else "not_configured",
        }
