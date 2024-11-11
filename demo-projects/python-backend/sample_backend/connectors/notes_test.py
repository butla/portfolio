import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from sample_backend.connectors import NotesRepository
from sample_backend.interface import schemas


@pytest.fixture
def notes_repo(db_session: AsyncSession) -> NotesRepository:
    return NotesRepository(db_session)


@pytest.mark.integrated
async def test_create_a_note(notes_repo: NotesRepository) -> None:
    note_payload = schemas.NoteCreationPayload(contents="I'm a note, wee!")

    stored_note = await notes_repo.create(note_payload)

    assert stored_note.contents == note_payload.contents


# TODO cover the rest of NotesRepository methods. Introduce FactoryBoy fakers.
