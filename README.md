# Vedro Hooks

[![PyPI Version](https://img.shields.io/pypi/v/vedro-hooks)](https://pypi.org/project/vedro-hooks/)
[![License](https://img.shields.io/github/license/mickeystreicher/vedro-hooks)](https://github.com/mickeystreicher/vedro-hooks/blob/main/LICENSE)

`vedro-hooks` is a plugin for the [Vedro](https://vedro.io) testing framework that allows you to attach custom hooks to various testing events, such as startup, scenario execution, and cleanup. This enables you to perform specific actions automatically at different stages of the testing lifecycle.

## Installation

To install [vedro-hooks](https://pypi.org/project/vedro-hooks/), you can use the `vedro plugin install` command:

```sh
$ vedro plugin install vedro-hooks
```

Ensure you have Vedro already installed in your environment. If not, you can install it using pip:

```sh
$ pip install vedro
```

## Usage

You can register your custom hooks anywhere in your project; however, it is recommended to register them in the `vedro.cfg.py` file to keep your configuration centralized and easy to locate. Below is an example setup:

```python
from vedro.events import CleanupEvent, ScenarioRunEvent, StartupEvent
from vedro_hooks import on_cleanup, on_scenario_run, on_startup

@on_startup
def my_startup_hook(event: StartupEvent):
    print("Testing started!")

@on_scenario_run
def my_scenario_run_hook(event: ScenarioRunEvent):
    scenario = event.scenario_result.scenario
    print(f"Running scenario: {scenario.subject}")

@on_cleanup
def my_cleanup_hook(event: CleanupEvent):
    print("Testing finished!")

...
```

### Sync and Async Hooks

`vedro-hooks` supports both synchronous and asynchronous hooks, allowing you to handle events in the way that best suits your needs:
- **Sync Hook Example**
    ```python
    @on_scenario_passed
    def my_sync_hook(event):
        scenario = event.scenario_result.scenario
        print(f"Scenario passed: {scenario.subject}")
    ```
- **Async Hook Example**
    ```python
    @on_scenario_failed
    async def my_async_hook(event):
        scenario = event.scenario_result.scenario
        print(f"Scenario failed: {scenario.subject}")
    ```

### Available Decorators

- `@on_startup`: Register a function to be executed when the testing process starts.
- `@on_scenario_run`: Register a function to be executed when a scenario starts running.
- `@on_scenario_passed`: Register a function to be executed when a scenario passes.
- `@on_scenario_failed`: Register a function to be executed when a scenario fails.
- `@on_scenario_skipped`: Register a function to be executed when a scenario is skipped.
- `@on_scenario_reported`: Register a function to be executed when a scenario is reported.
- `@on_cleanup`: Register a function to be executed when the testing process ends.

For more detailed information about the events these decorators can hook into, you can refer to the [Vedro Plugin Guide](https://vedro.io/docs/guides/writing-plugins).

## Configuration

The `VedroHooksPlugin` can be configured using the following options in your `vedro.cfg.py`:

- `show_hooks`: When set to `True`, a summary of all registered hooks will be displayed at the end of the testing process.
- `ignore_errors`: When set to `True`, the plugin will ignore any errors that occur within the hooks and continue the test execution. Errors encountered will be logged and summarized at the end of the testing process.

```python
import vedro
import vedro_hooks

class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class VedroHooks(vedro_hooks.VedroHooks):
            ignore_errors = True
            show_hooks = True
```

### Command-Line Arguments

- **`--hooks-show`:**  
  When enabled, after the testing process completes, a summary of all registered hooks along with their source locations will be displayed. This is useful for debugging and verifying which hooks are active.

- **`--hooks-ignore-errors`:**  
  When enabled, any exceptions raised within your hooks will be caught and logged without interrupting the entire test run. This ensures that one failing hook does not prevent the execution of subsequent tests or hooks.

These CLI arguments take precedence over the configuration specified in `vedro.cfg.py`.
