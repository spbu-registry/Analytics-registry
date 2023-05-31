from datetime import datetime

from pydantic import BaseModel, Field

from app.core.label.models import Label


class IssueResponse(BaseModel):
    """Contract for response issue."""

    project_id: int = Field(
        default=...,
        description="Id of project to which this issue is bound",
    )
    author_login: str = Field(
        default=...,
        description="Github login of issue author",
    )
    created_at: datetime = Field(
        default=...,
        description="Datetime when this issue was created",
    )
    closed_at: datetime | None = Field(
        default=None,
        description="Datetime when this issue was closed/done",
    )
    labels: list[Label] = Field(
        default=[],
        description="List of label that bound to this issue",
    )

    class Config:  # noqa
        orm_mode = True
