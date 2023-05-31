from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolz import pipe

from .dependencies import Container
from .settings import FastAPISettings


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize common FastAPI middleware.

    Args:
        app (FastAPI): to bootstrap with common middleware.

    Returns:
        FastAPI: bootstrapped with common middleware.
    """
    return pipe(
        app,
        __bootstrap_cors,
    )


@inject
def __bootstrap_cors(
    app: FastAPI,
    fastapi_settings: FastAPISettings = Provide[Container.fastapi_settings],
) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=fastapi_settings.CORS_ALLOW_ORIGINS,
        allow_credentials=fastapi_settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=fastapi_settings.CORS_ALLOW_METHODS,
        allow_headers=fastapi_settings.CORS_ALLOW_HEADERS,
    )
    return app
