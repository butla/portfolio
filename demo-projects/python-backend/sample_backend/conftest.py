from collections.abc import AsyncIterator
import contextlib

import pytest
import pytest_asyncio
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from sample_backend import connectors
from sample_backend.core.config import SETTINGS


@pytest.fixture(scope="session")
def _init_db_session_creator() -> None:
    connectors.db.init_db_session_creator(database_url=SETTINGS.postgres_url)


@pytest_asyncio.fixture
async def db_session(mocker: MockerFixture, _init_db_session_creator: None) -> AsyncIterator[AsyncSession]:
    """
    Use this when constructing production code objects that require an async DB session.

    This is to be used in integrated and external tests.

    This rolls back the transaction before applying it, so we won't dump data to the database.
    """
    # Using _SessionMaker directly to not get the commit() from get_db_session.
    # `get_db_session` is tested in external tests.
    async with connectors.db._SessionMaker() as only_session:  # type: ignore[misc] # noqa: SLF001

        @contextlib.asynccontextmanager
        async def mock_session_maker() -> AsyncIterator[AsyncSession]:
            yield only_session

        # Mocking the session maker is easier than mocking get_db_session
        # because of the Depends usage from Fastapi.
        mocker.patch.object(connectors.db, "_SessionMaker", mock_session_maker)

        yield only_session
        # Nothing gets commited, so the tests run a bit faster.
        await only_session.rollback()
