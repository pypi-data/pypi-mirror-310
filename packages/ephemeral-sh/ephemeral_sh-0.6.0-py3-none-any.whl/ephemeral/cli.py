from typing import Callable, Optional

import typer
from typing_extensions import Annotated

from ephemeral.controller import Controller, ControllerError

app = typer.Typer()
controller = Controller()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[Optional[bool], typer.Option("--version")] = False,
) -> None:
    """A simple task tracker with a forgetful history"""
    if version:
        safe_exit(controller.show_version)

    if ctx.invoked_subcommand is None:
        safe_exit(controller.show_current_task)


@app.command()
def track(task: str | None = None) -> None:
    """start tracking a new task, or replace your current task"""
    if controller.tracking:
        controller.warn_current_task()
        prompt_for_confirmation()

        do_complete = typer.confirm("[>] do you want to complete your current task?")
        if do_complete:
            controller.complete_current_task()
        else:
            controller.discard_current_task()

    if task is None:
        task = typer.prompt("[>] what would you like to track?")

    # TODO(mmoran): figure out how to handle unquoted tasks
    # if isinstance(task, tuple):
    #     task = " ".join(task)

    controller.start_new_task(task)


@app.command()
def complete() -> None:
    """finish a task and save it in the history"""
    safe_exit(controller.complete_current_task)


@app.command()
def discard() -> None:
    """discard the currently-active task"""
    controller.warn_current_task()
    safe_exit(controller.discard_current_task)


@app.command()
def history() -> None:
    """display record of completed tasks"""
    safe_exit(controller.show_history)


@app.command()
def clear() -> None:
    """delete all persisted state"""
    if not controller.active:
        controller.show_no_change()
        raise typer.Exit()

    controller.warn_current_task()
    controller.warn_history()

    prompt_for_confirmation()

    safe_exit(controller.discard_current_task)
    safe_exit(controller.discard_history)


def prompt_for_confirmation() -> None:
    controller.prompt_continue()
    selection = typer.confirm("[>]")

    if not selection:
        controller.show_no_change()
        raise typer.Exit()


def safe_exit(callable: Callable, *args) -> None:
    try:
        callable(*args)
    except ControllerError:
        raise typer.Exit()


if __name__ == "__main__":
    app()
