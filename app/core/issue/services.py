from datetime import datetime, timedelta
from typing import Protocol

from aiohttp import ClientSession
from fastapi import HTTPException

from app.common.errors import ExternalAPI
from app.core.issue.models import Issue
from app.core.project.models import Project
from app.core.project.services import AbstractProjectService
from app.service.postgres.common.settings import PostgresSettings

from .vault import AbstractIssueVault

config = PostgresSettings()


class AbstractIssueService(Protocol):
    """Abstract service."""

    async def get_issues_by_project(self, project_uid: int) -> list[Issue]:
        """Abstract method in service."""
        raise NotImplementedError

    async def create_issue(self, issue: Issue):
        """Abstract method in service."""
        raise NotImplementedError

    async def update_issue(self, issue: Issue):
        """Abstract method in service."""
        raise NotImplementedError

    async def fetch_data_from_github(self, links: list[str]):
        """Abstract method in service."""
        raise NotImplementedError

    async def delete_by_project(self, project_uid: int):
        """Abstract method in service."""
        raise NotImplementedError


class DatabaseIssueService(AbstractIssueService):
    """Implementation of AbstractIssueService."""

    def __init__(
        self,
        vault: AbstractIssueVault,
        project_service: AbstractProjectService,
    ) -> None:
        self.vault = vault
        self.project_service = project_service

    async def get_issues_by_project(self, project_uid: int) -> list[Issue]:
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

        issue_from_project = await self.vault.read_all(project_uid=project_uid)

        if not issue_from_project:
            await self.fetch_data_from_github(project.links, project_uid=project_uid)
            return await self.vault.read_all(project_uid=project_uid)
        if datetime.now() - issue_from_project[0].updated_at > timedelta(minutes=5):
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
                        url=link + f"/issues?per_page=100&page={page}&state=all",
                        headers={
                            "Authorization": f"Bearer {config.TOKEN}",
                        },
                    ) as response:
                        if response.status != 200:
                            return ExternalAPI(
                                message="Error in external API, likely with Github"
                            )
                        issues = await response.json()
                        for issue in issues:
                            issue = Issue(
                                project_id=project_uid,
                                author_login=issue["user"]["login"],
                                created_at=issue["created_at"],
                                closed_at=issue["closed_at"],
                            )
                            await self.vault.create(model=issue)

    async def delete_by_project(self, project_uid: int):
        """Implementaion of abstract method."""
        await self.vault.delete_by_project(project_uid=project_uid)
