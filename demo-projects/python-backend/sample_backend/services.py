"""
Internal services of the application.

The IoC container of the application.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .db import make_db_session_creator
from .notes import NotesRepository

_db_session_creator: async_sessionmaker[AsyncSession] | None
_notes_repo: NotesRepository | None


def get_db_session_creator() -> async_sessionmaker[AsyncSession]:
    if _db_session_creator is None:
        raise LookupError("Init wasn't run!")
    return _db_session_creator


def get_notes_repo() -> NotesRepository:
    if _notes_repo is None:
        raise LookupError("Init wasn't run!")
    return _notes_repo


def init() -> None:
    global _db_session_creator  # noqa: PLW0603
    global _notes_repo  # noqa: PLW0603
    _db_session_creator = make_db_session_creator()
    _notes_repo = NotesRepository(_db_session_creator)
