import datetime
import http
import uuid

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from sample_backend.entities import db_models
from sample_backend.interface import routers
from sample_backend.tests.utils import get_endpoint_url


@pytest.mark.integrated
async def test_notes_get_all_with_paging(test_client: TestClient, db_session: AsyncSession) -> None:
    """Test the paging across all layers of the application for Notes."""
    # Arrange ======
    # A unique category for the test enabling to filter out the data belonging to this test.
    category = f"test {uuid.uuid4()}"

    # TODO refactor with factory boy
    # Excluded notes have a future creation date, so that they'll be returned first,
    # and omitted with the offset.
    excluded_notes = [
        db_models.Note(
            contents="excluded 1",
            category=category,
            creation_date=datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(days=1),
        )
    ]
    included_notes = [
        db_models.Note(contents="included 1", category=category),
        db_models.Note(contents="included 2", category=category),
    ]
    # Excluded need to be first, because of the creation time ordering.
    for note in excluded_notes + included_notes:
        db_session.add(note)
    await db_session.flush()

    # Act ======
    url = get_endpoint_url(
        endpoint_name=routers.notes.get_all_notes.__name__,
        query_parameters={"offset": 1, "limit": 2, "category": category},
    )
    response = test_client.get(url=url)

    # Assert ======
    assert response.status_code == http.HTTPStatus.OK
    returned_notes = response.json()

    assert {note["contents"] for note in returned_notes} == {note.contents for note in included_notes}
