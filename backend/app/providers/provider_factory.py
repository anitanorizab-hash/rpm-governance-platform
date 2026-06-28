"""Provider factory (CP2) — config-driven selection.

The ONLY place the app resolves a concrete provider. Business logic calls get_llm_provider() /
get_embedding_provider() and uses the abstract interface — switching provider = config change only.
"""
from __future__ import annotations

from app.core.config import get_settings
from app.providers.base import (
    BaseEmbeddingProvider,
    BaseLLMProvider,
    ProviderConfigurationError,
)
from app.providers.groq_provider import GroqProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.embedding_provider import (
    OpenAIEmbeddingProvider,
    SentenceTransformerEmbeddingProvider,
)

_LLM_REGISTRY = {
    "groq": GroqProvider,
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
}

_EMBEDDING_REGISTRY = {
    "sentence-transformer": SentenceTransformerEmbeddingProvider,
    "openai": OpenAIEmbeddingProvider,
}


def get_llm_provider() -> BaseLLMProvider:
    cfg = get_settings()
    name = (cfg.get("llm_provider") or "groq").strip().lower()
    cls = _LLM_REGISTRY.get(name)
    if cls is None:
        raise ProviderConfigurationError(
            f"Unknown llm_provider '{name}' in config.md. "
            f"Valid options: {sorted(_LLM_REGISTRY)}."
        )
    return cls()


def get_embedding_provider() -> BaseEmbeddingProvider:
    cfg = get_settings()
    name = (cfg.get("embedding_provider") or "sentence-transformer").strip().lower()
    cls = _EMBEDDING_REGISTRY.get(name)
    if cls is None:
        raise ProviderConfigurationError(
            f"Unknown embedding_provider '{name}' in config.md. "
            f"Valid options: {sorted(_EMBEDDING_REGISTRY)}."
        )
    model = cfg.get("embedding_model")
    return cls(model) if model else cls()


def providers_health() -> dict:
    """Aggregate health for the active LLM + embedding providers (no secrets, no network)."""
    cfg = get_settings()
    result = {"mode": cfg.get("mode"), "llm": None, "embedding": None, "errors": []}
    try:
        result["llm"] = get_llm_provider().health_check()
    except ProviderConfigurationError as e:
        result["errors"].append(str(e))
    try:
        result["embedding"] = get_embedding_provider().health_check()
    except ProviderConfigurationError as e:
        result["errors"].append(str(e))
    return result
