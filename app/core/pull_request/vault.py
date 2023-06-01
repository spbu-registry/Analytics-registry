from typing import Protocol

from app.core.pull_request.models import PullRequest


class AbstractPullRequestVault(Protocol):
    """Abstract class for pull request vault."""

    async def create(self, model: PullRequest):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read(self, uid: int) -> PullRequest:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read_all(self) -> list[PullRequest]:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def update(self, model: PullRequest):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete(self, uid: int):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete_by_project(self, project_uid: int):
        """Abstract method in generic repository."""
        raise NotImplementedError
