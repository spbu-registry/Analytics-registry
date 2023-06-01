from dependency_injector import containers, providers
from fastapi import FastAPI

from app.service.postgres.common.settings import PostgresSettings

from .settings import FastAPISettings


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize common FastAPI dependencies.

    Important that there we do not configure and wire Container. It is done in FastAPI
    factory function in app.api.main module.

    Args:
        app (FastAPI): to bootstrap with global dependencies.

    Returns:
        FastAPI: bootstrapped with global dependencies.
    """
    return app


class Container(containers.DeclarativeContainer):
    """Container for dependencies used in API presentation layer.

    Highly suggested to use Object provider for BaseSettings as Configuration provider
    just looses all typing, validation and logic that might be the part of settings.

    When some dependency must be configured at startup use Abstract dependencies and
    override them on application startup.
    """

    fastapi_settings = providers.Object(FastAPISettings())
    postgres_settings = providers.Object(PostgresSettings())

    postgres_db = providers.AbstractSingleton()

    commit_repository = providers.AbstractFactory()
    project_repository = providers.AbstractFactory()
    pull_request_repository = providers.AbstractFactory()
    issue_repository = providers.AbstractFactory()

    commit_service = providers.AbstractSingleton()
    project_service = providers.AbstractSingleton()
    pull_request_service = providers.AbstractSingleton()
    issue_service = providers.AbstractSingleton()
