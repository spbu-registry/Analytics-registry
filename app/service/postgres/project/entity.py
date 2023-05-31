import sqlalchemy as sa

from app.service.postgres.common.base import Base


class ProjectEntity(Base):
    """Entity for database relation."""

    __tablename__ = "project"

    uid = sa.Column(
        sa.INTEGER,
        sa.Identity(),
        primary_key=True,
        nullable=False,
    )
    links = sa.Column(
        sa.ARRAY(sa.String),
        nullable=False,
    )
    updated_at = sa.Column(
        sa.TIMESTAMP(False),
        nullable=False,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )
