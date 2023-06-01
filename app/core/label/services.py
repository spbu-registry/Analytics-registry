from typing import Protocol

from app.core.label.models import Label


class AbstractLabelService(Protocol):
    """Abstract service."""

    async def get_labels_by_project(self, project_uid: int) -> list[Label]:
        """Abstract method in service."""
        raise NotImplementedError

    async def create_label(self, label: Label):
        """Abstract method in service."""
        raise NotImplementedError

    async def update_label(self, label: Label):
        """Abstract method in service."""
        raise NotImplementedError

    async def fetch_data_from_github(self, links: list[str]):
        """Abstract method in service."""
        raise NotImplementedError

    async def delete_by_project(self, project_uid: int):
        """Abstract method in service."""
        raise NotImplementedError


class DataBaseLabelService(AbstractLabelService):
    """implementation of AbstractLabelService."""

    ...
