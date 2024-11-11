"""
Some would say that ORM models shouldn't be treated as entities, because they're not "pure".

But pragmatically, they function as entities very well. Especially with FastAPI.
"""

import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import expression


class Base(DeclarativeBase):
    """Base class for SQL Alchemy tables."""


class Note(Base):
    """Notes table."""

    __tablename__ = "notes"

    # TODO make this a GUID
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO should be timezone-aware
    creation_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    contents: Mapped[str]
    is_deleted: Mapped[bool] = mapped_column(server_default=expression.false())
