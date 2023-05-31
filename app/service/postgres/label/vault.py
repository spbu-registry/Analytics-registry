from sqlalchemy import delete, select

from app.core.label.models import Label
from app.core.label.vault import AbstractLabelVault
from app.service.postgres.label.entity import LabelEntity


class LabelPostgresVault(AbstractLabelVault):
    """Implementation of abstract vault."""

    def __init__(self, db_session) -> None:
        self.db_session = db_session

    async def create(self, model: Label):
        """Implementation of abstract method."""
        entity_to_create = LabelEntity(**model.dict())
        async with self.db_session() as session:
            session.add(entity_to_create)
            await session.commit()

    async def read(self, uid: int) -> Label:
        """Implementation of abstract method."""
        async with self.db_session() as session:
            entity = (
                await session.select(LabelEntity).where(LabelEntity.uid == uid).first()
            )
            return Label(entity)

    async def read_all(self, project_uid: int) -> list[Label]:
        """Implementation of abstract method."""
        async with self.db_session() as session:
            query = select(LabelEntity).where(LabelEntity.project_id == project_uid)
            commit_list = await session.execute(query)
            return commit_list.scalars().all()

    async def update(self, model: Label):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            await session.update(LabelEntity).where(
                LabelEntity.uid == model.uid
            ).values(model.dict())
            await session.commit()

    async def delete(self, uid: int):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            await session.delete(LabelEntity).where(LabelEntity.uid == uid)
            await session.commit()

    async def delete_by_project(self, project_uid: int):
        """Implementation of abstract method."""
        async with self.db_session() as session:
            query = delete(LabelEntity).where(LabelEntity.project_id == project_uid)
            await session.execute(query)
            await session.commit()
