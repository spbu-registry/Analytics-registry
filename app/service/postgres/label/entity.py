import sqlalchemy as sa

from app.service.postgres.common.base import Base


class LabelEntity(Base):
    """Entity for database relation."""

    __tablename__ = "label"

    uid = sa.Column(
        sa.INTEGER,
        sa.Identity(),
        primary_key=True,
        nullable=False,
    )
    name = sa.Column(
        sa.VARCHAR,
        unique=True,
        nullable=False,
    )
    description = sa.Column(
        sa.VARCHAR,
        nullable=True,
    )
