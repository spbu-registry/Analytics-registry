from dependency_injector import providers
from fastapi import FastAPI
from toolz import pipe

from app.core.commit.services import DatabaseCommitService
from app.core.issue.services import DatabaseIssueService
from app.core.project.services import DatabaseProjectService
from app.core.pull_request.services import DatabasePullRequestService
from app.service.postgres.commit.vault import CommitPostgresVault
from app.service.postgres.common.database import AsyncDb
from app.service.postgres.issue.vault import IssuePostgresVault
from app.service.postgres.project.vault import ProjectPostgresVault
from app.service.postgres.pull_request.vault import PullRequestPostgresVault

from .commit import endpoints as commit_endpoints
from .common import dependencies, endpoints, error_handlers, event_handlers, middleware
from .issue import endpoints as issue_endpoints
from .pull_request import endpoints as pull_request_endpoints


def bootstrap() -> FastAPI:
    """Factory function for FastAPI."""
    # Initialize dependency container
    container = dependencies.Container(
        # Abstract dependencies are configured via override or arguments for Container
        # constructor
    )
    container.postgres_db.override(
        providers.Singleton(
            AsyncDb,
            db_url=container.postgres_settings.provides.get_database_url(),
            debug=container.fastapi_settings.provided.DEBUG,
        )
    )
    container.commit_repository.override(
        providers.Factory(
            CommitPostgresVault,
            db_session=container.postgres_db.provided.session,
        )
    )
    container.project_repository.override(
        providers.Factory(
            ProjectPostgresVault,
            db_session=container.postgres_db.provided.session,
        )
    )
    container.issue_repository.override(
        providers.Factory(
            IssuePostgresVault,
            db_session=container.postgres_db.provided.session,
        )
    )
    container.pull_request_repository.override(
        providers.Factory(
            PullRequestPostgresVault,
            db_session=container.postgres_db.provided.session,
        )
    )
    container.project_service.override(
        providers.Singleton(
            DatabaseProjectService,
            vault=container.project_repository,
        )
    )
    container.commit_service.override(
        providers.Singleton(
            DatabaseCommitService,
            vault=container.commit_repository,
            project_service=container.project_service,
        )
    )
    container.pull_request_service.override(
        providers.Singleton(
            DatabasePullRequestService,
            vault=container.pull_request_repository,
            project_service=container.project_service,
        )
    )
    container.issue_service.override(
        providers.Singleton(
            DatabaseIssueService,
            vault=container.issue_repository,
            project_service=container.project_service,
        )
    )
    # Wire package and modules - API only as this is the only place where dependencies
    # are injected
    container.wire(
        modules=[
            dependencies,
            endpoints,
            error_handlers,
            event_handlers,
            middleware,
            commit_endpoints,
            pull_request_endpoints,
            issue_endpoints,
        ],
        packages=[],
    )
    fastapi_settings = container.fastapi_settings()

    return pipe(
        fastapi_settings.create_fastapi(),
        # bootstrap commons
        dependencies.bootstrap,
        middleware.bootstrap,
        error_handlers.bootstrap,
        event_handlers.bootstrap,
        # bootstrap endpoints and sub routes
        endpoints.bootstrap,
        commit_endpoints.bootstrap,
        pull_request_endpoints.bootstrap,
        issue_endpoints.bootstrap,
    )
