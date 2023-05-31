from typing import Protocol

from app.core.label.models import Label


class AbstractLabelVault(Protocol):
    """Abstract class for label vault."""

    async def create(self, model: Label):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read(self, uid: int) -> Label:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def read_all(self) -> list[Label]:
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def update(self, model: Label):
        """Abstract method in generic repository."""
        raise NotImplementedError

    async def delete(self, uid: int):
        """Abstract method in generic repository."""
        raise NotImplementedError
