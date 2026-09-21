import pytest

from Application.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_index(client):
    response = client.get("/")
    data = response.get_json()

    assert response.status_code == 200
    assert data["application"] == "System Health API"
    assert data["endpoints"] == ["/health", "/system", "/version"]


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_system(client):
    response = client.get("/system")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data["hostname"], str)
    assert isinstance(data["cpu_usage"], float)
    assert isinstance(data["memory_usage"], float)
    assert isinstance(data["disk_usage"], float)
    assert isinstance(data["uptime_seconds"], int)
    assert 0 <= data["cpu_usage"] <= 100
    assert 0 <= data["memory_usage"] <= 100
    assert 0 <= data["disk_usage"] <= 100
    assert data["uptime_seconds"] >= 0


def test_version_uses_default(client):
    response = client.get("/version")

    assert response.status_code == 200
    assert response.get_json() == {"version": "development"}


def test_version_uses_environment_variable(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "test-version")
    response = client.get("/version")

    assert response.status_code == 200
    assert response.get_json() == {"version": "test-version"}
