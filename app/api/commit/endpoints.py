"""Module for storing request/response handlers.

As an agreement handler functions are called as: <method>_<route>
For example if handler has route: GET commit/{uid} function is called get_commit_uid
They can ignore docstrings, but description is required.
"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI, Path

from app.api.commit.contracts import CommitResponse
from app.api.common.dependencies import Container
from app.core.commit.services import AbstractCommitService

router = APIRouter(prefix="/commit", tags=["Commit"])


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize task router for app."""
    app.include_router(router)
    return app


@router.get(
    "/{project_id}",
    response_model=list[CommitResponse],
    description="Get commits list from project",
    response_description="Successfully fetch commits",
    status_code=200,
)
@inject
async def get_commit_project_id(  # noqa
    project_id: int = Path(  # noqa
        default=...,
        description="Project id",
    ),
    commit_service: AbstractCommitService = Depends(  # noqa
        Provide[Container.commit_service]
    ),
):
    return await commit_service.get_commits_by_project(project_id)
