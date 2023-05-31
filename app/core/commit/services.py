from datetime import datetime, timedelta
from typing import Protocol

from aiohttp import ClientSession
from fastapi import HTTPException

from app.common.errors import ExternalAPI
from app.core.commit.models import Commit
from app.core.project.models import Project
from app.core.project.services import AbstractProjectService
from app.service.postgres.common.settings import PostgresSettings

from .vault import AbstractCommitVault

config = PostgresSettings()


class AbstractCommitService(Protocol):
    """Abstract service."""

    async def get_commits_by_project(self, project_uid: int) -> list[Commit]:
        """Abstract method in service."""
        raise NotImplementedError

    async def create_commit(self, commit: Commit):
        """Abstract method in service."""
        raise NotImplementedError

    async def update_commit(self, commit: Commit):
        """Abstract method in service."""
        raise NotImplementedError

    async def fetch_data_from_github(self, links: list[str]):
        """Abstract method in service."""
        raise NotImplementedError

    async def delete_by_project(self, project_uid: int):
        """Abstract method in service."""
        raise NotImplementedError


class DatabaseCommitService(AbstractCommitService):
    """Implementation of AbstractCommitService."""

    def __init__(
        self,
        vault: AbstractCommitVault,
        project_service: AbstractProjectService,
    ) -> None:
        self.vault = vault
        self.project_service = project_service

    async def get_commits_by_project(self, project_uid: int) -> list[Commit]:
        """Implementation of abstract method."""
        project = await self.project_service.get_project(uid=project_uid)
        if not project:
            async with ClientSession() as session:
                async with session.get(
                    url=f"http://217.197.0.155/data/projects/project?id={project_uid}",
                ) as response:
                    if response.status == 404:
                        raise HTTPException(
                            status_code=404,
                            detail="Entity project not found",
                        )
                    response_project = await response.json()
                    project = Project(
                        uid=project_uid,
                        links=[
                            response_project["links"][i]["link"]
                            for i in range(len(response_project["links"]))
                        ],
                    )
                    await self.project_service.create_project(project)
                    await self.fetch_data_from_github(
                        project.links, project_uid=project_uid
                    )
                    return await self.vault.read_all(project_uid=project_uid)

        commit_from_project = await self.vault.read_all(project_uid=project_uid)

        if not commit_from_project:
            await self.fetch_data_from_github(project.links, project_uid=project_uid)
            return await self.vault.read_all(project_uid=project_uid)
        if datetime.utcnow() - commit_from_project[0].updated_at > timedelta(minutes=5):
            await self.fetch_data_from_github(project.links, project_uid=project_uid)
        return await self.vault.read_all(project_uid=project_uid)

    async def fetch_data_from_github(self, links: list[str], project_uid: int):
        """A po pope?."""
        await self.delete_by_project(project_uid=project_uid)
        for link in links:
            if link[0] == "+":
                link = link[1:]
            link = link.replace("https://github.com", "https://api.github.com/repos")
            for page in range(1, 11):
                async with ClientSession() as session:
                    async with session.get(
                        url=link + f"/commits?per_page=100&page={page}",
                        headers={
                            "Authorization": f"Bearer {config.TOKEN}",
                        },
                    ) as response:
                        if response.status != 200:
                            return ExternalAPI(
                                message="Error in external API, likely with Github"
                            )
                        commits = await response.json()
                        for commit in commits:
                            commit = Commit(
                                project_id=project_uid,
                                author_login=commit["author"]["login"],
                                created_at=commit["commit"]["author"]["date"],
                            )
                            await self.vault.create(model=commit)

    async def delete_by_project(self, project_uid: int):
        """Implementaion of abstract method."""
        await self.vault.delete_by_project(project_uid=project_uid)
