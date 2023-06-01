from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any

from pydantic import BaseModel
from toolz import curried, pipe


@dataclass
class Base(Exception):  # noqa
    """Base abstraction for errors."""

    message: str = field(default="error")
    code: str = field(default="ERROR-001")
    trace: Exception | None = field(default=None)

    def to_dict(self) -> dict[str, Any]:  # noqa
        # TODO optimize
        return pipe(
            self,
            asdict,
            curried.valfilter(lambda value: value is not None),
            curried.valmap(
                lambda value: asdict(value) if is_dataclass(value) else value
            ),
            curried.valmap(
                lambda value: value.dict(exclude_none=True)
                if isinstance(value, BaseModel)
                else value
            ),
            curried.valmap(
                lambda value: str(value) if isinstance(value, Exception) else value
            ),
        )  # type: ignore


@dataclass
class Vault(Base):  # noqa
    """Common error for store-related errors."""

    message: str = "Error on database query execution"
    code: str = "STORE-001"


@dataclass
class ExternalAPI(Base):  # noqa
    """Common error for API-related errors."""

    message: str = "Error on external API call"
    code: str = "EXTERNAL-API-001"


@dataclass
class EntityNotFound(Base):  # noqa
    """Common error for API-related errors."""

    message: str = "Entity not found"
    code: str = "Entity-Not-Found-404"
