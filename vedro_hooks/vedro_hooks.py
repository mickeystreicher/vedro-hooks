from asyncio import iscoroutinefunction
from typing import Type, TypeVar

from vedro.core import Dispatcher, Plugin, PluginConfig
from vedro.events import (CleanupEvent, Event, ScenarioFailedEvent, ScenarioPassedEvent, ScenarioReportedEvent,
                          ScenarioRunEvent, ScenarioSkippedEvent, StartupEvent)

from .hooks import Hooks, HookType

__all__ = ("VedroHooks", "VedroHooksPlugin")


_hooks = Hooks()

T = TypeVar("T", bound=HookType)


def on_startup(fn: T, *, hooks: Hooks = _hooks) -> T:
    hooks.register_hook(fn, StartupEvent)
    return fn


def on_scenario_run(fn: T, *, hooks: Hooks = _hooks) -> T:
    hooks.register_hook(fn, ScenarioRunEvent)
    return fn


def on_scenario_passed(fn: T, *, hooks: Hooks = _hooks) -> T:
    hooks.register_hook(fn, ScenarioPassedEvent)
    return fn


def on_scenario_failed(fn: T, *, hooks: Hooks = _hooks) -> T:
    hooks.register_hook(fn, ScenarioFailedEvent)
    return fn


def on_scenario_skipped(fn: T, *, hooks: Hooks = _hooks) -> T:
    hooks.register_hook(fn, ScenarioSkippedEvent)
    return fn


def on_scenario_reported(fn: T, *, hooks: Hooks = _hooks) -> T:
    hooks.register_hook(fn, ScenarioReportedEvent)
    return fn


def on_cleanup(fn: T, *, hooks: Hooks = _hooks) -> T:
    hooks.register_hook(fn, CleanupEvent)
    return fn


class VedroHooksPlugin(Plugin):
    def __init__(self, config: Type["VedroHooks"], *, hooks: Hooks = _hooks) -> None:
        super().__init__(config)
        self._hooks = hooks

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(StartupEvent, self.on_event) \
                  .listen(ScenarioRunEvent, self.on_event) \
                  .listen(ScenarioPassedEvent, self.on_event) \
                  .listen(ScenarioFailedEvent, self.on_event) \
                  .listen(ScenarioSkippedEvent, self.on_event) \
                  .listen(ScenarioReportedEvent, self.on_event) \
                  .listen(CleanupEvent, self.on_event)

    async def on_event(self, event: Event) -> None:
        for hook in self._hooks.get_hooks(event):
            if iscoroutinefunction(hook):
                await hook(event)
            else:
                hook(event)


class VedroHooks(PluginConfig):
    plugin = VedroHooksPlugin
    description = ("Enables custom hooks for Vedro, "
                   "allowing actions on events like startup, scenario execution, and cleanup")
