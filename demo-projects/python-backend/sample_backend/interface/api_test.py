import http

from fastapi.testclient import TestClient
import pytest

from sample_backend.main import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


def test_healthcheck(test_client: TestClient) -> None:
    response = test_client.get("/")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["status"] == "up"
