import http

from fastapi.testclient import TestClient


def test_healthcheck(test_client: TestClient) -> None:
    response = test_client.get("/")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json()["status"] == "up"
