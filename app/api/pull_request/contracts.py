from datetime import datetime

from pydantic import BaseModel, Field


class PullRequestResponse(BaseModel):
    """Contract for response pull."""

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

    class Config:  # noqa
        orm_mode = True
