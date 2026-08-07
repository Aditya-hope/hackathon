"""
Smoke test for the FastAPI application.

Verifies the app boots (dependency graph wires up cleanly with no
provider keys configured) and the health endpoint reports correctly -
this is the "working code, demonstrable" non-negotiable exercised as
an automated test rather than only a manual `uvicorn` run.
"""

from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_health_endpoint_returns_healthy():
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "healthy"
    assert body["application"]
    assert body["version"]
    assert isinstance(body["providers_configured"], list)


def test_root_endpoint_reports_running():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_docs_are_available():
    response = client.get("/docs")

    assert response.status_code == 200


def test_process_invoice_text_rejects_empty_text():
    response = client.post(
        "/process-invoice-text",
        json={"text": "   "},
    )

    assert response.status_code == 400
