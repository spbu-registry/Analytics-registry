from datetime import datetime, timedelta
from typing import Protocol

from aiohttp import ClientSession
from fastapi import HTTPException

from app.common.errors import ExternalAPI
from app.core.project.models import Project
from app.core.project.services import AbstractProjectService
from app.core.pull_request.models import PullRequest
from app.service.postgres.common.settings import PostgresSettings

from .vault import AbstractPullRequestVault

config = PostgresSettings()


class AbstractPullRequestService(Protocol):
    """Abstract service."""

    async def get_pull_requests_by_project(self, project_uid: int) -> list[PullRequest]:
        """Abstract method in service."""
        raise NotImplementedError

    async def create_pull_request(self, pull_request: PullRequest):
        """Abstract method in service."""
        raise NotImplementedError

    async def update_pull_request(self, pull_request: PullRequest):
        """Abstract method in service."""
        raise NotImplementedError

    async def fetch_data_from_github(self, links: list[str]):
        """Abstract method in service."""
        raise NotImplementedError

    async def delete_by_project(self, project_uid: int):
        """Abstract method in service."""
        raise NotImplementedError


class DatabasePullRequestService(AbstractPullRequestService):
    """Implementation of AbstractPullRequestService."""

    def __init__(
        self,
        vault: AbstractPullRequestVault,
        project_service: AbstractProjectService,
    ) -> None:
        self.vault = vault
        self.project_service = project_service

    async def get_pull_requests_by_project(self, project_uid: int) -> list[PullRequest]:
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

        pulls_from_project = await self.vault.read_all(project_uid=project_uid)

        if not pulls_from_project:
            await self.fetch_data_from_github(project.links, project_uid=project_uid)
            return await self.vault.read_all(project_uid=project_uid)
        if datetime.utcnow() - pulls_from_project[0].updated_at > timedelta(minutes=5):
            await self.fetch_data_from_github(project.links, project_uid=project_uid)
        return await self.vault.read_all(project_uid=project_uid)

    async def fetch_data_from_github(self, links: list[str], project_uid: int):
        """A po pope?."""
        await self.delete_by_project(project_uid=project_uid)
        for link in links:
            if link[0] == "+":
                link = link[1:]
            link = link.replace("https://github.com", "https://api.github.com/repos")
            async with ClientSession() as session:
                async with session.get(
                    url=link + "/pulls?per_page=100&page=1&state=all",
                    headers={
                        "Authorization": f"Bearer {config.TOKEN}",
                    },
                ) as response:
                    if response.status != 200:
                        return ExternalAPI(
                            message="Error in external API, likely with Github"
                        )
                    pull_requests = await response.json()
                    for pull_request in pull_requests:
                        pull_request = PullRequest(
                            project_id=project_uid,
                            author_login=pull_request["user"]["login"],
                            created_at=pull_request["created_at"],
                            closed_at=pull_request["closed_at"],
                        )
                        await self.vault.create(model=pull_request)

    async def delete_by_project(self, project_uid: int):
        """Implementaion of abstract method."""
        await self.vault.delete_by_project(project_uid=project_uid)
