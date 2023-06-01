from pydantic import BaseModel, Field

from app.core.common.models import Auditable, Entity


class ProjectInfo(BaseModel):
    """All info about project."""

    links: list[str] = Field(
        default=...,
        description="Links to project",
    )


class Project(Entity, ProjectInfo, Auditable):
    """Class that contains all fields of project."""
