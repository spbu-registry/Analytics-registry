from datetime import datetime

from pydantic import BaseModel, Field

from app.core.common.models import Entity


class LabelInfo(BaseModel):
    """All info about label."""

    name: str = Field(
        default=...,
        description="Name of label",
    )
    description: str | None = Field(
        default=None,
        description="Custom description of label",
    )


class Label(Entity, LabelInfo):
    """Class that contains all fields of label."""
