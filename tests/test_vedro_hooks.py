import unittest
from unittest.mock import AsyncMock, Mock

from parameterized import parameterized
from vedro.core import Dispatcher
from vedro.events import (CleanupEvent, ScenarioFailedEvent, ScenarioPassedEvent, ScenarioReportedEvent,
                          ScenarioRunEvent, ScenarioSkippedEvent, StartupEvent)

from vedro_hooks import (VedroHooks, VedroHooksPlugin, on_cleanup, on_scenario_failed, on_scenario_passed,
                         on_scenario_reported, on_scenario_run, on_scenario_skipped, on_startup)
from vedro_hooks.hooks import Hooks


class TestVedroHooksPlugin(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.hooks = Hooks()
        self.plugin = VedroHooksPlugin(VedroHooks, hooks=self.hooks)

        self.dispatcher = Dispatcher()
        self.plugin.subscribe(self.dispatcher)

    @parameterized.expand([
        (Mock(), "assert_called_once_with"),
        (AsyncMock(), "assert_awaited_once_with"),
    ])
    async def test_on_startup_hook(self, func, assert_method):
        hook = on_startup(func, hooks=self.hooks)
        event = StartupEvent(scheduler=Mock())

        await self.dispatcher.fire(event)

        getattr(hook, assert_method)(event)

    @parameterized.expand([
        (Mock(), "assert_called_once_with"),
        (AsyncMock(), "assert_awaited_once_with"),
    ])
    async def test_on_scenario_run_hook(self, func, assert_method):
        hook = on_scenario_run(func, hooks=self.hooks)
        event = ScenarioRunEvent(scenario_result=Mock())

        await self.dispatcher.fire(event)

        getattr(hook, assert_method)(event)

    @parameterized.expand([
        (Mock(), "assert_called_once_with"),
        (AsyncMock(), "assert_awaited_once_with"),
    ])
    async def test_on_scenario_passed_hook(self, func, assert_method):
        hook = on_scenario_passed(func, hooks=self.hooks)
        event = ScenarioPassedEvent(scenario_result=Mock())

        await self.dispatcher.fire(event)

        getattr(hook, assert_method)(event)

    @parameterized.expand([
        (Mock(), "assert_called_once_with"),
        (AsyncMock(), "assert_awaited_once_with"),
    ])
    async def test_on_scenario_failed_hook(self, func, assert_method):
        hook = on_scenario_failed(func, hooks=self.hooks)
        event = ScenarioFailedEvent(scenario_result=Mock())

        await self.dispatcher.fire(event)

        getattr(hook, assert_method)(event)

    @parameterized.expand([
        (Mock(), "assert_called_once_with"),
        (AsyncMock(), "assert_awaited_once_with"),
    ])
    async def test_on_scenario_skipped_hook(self, func, assert_method):
        hook = on_scenario_skipped(func, hooks=self.hooks)
        event = ScenarioSkippedEvent(scenario_result=Mock())

        await self.dispatcher.fire(event)

        getattr(hook, assert_method)(event)

    @parameterized.expand([
        (Mock(), "assert_called_once_with"),
        (AsyncMock(), "assert_awaited_once_with"),
    ])
    async def test_on_scenario_reported_hook(self, func, assert_method):
        hook = on_scenario_reported(func, hooks=self.hooks)
        event = ScenarioReportedEvent(aggregated_result=Mock())

        await self.dispatcher.fire(event)

        getattr(hook, assert_method)(event)

    @parameterized.expand([
        (Mock(), "assert_called_once_with"),
        (AsyncMock(), "assert_awaited_once_with"),
    ])
    async def test_on_cleanup_hook(self, func, assert_method):
        hook = on_cleanup(func, hooks=self.hooks)
        event = CleanupEvent(report=Mock())

        await self.dispatcher.fire(event)

        getattr(hook, assert_method)(event)


if __name__ == "__main__":
    unittest.main()
