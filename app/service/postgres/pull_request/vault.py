from sqlalchemy import delete, select

from app.core.pull_request.models import PullRequest
from app.core.pull_request.vault import AbstractPullRequestVault
from app.service.postgres.pull_request.entity import PullRequestEntity


class PullRequestPostgresVault(AbstractPullRequestVault):
    """Implementation of abstract vault."""

    def __init__(self, db_session) -> None:
        self.db_session = db_session

    async def create(self, model: PullRequest):
        """Implementation of abstract method."""
        entity_to_create = PullRequestEntity(**model.dict())
        async with self.db_session() as session:
            session.add(entity_to_create)
            await session.commit()

    async def read(self, uid: int) -> PullRequest:
        """Implementation of abstract method."""
        async with self.db_session() as session:
            entity = (
                await session.select(PullRequestEntity)
                .where(PullRequestEntity.uid == uid)
                .first()
            )
            return PullRequest(entity)

    async def read_all(self, project_uid: int) -> list[PullRequest]:
        """Implementation of abstract method."""
        async with self.db_session() as session:
            query = select(PullRequestEntity).where(
                PullRequestEntity.project_id == project_uid
            )
            commit_list = await session.execute(query)
            return commit_list.scalars().all()

    async def update(self, model: PullRequest):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            await session.update(PullRequestEntity).where(
                PullRequestEntity.uid == model.uid
            ).values(model.dict())
            await session.commit()

    async def delete(self, uid: int):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            await session.delete(PullRequestEntity).where(PullRequestEntity.uid == uid)
            await session.commit()

    async def delete_by_project(self, project_uid: int):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            query = delete(PullRequestEntity).where(
                PullRequestEntity.project_id == project_uid
            )
            await session.execute(query)
            await session.commit()
