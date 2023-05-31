from datetime import datetime

from sqlalchemy import select, update

from app.core.project.models import Project
from app.core.project.vault import AbstractProjectVault
from app.service.postgres.project.entity import ProjectEntity


class ProjectPostgresVault(AbstractProjectVault):
    """Implementation of abstract vault."""

    def __init__(self, db_session) -> None:
        self.db_session = db_session

    async def create(self, model: Project):
        """Implementation of abstract method."""
        entity_to_create = ProjectEntity(**model.dict())
        async with self.db_session() as session:
            session.add(entity_to_create)
            await session.commit()

    async def read(self, uid: int) -> Project:
        """Implementation of abstract method."""
        async with self.db_session() as session:
            query = select(ProjectEntity).where(ProjectEntity.uid == uid)
            entity = await session.execute(query)
            return entity.scalar()

    async def read_all(self) -> list[Project]:
        """Implementation of abstract method."""
        async with self.db_session() as session:
            query = select(ProjectEntity)
            commit_list = await session.execute(query)
            return commit_list.scalars().all()

    async def delete(self, uid: int):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            await session.delete(ProjectEntity.uid).where(ProjectEntity.uid == uid)
            await session.commit()
