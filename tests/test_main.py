from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_name_and_version() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"name": "gha-lab-app", "version": "0.1.0"}


def test_health_returns_healthy() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_config_check_reports_missing_env(monkeypatch) -> None:
    monkeypatch.delenv("APP_ENV", raising=False)

    response = client.get("/config-check")

    assert response.status_code == 200
    assert response.json() == {
        "variable": "APP_ENV",
        "configured": False,
        "value": None,
    }


def test_config_check_reports_env(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")

    response = client.get("/config-check")

    assert response.status_code == 200
    assert response.json() == {
        "variable": "APP_ENV",
        "configured": True,
        "value": "test",
    }


def test_fail_demo_is_intentionally_broken() -> None:
    response = client.get("/fail-demo")

    assert response.status_code == 500
    assert "Intentional failure" in response.json()["detail"]

