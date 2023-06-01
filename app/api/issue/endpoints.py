"""Module for storing request/response handlers.

As an agreement handler functions are called as: <method>_<route>
For example if handler has route: GET commit/{uid} function is called get_commit_uid
They can ignore docstrings, but description is required.
"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI, Path

from app.api.common.dependencies import Container
from app.api.issue.contracts import IssueResponse
from app.core.issue.services import AbstractIssueService

router = APIRouter(prefix="/issue", tags=["Issue"])


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize task router for app."""
    app.include_router(router)
    return app


@router.get(
    "/{project_id}",
    response_model=list[IssueResponse],
    description="Get issues list from project",
    response_description="Successfully fetch issues",
    status_code=200,
)
@inject
async def get_issue_project_id(  # noqa
    project_id: int = Path(  # noqa
        default=...,
        description="Project id",
    ),
    issue_service: AbstractIssueService = Depends(  # noqa
        Provide[Container.issue_service]
    ),
):
    return await issue_service.get_issues_by_project(project_id)
