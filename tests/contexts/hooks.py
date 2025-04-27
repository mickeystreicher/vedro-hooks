from typing import Any, Awaitable, Callable, Optional, TypeVar, Union
from unittest.mock import AsyncMock, Mock

__all__ = ("sync_hook", "async_hook", "HookType",)


EventT = TypeVar("EventT")

SyncHook = Callable[[EventT], Any]
AsyncHook = Callable[[EventT], Awaitable[Any]]

HookType = Union[SyncHook, AsyncHook]


def sync_hook(side_effect: Optional[Exception] = None) -> SyncHook:
    return Mock(__name__="hook", side_effect=side_effect)


def async_hook(side_effect: Optional[Exception] = None) -> AsyncHook:
    return AsyncMock(__name__="hook", side_effect=side_effect)
