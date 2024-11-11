from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from sample_backend import connectors
from sample_backend.core.config import SETTINGS


@pytest.fixture(scope="session")
def _init_db_session_creator() -> None:
    connectors.db.init_db_session_creator(SETTINGS.postgres_url)


@pytest_asyncio.fixture
async def db_session(_init_db_session_creator: None) -> AsyncIterator[AsyncSession]:
    """
    Use this when constructing production code objects that require an async DB session.

    This is to be used in integrated and external tests.

    This rolls back the transaction before applying it, so we won't dump data to the database.
    """
    session = await anext(connectors.db.get_db_session())
    yield session
    await session.rollback()
    await session.close()
