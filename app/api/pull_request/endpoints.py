"""Module for storing request/response handlers.

As an agreement handler functions are called as: <method>_<route>
For example if handler has route: GET commit/{uid} function is called get_commit_uid
They can ignore docstrings, but description is required.
"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI, Path

from app.api.common.dependencies import Container
from app.api.pull_request.contracts import PullRequestResponse
from app.core.pull_request.services import AbstractPullRequestService

router = APIRouter(prefix="/pull_request", tags=["Pull_request"])


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize task router for app."""
    app.include_router(router)
    return app


@router.get(
    "/{project_id}",
    response_model=list[PullRequestResponse],
    description="Get pulls list from project",
    response_description="Successfully fetch pulls",
    status_code=200,
)
@inject
async def get_pull_request_project_id(  # noqa
    project_id: int = Path(  # noqa
        default=...,
        description="Project id",
    ),
    pull_request_service: AbstractPullRequestService = Depends(  # noqa
        Provide[Container.pull_request_service]
    ),
):
    return await pull_request_service.get_pull_requests_by_project(project_id)
