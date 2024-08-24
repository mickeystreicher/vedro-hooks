from asyncio import iscoroutinefunction
from os import linesep
from typing import List, Type, TypeVar

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
        self._ignore_errors = config.ignore_errors
        self._errors: List[str] = []

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(StartupEvent, self.on_event) \
                  .listen(ScenarioRunEvent, self.on_event) \
                  .listen(ScenarioPassedEvent, self.on_event) \
                  .listen(ScenarioFailedEvent, self.on_event) \
                  .listen(ScenarioSkippedEvent, self.on_event) \
                  .listen(ScenarioReportedEvent, self.on_event) \
                  .listen(CleanupEvent, self.on_event)

        dispatcher.listen(CleanupEvent, self.on_cleanup)

    async def on_event(self, event: Event) -> None:
        for hook in self._hooks.get_hooks(event):
            try:
                await self.run_hook(hook, event)
            except BaseException as e:
                if not self._ignore_errors:
                    raise
                self._errors.append(f"Error in hook '{hook.__name__}': {e!r}")

    async def run_hook(self, hook: HookType, event: Event) -> None:
        if iscoroutinefunction(hook):
            await hook(event)
        else:
            hook(event)

    async def on_cleanup(self, event: CleanupEvent) -> None:
        if self._errors:
            error_prefix = f"{linesep}#  - "
            summary = f"Vedro Hooks:{error_prefix}" + f"{error_prefix}".join(self._errors)
            event.report.add_summary(summary)


class VedroHooks(PluginConfig):
    plugin = VedroHooksPlugin
    description = ("Enables custom hooks for Vedro, "
                   "allowing actions on events like startup, scenario execution, and cleanup")

    ignore_errors: bool = False
