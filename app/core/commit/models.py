from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common.models import Auditable, Entity


class CommitInfo(BaseModel):
    """All info about commit."""

    project_id: int = Field(
        default=...,
        description="Id of project to which this commit is bound",
    )
    author_login: str = Field(
        default=...,
        description="Github login of commit author",
    )
    created_at: datetime = Field(
        default=...,
        description="Datetime when this commit was created",
    )


class Commit(Entity, CommitInfo, Auditable):
    """Class that contains all fields of commit."""
