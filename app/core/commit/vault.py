from typing import Protocol

from app.core.commit.models import Commit


class AbstractCommitVault(Protocol):
    """Abstract class for commit vault."""

    async def create(self, model: Commit):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read(self, uid: int) -> Commit:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read_all(self, project_uid: int) -> list[Commit]:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def update(self, model: Commit):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete(self, uid: int):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete_by_project(self, project_uid: int):
        """Abstract method in generic repository."""
        raise NotImplementedError
