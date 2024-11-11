import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

from sample_backend import connectors, services


def get_notes_repository(
    db_session: AsyncSession = fastapi.Depends(connectors.db.get_db_session),
) -> connectors.NotesRepository:
    return connectors.NotesRepository(db_session=db_session)


def get_notes_service(
    notes_repo: connectors.NotesRepository = fastapi.Depends(get_notes_repository),
) -> services.NotesService:
    return services.NotesService(repository=notes_repo)
