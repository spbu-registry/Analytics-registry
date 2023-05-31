from datetime import datetime

from pydantic import BaseModel, Field


class CommitResponse(BaseModel):
    """Contract for response commit."""

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

    class Config:  # noqa
        orm_mode = True
