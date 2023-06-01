from typing import Protocol

from app.core.project.models import Project


class AbstractProjectVault(Protocol):
    """Abstract class for Project vault."""

    async def create(self, model: Project):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read(self, uid: int) -> Project:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read_all(self) -> list[Project]:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def update(self, model: Project):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete(self, uid: int):
        """Abstract method in generic repository."""
        raise NotImplementedError
