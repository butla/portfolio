from collections.abc import AsyncIterator, Sequence
import contextlib

import fastapi

from . import api_schemas, services
from .db import Note


@contextlib.asynccontextmanager
async def app_lifespan(app: fastapi.FastAPI) -> AsyncIterator[None]:
    del app  # not used
    services.init()
    yield


app = fastapi.FastAPI(lifespan=app_lifespan)


@app.get("/")
async def hello() -> dict[str, str]:
    return {"hello": "world"}


@app.get("/notes/", response_model=list[api_schemas.NoteResponsePayload])
async def get_all_notes() -> Sequence[Note]:
    return await services.get_notes_repo().get_all()


@app.get("/notes/{note_id}/", response_model=api_schemas.NoteResponsePayload)
async def get_note_by_id(note_id: int) -> Note:
    return await services.get_notes_repo().get(note_id)


@app.post("/notes/", response_model=api_schemas.NoteResponsePayload, status_code=201)
async def new_note(note_payload: api_schemas.NoteCreationPayload) -> Note:
    notes_repo = services.get_notes_repo()
    note_id = await notes_repo.create(note_payload)
    return await notes_repo.get(note_id)


# TODO add the delete endpoint
