import datetime
from typing import Type, TypeVar

import pydantic

from sample_backend.entities.db_models import Note
from sample_backend.interface.schemas.common import PaginationParams


class NoteCreationPayload(pydantic.BaseModel):
    contents: str


class NoteResponsePayload(pydantic.BaseModel):
    # With this, FastApi will handle returning ORM Note objects from endpoint functions.
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    creation_date: pydantic.AwareDatetime
    contents: str


# TODO finish this up thework out the details and fini
T = TypeVar("T", bound="NotesPage")


class NotesPage(PaginationParams):
    notes: list[NoteResponsePayload]

    @classmethod
    # TODO needs pagination params as input
    def from_notes(cls: type[T], notes: list[Note]) -> T:  # type: ignore[empty-body]
        # return cls(notes=notes, ) for note]
        pass
