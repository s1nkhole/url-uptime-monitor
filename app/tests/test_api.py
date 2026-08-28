"""Простые тесты API. Запуск: pytest app/tests -v"""
import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient

from app.db import init_db
from app.main import app

init_db()
client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_metrics_endpoint():
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "text/plain" in resp.headers["content-type"]


def test_create_and_list_target():
    create_resp = client.post("/targets", json={"url": "https://example.com"})
    assert create_resp.status_code == 201
    assert create_resp.json()["current_status"] == "unknown"

    list_resp = client.get("/targets")
    urls = [t["url"] for t in list_resp.json()]
    assert "https://example.com/" in urls


def test_duplicate_target_rejected():
    client.post("/targets", json={"url": "https://dupe.example.com"})
    resp = client.post("/targets", json={"url": "https://dupe.example.com"})
    assert resp.status_code == 409


def test_history_for_unknown_target_404s():
    resp = client.get("/targets/does-not-exist/history")
    assert resp.status_code == 404
