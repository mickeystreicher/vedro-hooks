from typing import Awaitable, Callable, Dict, Generator, List, Tuple, Type, Union

from vedro.events import Event

__all__ = ("Hooks", "HookType")

HookType = Callable[[Event], Union[None, Awaitable[None]]]


class Hooks:
    def __init__(self) -> None:
        self._hooks: Dict[str, List[HookType]] = {}

    def register_hook(self, hook: HookType, event: Type[Event]) -> None:
        event_name = event.__name__
        if event_name not in self._hooks:
            self._hooks[event_name] = []
        self._hooks[event_name].append(hook)

    def get_hooks(self, event: Event) -> List[HookType]:
        event_name = event.__class__.__name__
        return self._hooks.get(event_name, [])

    def get_all_hooks(self) -> Generator[Tuple[str, HookType], None, None]:
        for event_name, hooks in self._hooks.items():
            for hook in hooks:
                yield (event_name, hook)
