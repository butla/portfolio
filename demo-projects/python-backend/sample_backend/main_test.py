"""A sample external tests' file."""

import http
import uuid

import httpx
import pytest
import tenacity

from sample_backend.tests.config import AppTestsConfig


# Scope is session, so that this fixture runs only once during the test suite.
# If we'd have more tests, we don't need to go through waiting for the app again.
@pytest.fixture(scope="session")
def app_url() -> str:
    app_address = f"http://localhost:{AppTestsConfig().api_port}"
    _wait_for_http_url(app_address)
    return app_address


@tenacity.retry(stop=tenacity.stop_after_delay(10), wait=tenacity.wait_fixed(0.2), reraise=True)
def _wait_for_http_url(url: str) -> None:
    """
    Waits for the app running in Docker to become responsive.

    If the tests run immediately after the containers have started, they will need to wait a moment for the
    app to become responsive.
    """
    result = httpx.get(url)
    if result.status_code != http.HTTPStatus.OK:
        raise ValueError("App returned the wrong status code")


@pytest.mark.external
def test_store_and_retrieve_note(app_url: str) -> None:
    """Check that the app runs correctly in the Docker container."""
    note_contents = f"first note {uuid.uuid4()}"
    create_result = httpx.post(
        f"{app_url}/notes/",
        json={"contents": note_contents},
    )
    assert create_result.status_code == http.HTTPStatus.CREATED
    assert create_result.json()["contents"] == note_contents
    note_id = create_result.json()["id"]

    get_result = httpx.get(f"{app_url}/notes/{note_id}/")
    assert get_result.status_code == http.HTTPStatus.OK
    assert get_result.json()["contents"] == note_contents

    get_all_result = httpx.get(f"{app_url}/notes/")
    assert next(note for note in get_all_result.json() if note["id"] == note_id)


@pytest.mark.non_parallel
@pytest.mark.external
def test_app_image_handles_shutdown_signal() -> None:
    assert True
    # TODO implement
    # Flow:
    # - docker compose down api
    # - see that it emits the "shutting down" log message, meaning that it handles SIGTERM correctly
    # - docker compose up -d api
