from fastapi import FastAPI


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize common FastAPI error handlers.

    Args:
        app (FastAPI): to bootstrap with common error handlers.

    Returns:
        FastAPI: bootstrapped with common error handlers.
    """
    return app
