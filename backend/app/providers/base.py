"""Provider abstraction base (CP2).

Business logic depends ONLY on these interfaces — never on a concrete vendor SDK (BR-044/AD-001).
LLM provider and Embedding provider are independent (TRD §17.2).
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class ProviderConfigurationError(Exception):
    """Raised when a provider is selected but not usable (e.g. missing API key).

    Carries a clear, safe message — it must NEVER include secret values.
    """


class BaseLLMProvider(ABC):
    """Uniform LLM interface: chat() + health_check()."""

    name: str = "base-llm"
    env_key: str | None = None

    @abstractmethod
    def chat(self, messages: list[dict], **kwargs) -> str:
        """Return the model's text response for a list of {role, content} messages."""

    @abstractmethod
    def health_check(self) -> dict:
        """Return a status dict (no secrets, no network call by default)."""


class BaseEmbeddingProvider(ABC):
    """Uniform embedding interface: embed() + health_check()."""

    name: str = "base-embedding"
    env_key: str | None = None

    @abstractmethod
    def embed(self, texts: list[str], **kwargs) -> list[list[float]]:
        """Return one embedding vector per input text."""

    @abstractmethod
    def health_check(self) -> dict:
        """Return a status dict (no secrets, no network call by default)."""
