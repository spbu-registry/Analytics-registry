from fastapi import FastAPI


def bootstrap(app: FastAPI) -> FastAPI:
    """Initialize common FastAPI event handlers.

    Args:
        app (FastAPI): to bootstrap with common event handlers.

    Returns:
        FastAPI: bootstrapped with common event handlers.
    """
    return app
