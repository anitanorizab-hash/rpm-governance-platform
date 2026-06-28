"""CP1 smoke test: /api/v1/health returns the expected shape."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    for key in ("app_name", "mode", "version"):
        assert key in body and body[key]


def test_ready_stub():
    r = client.get("/api/v1/health/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"
