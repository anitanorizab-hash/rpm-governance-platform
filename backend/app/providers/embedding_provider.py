"""Embedding providers (CP2) — independent of the LLM provider (TRD §17.2).

- SentenceTransformerEmbeddingProvider: local, no API key (dev default). Heavy deps imported lazily.
- OpenAIEmbeddingProvider: requires OPENAI_API_KEY (dev fallback / production).
Both raise a clear ProviderConfigurationError when unusable; neither leaks secrets.
"""
from __future__ import annotations

from app.core.env import get_secret, has_secret
from app.providers.base import BaseEmbeddingProvider, ProviderConfigurationError


class SentenceTransformerEmbeddingProvider(BaseEmbeddingProvider):
    name = "sentence-transformer"
    env_key = None  # local model; no API key required

    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        self.model = model

    def embed(self, texts: list[str], **kwargs) -> list[list[float]]:
        try:
            from sentence_transformers import SentenceTransformer  # lazy; installed when RAG is built
        except ImportError as exc:
            raise ProviderConfigurationError(
                "sentence-transformers not installed. Run: pip install sentence-transformers "
                "(or set embedding_provider: openai in config.md)."
            ) from exc
        model = SentenceTransformer(self.model)
        return [v.tolist() for v in model.encode(texts)]

    def health_check(self) -> dict:
        # Local provider needs no key; the heavy package is installed on demand (CP RAG step).
        return {
            "provider": self.name,
            "kind": "embedding",
            "configured": True,
            "status": "available_on_demand",
            "model": self.model,
            "requires_key": False,
        }


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    name = "openai"
    env_key = "OPENAI_API_KEY"

    def __init__(self, model: str = "text-embedding-3-large"):
        self.model = model

    def embed(self, texts: list[str], **kwargs) -> list[list[float]]:
        if not has_secret(self.env_key):
            raise ProviderConfigurationError(
                "OpenAI embeddings selected but OPENAI_API_KEY is not set. Add it to .env."
            )
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ProviderConfigurationError("OpenAI SDK not installed. Run: pip install openai") from exc
        client = OpenAI(api_key=get_secret(self.env_key))
        resp = client.embeddings.create(model=self.model, input=texts)
        return [d.embedding for d in resp.data]

    def health_check(self) -> dict:
        configured = has_secret(self.env_key)
        return {
            "provider": self.name,
            "kind": "embedding",
            "configured": configured,
            "status": "configured" if configured else "not_configured",
            "model": self.model,
            "requires_key": True,
        }
