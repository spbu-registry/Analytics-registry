from fastapi import FastAPI
from pydantic import BaseSettings, Field


class FastAPISettings(BaseSettings):
    """FastAPI settings from environment variables.

    Configuration options must be named in upper snake case as they are constant.

    When more configuration options required add needed fields, add environment
    variables to /settings/debug.env and /settings/docker.env and modify create_fastapi
    method.
    """

    DEBUG: bool = Field(
        default=False,
        description="When true debug traceback should be returned on errors",
    )
    TITLE: str = Field(
        default="analytics-service",
        description="Name of the API",
    )
    DESCRIPTION: str = Field(
        default="Main service for analytics management",
        description="Short explanation of API role",
    )
    VERSION: str = Field(
        default="0.0.1",
        description="Currently used version of API",
    )
    ROOT_PATH: str = Field(
        default="",
        description="Root path of all routes of application",
    )

    CORS_ALLOW_ORIGINS: list[str] = Field(
        default=["*"],
        description="Which origins are allowed",
        example='["*"]',
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True,
        description="Whether to expose response to browser or not",
    )
    CORS_ALLOW_METHODS: list[str] = Field(
        default=["*"],
        description="Which methods are allowed",
        example='["*"]',
    )
    CORS_ALLOW_HEADERS: list[str] = Field(
        default=["*"],
        description="Which headers are allowed",
        example='["*"]',
    )

    USE_DEFAULT_PING: bool = Field(
        default=True,
        description="Whether to include or default /ping endpoint",
    )
    USE_DEFAULT_HEALTH: bool = Field(
        default=False,
        description="Whether to include or not default /health endpoint",
    )

    class Config:  # noqa
        env_prefix = "FASTAPI_"
        frozen = True

    def create_fastapi(self) -> FastAPI:
        """Initialize common FastAPI middleware.

        Returns:
            FastAPI: configured based on settings class.
        """
        return FastAPI(
            debug=self.DEBUG,
            title=self.TITLE,
            description=self.DESCRIPTION,
            version=self.VERSION,
            root_path=self.ROOT_PATH,
        )
