from unittest.mock import AsyncMock, Mock

from contexts import HookType
from vedro.events import Event

__all__ = ("assert_called_once_with",)


def assert_called_once_with(hook: HookType, event: Event) -> bool:
    if isinstance(hook, AsyncMock):
        hook.assert_awaited_once_with(event)
    elif isinstance(hook, Mock):
        hook.assert_called_once_with(event)
    else:
        raise TypeError(
            f"Unsupported hook type: {type(hook).__name__}. Expected Mock or AsyncMock.")
    return True
