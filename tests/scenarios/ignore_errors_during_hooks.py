from unittest.mock import Mock

from contexts import registered_plugin, sync_hook
from helpers import assert_called_once_with
from vedro.events import CleanupEvent, ScenarioRunEvent
from vedro_fn import given, scenario, then, when

from vedro_hooks import on_scenario_run
from vedro_hooks.hooks import Hooks


@scenario()
async def ignore_errors_when_no_errors_occur():
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks, ignore_errors=True)

        hook = sync_hook()
        on_scenario_run(hook, hooks=hooks)

        event = ScenarioRunEvent(scenario_result=Mock())
        await dispatcher.fire(event)

        report = Mock()

    with when:
        await dispatcher.fire(CleanupEvent(report))

    with then:
        assert assert_called_once_with(hook, event)
        report.add_summary.assert_not_called()


@scenario()
async def ignore_errors_when_errors_occur():
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks, ignore_errors=True)

        hook = sync_hook(side_effect=ValueError)
        on_scenario_run(hook, hooks=hooks)

        event = ScenarioRunEvent(scenario_result=Mock())
        await dispatcher.fire(event)

        report = Mock()

    with when:
        await dispatcher.fire(CleanupEvent(report))

    with then:
        assert assert_called_once_with(hook, event)
        report.add_summary.assert_called_once_with(
            f"[vedro-hooks] Errors:\n#  - Error in hook '{hook.__name__}': ValueError()")
