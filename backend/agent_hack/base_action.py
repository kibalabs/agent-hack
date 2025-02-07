from collections.abc import Callable

from pydantic import BaseModel


class BaseAction(BaseModel):
    """Base Action Class."""

    name: str
    description: str
    args_schema: type[BaseModel] | None = None  # pylint: disable=invalid-name
    func: Callable[..., str] | None = None
    afunc: Callable[..., str] | None = None
