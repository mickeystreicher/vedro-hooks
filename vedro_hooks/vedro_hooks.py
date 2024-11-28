import inspect
from asyncio import iscoroutinefunction
from os import linesep
from typing import List, Type, TypeVar

from vedro.core import Dispatcher, Plugin, PluginConfig
from vedro.events import (ArgParsedEvent, ArgParseEvent, CleanupEvent, Event, ScenarioFailedEvent, ScenarioPassedEvent,
                          ScenarioReportedEvent, ScenarioRunEvent, ScenarioSkippedEvent, StartupEvent)

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
        self._show_hooks = config.show_hooks
        self._ignore_errors = config.ignore_errors
        self._errors: List[str] = []

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ArgParseEvent, self.on_arg_parse) \
                  .listen(ArgParsedEvent, self.on_arg_parsed) \
                  .listen(StartupEvent, self.on_event) \
                  .listen(ScenarioRunEvent, self.on_event) \
                  .listen(ScenarioPassedEvent, self.on_event) \
                  .listen(ScenarioFailedEvent, self.on_event) \
                  .listen(ScenarioSkippedEvent, self.on_event) \
                  .listen(ScenarioReportedEvent, self.on_event) \
                  .listen(CleanupEvent, self.on_event)

        dispatcher.listen(CleanupEvent, self.on_cleanup)

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        group = event.arg_parser.add_argument_group("Vedro Hooks")
        group.add_argument("--hooks-show", action="store_true", default=self._show_hooks,
                           help="Show registered hooks in the cleanup summary")
        group.add_argument("--hooks-ignore-errors", action="store_true", default=self._ignore_errors,
                           help="Ignore errors in hooks and continue execution")

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._show_hooks = event.args.hooks_show
        self._ignore_errors = event.args.hooks_ignore_errors

    async def on_event(self, event: Event) -> None:
        for hook in self._hooks.get_hooks(event):
            try:
                await self._run_hook(hook, event)
            except BaseException as e:
                if not self._ignore_errors:
                    raise
                self._errors.append(f"Error in hook '{hook.__name__}': {e!r}")

    async def _run_hook(self, hook: HookType, event: Event) -> None:
        if iscoroutinefunction(hook):
            await hook(event)
        else:
            hook(event)

    async def on_cleanup(self, event: CleanupEvent) -> None:
        if self._show_hooks:
            hooks = self._get_hooks()
            if hooks:
                hook_prefix = f"{linesep}#  - "
                event.report.add_summary(
                    f"[vedro-hooks] Hooks:{hook_prefix}" + f"{hook_prefix}".join(hooks))
            else:
                event.report.add_summary("[vedro-hooks] Hooks: No hooks registered")

        if self._errors:
            error_prefix = f"{linesep}#  - "
            event.report.add_summary(
                f"[vedro-hooks] Errors:{error_prefix}" + f"{error_prefix}".join(self._errors))

    def _get_hooks(self) -> List[str]:
        hooks = []
        for event_name, hook in self._hooks.get_all_hooks():
            hook_file = inspect.getfile(hook)
            hook_line = inspect.getsourcelines(hook)[1]
            hooks.append(f"'{hook.__name__}' ({event_name}) {hook_file}:{hook_line}")
        return hooks


class VedroHooks(PluginConfig):
    plugin = VedroHooksPlugin
    description = ("Enables custom hooks for Vedro, "
                   "allowing actions on events like startup, scenario execution, and cleanup")

    show_hooks: bool = False
    ignore_errors: bool = False
