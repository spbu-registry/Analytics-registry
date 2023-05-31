from sqlalchemy import delete, select

from app.core.commit.models import Commit
from app.core.commit.vault import AbstractCommitVault
from app.service.postgres.commit.entity import CommitEntity


class CommitPostgresVault(AbstractCommitVault):
    """Implementation of abstract vault."""

    def __init__(self, db_session) -> None:
        self.db_session = db_session

    async def create(self, model: Commit):
        """Implementation of abstract method."""
        entity_to_create = CommitEntity(**model.dict())
        async with self.db_session() as session:
            session.add(entity_to_create)
            await session.commit()

    async def read(self, uid: int) -> Commit:
        """Implementation of abstract method."""
        async with self.db_session() as session:
            entity = (
                await session.select(CommitEntity)
                .where(CommitEntity.uid == uid)
                .first()
            )
            return Commit(entity)

    async def read_all(self, project_uid: int) -> list[Commit]:
        """Implementation of abstract method."""
        async with self.db_session() as session:
            query = select(CommitEntity).where(CommitEntity.project_id == project_uid)
            commit_list = await session.execute(query)
            return commit_list.scalars().all()

    async def update(self, model: Commit):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            await session.update(CommitEntity).where(
                CommitEntity.uid == model.uid
            ).values(model.dict())
            await session.commit()

    async def delete(self, uid: int):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            await session.delete(CommitEntity).where(CommitEntity.uid == uid)
            await session.commit()

    async def delete_by_project(self, project_uid: int):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            query = delete(CommitEntity).where(CommitEntity.project_id == project_uid)
            await session.execute(query)
            await session.commit()
