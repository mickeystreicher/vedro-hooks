from unittest.mock import Mock

from contexts import HookType, async_hook, registered_plugin, sync_hook
from helpers import assert_called_once_with
from vedro import catched, params
from vedro.events import (CleanupEvent, ScenarioFailedEvent, ScenarioPassedEvent,
                          ScenarioReportedEvent, ScenarioRunEvent, ScenarioSkippedEvent,
                          StartupEvent)
from vedro_fn import given, scenario, then, when

from vedro_hooks import (on_cleanup, on_scenario_failed, on_scenario_passed, on_scenario_reported,
                         on_scenario_run, on_scenario_skipped, on_startup)
from vedro_hooks.hooks import Hooks


@scenario([
    params(sync_hook()),
    params(async_hook()),
])
async def trigger_on_startup_hook(hook: HookType):
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks)

        on_startup(hook, hooks=hooks)
        event = StartupEvent(scheduler=Mock())

    with when:
        await dispatcher.fire(event)

    with then:
        assert assert_called_once_with(hook, event)


@scenario([
    params(sync_hook()),
    params(async_hook()),
])
async def trigger_on_scenario_run_hook(hook: HookType):
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks)

        on_scenario_run(hook, hooks=hooks)
        event = ScenarioRunEvent(scenario_result=Mock())

    with when:
        await dispatcher.fire(event)

    with then:
        assert assert_called_once_with(hook, event)


@scenario([
    params(sync_hook()),
    params(async_hook()),
])
async def trigger_on_scenario_passed_hook(hook: HookType):
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks)

        on_scenario_passed(hook, hooks=hooks)
        event = ScenarioPassedEvent(scenario_result=Mock())

    with when:
        await dispatcher.fire(event)

    with then:
        assert assert_called_once_with(hook, event)


@scenario([
    params(sync_hook()),
    params(async_hook()),
])
async def trigger_on_scenario_failed_hook(hook: HookType):
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks)

        on_scenario_failed(hook, hooks=hooks)
        event = ScenarioFailedEvent(scenario_result=Mock())

    with when:
        await dispatcher.fire(event)

    with then:
        assert assert_called_once_with(hook, event)


@scenario([
    params(sync_hook()),
    params(async_hook()),
])
async def trigger_on_scenario_skipped_hook(hook: HookType):
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks)

        on_scenario_skipped(hook, hooks=hooks)
        event = ScenarioSkippedEvent(scenario_result=Mock())

    with when:
        await dispatcher.fire(event)

    with then:
        assert assert_called_once_with(hook, event)


@scenario([
    params(sync_hook()),
    params(async_hook()),
])
async def trigger_on_scenario_reported_hook(hook: HookType):
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks)

        on_scenario_reported(hook, hooks=hooks)
        event = ScenarioReportedEvent(aggregated_result=Mock())

    with when:
        await dispatcher.fire(event)

    with then:
        assert assert_called_once_with(hook, event)


@scenario([
    params(sync_hook()),
    params(async_hook()),
])
async def trigger_on_cleanup_hook(hook: HookType):
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks)

        on_cleanup(hook, hooks=hooks)
        event = CleanupEvent(report=Mock())

    with when:
        await dispatcher.fire(event)

    with then:
        assert assert_called_once_with(hook, event)


@scenario()
async def trigger_hook_with_error():
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks)

        hook = sync_hook(side_effect=ValueError)
        on_scenario_run(hook, hooks=hooks)

        event = ScenarioRunEvent(scenario_result=Mock())

    with when, catched(ValueError) as exc_info:
        await dispatcher.fire(event)

    with then:
        assert exc_info.type is ValueError
        assert assert_called_once_with(hook, event)
