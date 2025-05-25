from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.database import Base

Table = TypeVar("Table", bound=Base)


class BaseRepository:
    def __init__(self
                 , db: Session):
        self.db = db


class UniqueFieldError(Exception):
    """Describes an error that is raised when unique validation is failed."""

    def __init__(self, detail: str):
        self.detail = detail


class Repository(Generic[Table]):
    """Describes basic methods for working with tables."""

    table: type[Table]

    def __init__(self, session: Session):
        self.session = session
