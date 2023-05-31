from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common.models import Auditable, Entity


class PullRequestInfo(BaseModel):
    """All info about pull request."""

    project_id: int = Field(
        default=...,
        description="Id of project to which this pull request is bound",
    )
    author_login: str = Field(
        default=...,
        description="Github login of pull request author",
    )
    created_at: datetime = Field(
        default=...,
        description="Datetime when this pull request was created",
    )
    closed_at: datetime | None = Field(
        default=None,
        description="Datetime when this pull request was closed/done",
    )


class PullRequest(Entity, PullRequestInfo, Auditable):
    """Class that contains all fields of pull request."""
