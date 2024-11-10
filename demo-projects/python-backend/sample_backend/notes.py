"""
Implementation of the repository pattern for notes.

With an app this simple we might not need a repository and just use the ORM directly,
but using the pattern will help illustrate when to use tests at different levels (unit/integrated/functional).

Also, it'll set the stage for using a test double of the NotesRepository in unit tests.
"""

from collections.abc import Sequence

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from sample_backend.interface import schemas

from .db import Note


# TODO have a function that returns a DB session. Multiple objects should reuse the same session.
# It should be put in a contextvar.
class NotesRepository:
    """Stores and returns notes."""

    def __init__(self, db_session_creator: async_sessionmaker[AsyncSession]) -> None:
        self._db_session_creator = db_session_creator

    async def create(self, note_payload: schemas.NoteCreationPayload) -> int:
        """
        Create a new note.

        Returns:
            The ID under which the note is stored.
        """
        async with self._db_session_creator() as session:
            query = insert(Note).values(contents=note_payload.contents).returning(Note.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def delete(self) -> None:
        """Delete a note."""
        raise NotImplementedError("Delete not implemented.")

    async def get(self, note_id: int) -> Note:
        """Get a single note."""
        # TODO handle the case where the ID is not found
        async with self._db_session_creator() as session:
            query = select(Note).where(Note.id == note_id)
            result = await session.execute(query)
            return result.scalar_one()

    async def get_all(self) -> Sequence[Note]:
        """Get all notes."""
        async with self._db_session_creator() as session:
            query = select(Note)
            result = await session.execute(query)
            return result.scalars().all()
