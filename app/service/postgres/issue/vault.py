from sqlalchemy import delete, select

from app.core.issue.models import Issue
from app.core.issue.vault import AbstractIssueVault
from app.service.postgres.issue.entity import IssueEntity


class IssuePostgresVault(AbstractIssueVault):
    """Implementation of abstract vault."""

    def __init__(self, db_session) -> None:
        self.db_session = db_session

    async def create(self, model: Issue):
        """Implementation of abstract method."""
        entity_to_create = IssueEntity(**model.dict())
        async with self.db_session() as session:
            session.add(entity_to_create)
            await session.commit()

    async def read(self, uid: int) -> Issue:
        """Implementation of abstract method."""
        async with self.db_session() as session:
            entity = (
                await session.select(IssueEntity).where(IssueEntity.uid == uid).first()
            )
            return Issue(entity)

    async def read_all(self, project_uid: int) -> list[Issue]:
        """Implementation of abstract method."""
        async with self.db_session() as session:
            query = select(IssueEntity).where(IssueEntity.project_id == project_uid)
            commit_list = await session.execute(query)
            return commit_list.scalars().unique().all()

    async def update(self, model: Issue):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            await session.update(IssueEntity).where(
                IssueEntity.uid == model.uid
            ).values(model.dict())
            await session.commit()

    async def delete(self, uid: int):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            await session.delete(IssueEntity).where(IssueEntity.uid == uid)
            await session.commit()

    async def delete_by_project(self, project_uid: int):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            query = delete(IssueEntity).where(IssueEntity.project_id == project_uid)
            await session.execute(query)
            await session.commit()
