from typing import Any

from vedro.core import Dispatcher

from vedro_hooks import VedroHooks, VedroHooksPlugin
from vedro_hooks.hooks import Hooks

__all__ = ("registered_plugin",)


def registered_plugin(hooks: Hooks, **kwargs: Any) -> Dispatcher:
    dispatcher = Dispatcher()

    class VedroHooksConf(VedroHooks):
        show_hooks = kwargs.get("show_hooks", False)
        ignore_errors = kwargs.get("ignore_errors", False)

    plugin = VedroHooksPlugin(VedroHooksConf, hooks=hooks)
    plugin.subscribe(dispatcher)

    return dispatcher
