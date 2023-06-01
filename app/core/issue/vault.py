from typing import Protocol

from app.core.issue.models import Issue


class AbstractIssueVault(Protocol):
    """Abstract class for issue vault."""

    async def create(self, model: Issue):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read(self, uid: int) -> Issue:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read_all(self) -> list[Issue]:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def update(self, model: Issue):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete(self, uid: int):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete_by_project(self, project_uid: int):
        """Abstract method in generic repository."""
        raise NotImplementedError
