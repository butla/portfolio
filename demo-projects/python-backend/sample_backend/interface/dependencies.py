from fastapi import Depends, HTTPException, Query, status
import pydantic
from sqlalchemy.ext.asyncio import AsyncSession

from sample_backend import connectors, services
from sample_backend.interface import schemas


def get_pagination_params(
    offset: int = Query(0, alias="offset"), limit: int = Query(10, alias="limit")
) -> schemas.PaginationParams:
    try:
        return schemas.PaginationParams(offset=offset, limit=limit)
    except pydantic.ValidationError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=err.errors()) from err


def get_notes_repository(
    db_session: AsyncSession = Depends(connectors.db.get_db_session),
) -> connectors.NotesRepository:
    return connectors.NotesRepository(db_session=db_session)


def get_notes_service(
    notes_repo: connectors.NotesRepository = Depends(get_notes_repository),
) -> services.NotesService:
    return services.NotesService(repository=notes_repo)
