from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel, Field

uid = int


class Auditable(BaseModel):
    """Base class for auditable entities."""

    updated_at: datetime = Field(default=datetime.now())


class Entity(BaseModel):
    """Base class for all entities that have uid(id)."""

    uid: int | None
