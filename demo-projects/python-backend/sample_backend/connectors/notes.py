"""
Implementation of the repository pattern for notes.

With an app this simple we might not need a repository and just use the ORM directly,
but using the pattern will help illustrate when to use tests at different levels (unit/integrated/functional).

Also, it'll set the stage for using a test double of the NotesRepository in unit tests.
"""

from collections.abc import Sequence
import dataclasses

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from sample_backend.entities.db_models import Note
from sample_backend.interface import schemas


@dataclasses.dataclass
class NotesRepository:
    """Stores and returns notes."""

    BASE_QUERY = select(Note).where(Note.is_deleted == False)  # noqa: E712

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def create(self, note_payload: schemas.NoteCreationPayload) -> Note:
        """Create a new note."""
        note = Note(contents=note_payload.contents)
        self._db_session.add(note)
        await self._db_session.flush()
        return note

    async def delete(self, note_id: int) -> Note:
        """Delete a note."""
        # Update returning the entire updated row.
        query = update(Note).where(Note.id == note_id).values(is_deleted=True).returning(Note)
        result = await self._db_session.execute(query)
        return result.scalar_one()

    async def get(self, note_id: int) -> Note:
        """Get a single note."""
        # TODO handle the case where the ID is not found
        query = self.BASE_QUERY.where(Note.id == note_id)
        result = await self._db_session.execute(query)
        return result.scalar_one()

    async def get_all(self) -> Sequence[Note]:
        """Get all notes."""
        query = self.BASE_QUERY
        result = await self._db_session.execute(query)
        return result.scalars().all()
