from collections.abc import Sequence

import fastapi
from fastapi import Depends, Query
import pydantic
import sqlalchemy

from sample_backend import services
from sample_backend.entities import db_models
from sample_backend.interface import dependencies, schemas

router = fastapi.APIRouter()


def _get_notes_filters(category: str | None = Query(None, alias="category")) -> schemas.NotesFilters:
    try:
        return schemas.NotesFilters(category=category)
    except pydantic.ValidationError as err:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY, detail=err.errors()
        ) from err


@router.get("/", response_model=list[schemas.NoteResponsePayload])
async def get_all_notes(
    pagination: schemas.PaginationParams = Depends(dependencies.get_pagination_params),
    filters: schemas.NotesFilters = Depends(_get_notes_filters),
    notes_service: services.NotesService = Depends(dependencies.get_notes_service),
) -> Sequence[db_models.Note]:
    return await notes_service.get_all(pagination=pagination, filters=filters)


@router.post("/", response_model=schemas.NoteResponsePayload, status_code=fastapi.status.HTTP_201_CREATED)
async def new_note(
    note_payload: schemas.NoteCreationPayload,
    notes_service: services.NotesService = Depends(dependencies.get_notes_service),
) -> db_models.Note:
    return await notes_service.create(note_payload)


@router.get("/{note_id}/", response_model=schemas.NoteResponsePayload)
async def get_note_by_id(
    note_id: int, notes_service: services.NotesService = Depends(dependencies.get_notes_service)
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
    note_id: int, notes_service: services.NotesService = Depends(dependencies.get_notes_service)
) -> db_models.Note:
    try:
        return await notes_service.delete(note_id)
    except sqlalchemy.exc.NoResultFound as ex:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Note not found"
        ) from ex
