import sqlalchemy as sa

from app.service.postgres.common.base import Base


class PullRequestEntity(Base):
    """Entity for database relation."""

    __tablename__ = "pull_request"

    uid = sa.Column(
        sa.INTEGER,
        sa.Identity(),
        primary_key=True,
        nullable=False,
    )
    project_id = sa.Column(
        sa.INTEGER,
        nullable=False,
    )
    author_login = sa.Column(
        sa.VARCHAR,
        nullable=False,
    )
    created_at = sa.Column(
        sa.TIMESTAMP(True),
        nullable=False,
    )
    closed_at = sa.Column(
        sa.TIMESTAMP(True),
        nullable=True,
    )
    updated_at = sa.Column(
        sa.TIMESTAMP(False),
        nullable=False,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )
