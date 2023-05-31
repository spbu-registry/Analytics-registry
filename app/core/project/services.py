from datetime import datetime
from typing import Protocol

from app.core.project.models import Project

from .vault import AbstractProjectVault


class AbstractProjectService(Protocol):
    """Abstract service."""

    async def get_project(self, uid: int) -> Project:
        """Abstract method in service."""
        raise NotImplementedError

    async def create_project(self, project: Project):
        """Abstract method in service."""
        raise NotImplementedError


class DatabaseProjectService(AbstractProjectService):
    """Implementation of AbstractProjectService."""

    def __init__(self, vault: AbstractProjectVault) -> None:
        self.vault = vault

    async def get_project(self, uid: int) -> Project:
        """Implementation of abstract method."""
        return await self.vault.read(uid=uid)

    async def create_project(self, project: Project):
        """Implementation of abstract method."""
        return await self.vault.create(model=project)
