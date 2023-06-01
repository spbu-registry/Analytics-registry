import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from app.service.postgres.common.base import Base
from app.service.postgres.label.entity import LabelEntity


class IssueEntity(Base):
    """Entity for database relation."""

    __tablename__ = "issue"

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
    labels: Mapped[list[LabelEntity]] = relationship(
        "LabelEntity",
        secondary="issue_label",
        backref="issue",
        lazy="joined",
    )
    updated_at = sa.Column(
        sa.TIMESTAMP(False),
        nullable=False,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )


class IssueLabelEntity(Base):
    """Entity for database relation."""

    __tablename__ = "issue_label"

    uid = sa.Column(
        sa.INTEGER,
        sa.Identity(),
        primary_key=True,
        nullable=False,
    )
    issue_uid = sa.Column(
        sa.INTEGER,
        sa.ForeignKey(
            "issue.uid",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    label_uid = sa.Column(
        sa.INTEGER,
        sa.ForeignKey(
            "label.uid",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
