from collections.abc import AsyncIterator, Sequence
import contextlib
import logging

import fastapi

from sample_backend import services
from sample_backend.core.config import SETTINGS
from sample_backend.db import Note

from . import schemas

logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def app_lifespan(app: fastapi.FastAPI) -> AsyncIterator[None]:
    del app  # not used
    logging.basicConfig(level=logging.INFO)
    logger.info("App starting...")
    services.init()

    yield
    logger.info("App shutting down...")
    # TODO close all services


app = fastapi.FastAPI(
    title=SETTINGS.app_name,
    lifespan=app_lifespan,
)


@app.get("/")
async def hello() -> dict[str, str]:
    return {"hello": "world"}


@app.get("/notes/", response_model=list[schemas.NoteResponsePayload])
async def get_all_notes() -> Sequence[Note]:
    return await services.get_notes_repo().get_all()


@app.get("/notes/{note_id}/", response_model=schemas.NoteResponsePayload)
async def get_note_by_id(note_id: int) -> Note:
    return await services.get_notes_repo().get(note_id)


@app.post("/notes/", response_model=schemas.NoteResponsePayload, status_code=201)
async def new_note(note_payload: schemas.NoteCreationPayload) -> Note:
    notes_repo = services.get_notes_repo()
    note_id = await notes_repo.create(note_payload)
    return await notes_repo.get(note_id)


# TODO add the delete endpoint
