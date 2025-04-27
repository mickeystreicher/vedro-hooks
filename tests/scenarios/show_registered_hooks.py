from unittest.mock import Mock

from contexts import registered_plugin
from vedro.events import CleanupEvent
from vedro_fn import given, scenario, then, when

from vedro_hooks import on_scenario_run
from vedro_hooks.hooks import Hooks


@scenario()
async def show_hooks_disabled_by_default():
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks)

        on_scenario_run(lambda event: None, hooks=hooks)

        report = Mock()

    with when:
        await dispatcher.fire(CleanupEvent(report))

    with then:
        report.add_summary.assert_not_called()


@scenario()
async def show_hooks_when_no_hooks_registered():
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks, show_hooks=True)

        report = Mock()

    with when:
        await dispatcher.fire(CleanupEvent(report))

    with then:
        report.add_summary.assert_called_once_with("[vedro-hooks] Hooks: No hooks registered")


@scenario()
async def show_hooks_when_hooks_registered():
    with given:
        hooks = Hooks()
        dispatcher = registered_plugin(hooks, show_hooks=True)

        on_scenario_run(lambda event: None, hooks=hooks)

        report = Mock()

    with when:
        await dispatcher.fire(CleanupEvent(report))

    with then:
        report.add_summary.assert_called_once()
