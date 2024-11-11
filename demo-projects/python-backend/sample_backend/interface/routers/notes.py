from collections.abc import Sequence

import fastapi
import sqlalchemy

from sample_backend import services
from sample_backend.entities import db_models
from sample_backend.interface import dependencies, schemas

router = fastapi.APIRouter()


@router.get("/", response_model=list[schemas.NoteResponsePayload])
async def get_all_notes(
    notes_service: services.NotesService = fastapi.Depends(dependencies.get_notes_service),
) -> Sequence[db_models.Note]:
    return await notes_service.get_all()


@router.post("/", response_model=schemas.NoteResponsePayload, status_code=fastapi.status.HTTP_201_CREATED)
async def new_note(
    note_payload: schemas.NoteCreationPayload,
    notes_service: services.NotesService = fastapi.Depends(dependencies.get_notes_service),
) -> db_models.Note:
    return await notes_service.create(note_payload)


@router.get("/{note_id}/", response_model=schemas.NoteResponsePayload)
async def get_note_by_id(
    note_id: int, notes_service: services.NotesService = fastapi.Depends(dependencies.get_notes_service)
) -> db_models.Note:
    try:
        return await notes_service.get(note_id)
    # We should catch this exception earlier and wrap it in a service-specific exception.
    except sqlalchemy.exc.NoResultFound as ex:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Note not found"
        ) from ex


@router.delete("/{note_id}/", response_model=schemas.NoteResponsePayload)
async def delete_note_by_id(
    note_id: int, notes_service: services.NotesService = fastapi.Depends(dependencies.get_notes_service)
) -> db_models.Note:
    try:
        return await notes_service.delete(note_id)
    except sqlalchemy.exc.NoResultFound as ex:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Note not found"
        ) from ex
