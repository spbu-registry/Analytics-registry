from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common.models import Auditable, Entity
from app.core.label.models import Label


class IssueInfo(BaseModel):
    """All info about issue."""

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


class Issue(Entity, IssueInfo, Auditable):
    """Class that contains all fields of issue."""
