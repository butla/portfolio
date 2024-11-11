from collections.abc import AsyncIterator

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

SessionMaker: async_sessionmaker | None = None
engine: AsyncEngine | None = None


def init_db_session_creator(database_url: sqlalchemy.URL) -> None:
    """Initialize the DB session creator when the program is starting."""
    global SessionMaker  # noqa: PLW0603
    if SessionMaker:
        return

    global engine  # noqa: PLW0603

    engine = create_async_engine(database_url, pool_pre_ping=True)
    # Don't expire objects when a commit is made.
    # Expired objects need to be refreshed from the DB.
    # With this we can get the IDs of freshly inserted objects without additional DB interactions,
    # because SQLAlchemy does inserts with "INSERT...RETURNING" query.
    SessionMaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Gets a DB session based on a connection from the pool. It's meant to be used with fastapi.Depends."""
    if not SessionMaker:
        raise RuntimeError("Attempting to get a DB session before initializing the session creator.")
    async with SessionMaker() as session:
        yield session
        await session.commit()


async def close_db_engine() -> None:
    """Call this when the program is shutting down."""
    if not engine:
        raise RuntimeError("Attempting to close the DB engine before it was initialized.")
    await engine.dispose()
