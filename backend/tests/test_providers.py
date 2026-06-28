"""CP2 tests: config loading, provider selection, missing-key handling, provider health endpoint."""
import importlib

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import get_settings
from app.providers.base import ProviderConfigurationError
from app.providers import provider_factory as pf
from app.providers.groq_provider import GroqProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.embedding_provider import SentenceTransformerEmbeddingProvider

client = TestClient(app)


def test_config_loads_provider_settings():
    s = get_settings()
    assert s["mode"] in ("development", "testing", "production")
    assert s["llm_provider"]  # present
    assert s["embedding_provider"]


def test_active_llm_provider_selection():
    # development default = groq
    provider = pf.get_llm_provider()
    assert isinstance(provider, GroqProvider)


def test_active_embedding_provider_selection():
    provider = pf.get_embedding_provider()
    assert isinstance(provider, SentenceTransformerEmbeddingProvider)


def test_missing_api_key_raises_clear_error(monkeypatch):
    # Ensure no Groq key, then chat() must raise a clear, key-free error (no silent crash).
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(ProviderConfigurationError) as exc:
        GroqProvider().chat([{"role": "user", "content": "hi"}])
    msg = str(exc.value)
    assert "GROQ_API_KEY" in msg          # names the missing key
    assert "sk-" not in msg               # never leaks a key value


def test_unknown_provider_raises(monkeypatch):
    monkeypatch.setattr(pf, "get_settings", lambda: {"llm_provider": "does-not-exist"})
    with pytest.raises(ProviderConfigurationError):
        pf.get_llm_provider()


def test_provider_health_endpoint():
    r = client.get("/api/v1/health/providers")
    assert r.status_code == 200
    body = r.json()
    assert "llm" in body and "embedding" in body
    assert body["llm"]["provider"] == "groq"
    assert body["llm"]["kind"] == "llm"
    assert "status" in body["llm"]
    # embedding (local) is available without a key
    assert body["embedding"]["provider"] == "sentence-transformer"
    # no secret values anywhere in the response
    assert "API_KEY" not in r.text and "sk-" not in r.text
