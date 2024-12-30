from collections.abc import Sequence
from dataclasses import dataclass

from sample_backend import connectors
from sample_backend.entities import db_models
from sample_backend.interface import schemas


# TODO currently this service just delegates to the repository. Make this more interesting.
@dataclass
class NotesService:
    """Manages notes."""

    repository: connectors.NotesRepository

    async def create(self, note_payload: schemas.NoteCreationPayload) -> db_models.Note:
        """Create a new note."""
        return await self.repository.create(note_payload)

    async def delete(self, note_id: int) -> db_models.Note:
        """Delete a note."""
        return await self.repository.delete(note_id)

    async def get(self, note_id: int) -> db_models.Note:
        """Get a single note."""
        return await self.repository.get(note_id)

    async def get_all(
        self, pagination: schemas.PaginationParams, filters: schemas.NotesFilters
    ) -> Sequence[db_models.Note]:
        """Get all notes."""
        return await self.repository.get_all(pagination=pagination, filters=filters)
