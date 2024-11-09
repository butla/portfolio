import datetime

import pydantic


class NoteCreationPayload(pydantic.BaseModel):
    contents: str


class NoteResponsePayload(pydantic.BaseModel):
    # With this, FastApi will handle returning ORM Note objects from endpoint functions.
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    creation_date: datetime.datetime
    contents: str
