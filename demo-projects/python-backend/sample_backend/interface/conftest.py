from fastapi.testclient import TestClient
import pytest

from sample_backend.main import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
