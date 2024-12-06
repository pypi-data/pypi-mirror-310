from typing import Optional

from rich import print
import typer
from typing_extensions import Annotated

from ephemeral import __version__
from ephemeral.model import Task, Tracker
from ephemeral.view import (
    display_command_end,
    display_command_start,
    display_version,
    show_current_task,
    show_history,
)

app = typer.Typer()
tracker = Tracker.load()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[Optional[bool], typer.Option("--version")] = False,
) -> None:
    """A simple task tracker with a forgetful history"""
    if version:
        display_version()
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        show_current_task(tracker)


@app.command()
def track(task: str | None = None) -> None:
    """start tracking a new task, or replace your current task"""
    display_command_start("track", tracker)
    if tracker.current_task is not None:
        show_current_task(tracker)
        # TODO mmoran 2024-03-02
        # we should ask if the user wants to save, and if they don't, if
        # they want to discard. if they say no to both, then we can't start a new task
        _ = typer.confirm("    would you like to complete your current task?", abort=True)
        complete()

    # if task is provided on the command line, we don't need to prompt the user
    new_task = task
    if new_task is None:
        new_task = typer.prompt("    what would you like to track?")

    tracker.update(Task(new_task))
    display_command_end("track", tracker)
    tracker.save()


@app.command()
def complete() -> None:
    """finish a task and save it in the history"""
    display_command_start("complete", tracker)

    if tracker.current_task is not None:
        tracker.update(new_task=None)  # this saves current task to history by default
        display_command_end("complete", tracker)
        tracker.save()


@app.command()
def discard() -> None:
    """discard the currently-active task"""
    display_command_start("discard", tracker)

    if tracker.current_task is not None:
        tracker.clear(task=True, history=False)
        display_command_end("discard", tracker)
        tracker.save()
    # TODO mmoran 2024-07-27
    # We should have a sensible response if we try to discard a task when we have none


@app.command()
def history() -> None:
    """display record of completed tasks"""
    display_command_start("history", tracker)
    show_history(tracker)


@app.command()
def clear() -> None:
    """delete all persisted state"""
    display_command_start("clear", tracker)
    if tracker.current_task is not None or len(tracker.history) > 0:
        print("    you have saved history")
        _ = typer.confirm("    would you like to continue?", abort=True)
    if tracker.current_task is not None:
        print("    Clearing the current task...")
    if len(tracker.history) > 0:
        print(f"    Clearing the saved history ({len(tracker.history)} tasks)...")
    tracker.clear(task=True, history=True)
    display_command_end("clear", tracker)
    tracker.save()


if __name__ == "__main__":
    app()
