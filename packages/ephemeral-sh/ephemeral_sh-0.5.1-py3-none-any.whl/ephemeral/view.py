import datetime

from rich.console import Console

from ephemeral import __version__
from ephemeral.model import Task, Tracker

console = Console()
SUCCESS = "[bold blue][*][/]"
INFO = "[bold green][+][/]"
CONFUSED = "[bold yellow][?][/]"
WARNING = "[bold red][!][/]"


def display_version() -> None:
    console.print(f"[white bold][?][/] {__package__} {__version__}")


def display_command_start(command: str, tracker: Tracker) -> None:
    """show the command message based on what we're trying to do"""
    # commands on the active task
    if command == "track":
        message = f"{SUCCESS} ephemeral is starting a new task"

    elif command == "complete":
        message = f"{CONFUSED} ephemeral is not tracking anything"
        if tracker.current_task is not None:
            message = (
                f"{SUCCESS} ephemeral is completing [bold white]{tracker.current_task.task}[/]"
            )

    elif command == "discard":
        message = f"{CONFUSED} ephemeral is not tracking anything"
        if tracker.current_task is not None:
            message = (
                f"{WARNING} ephemeral is discarding [bold white]{tracker.current_task.task}[/]"
            )

    # commands on the history
    elif command == "clear":
        message = f"{CONFUSED} ephemeral has no memory"
        if tracker.current_task is not None or len(tracker.history) > 0:
            message = f"{WARNING} ephemeral is clearing all recorded history"

    elif command == "history":
        message = f"{CONFUSED} ephemeral has no memory"
        if tracker.current_task is not None or len(tracker.history) > 0:
            message = f"{INFO} ephemeral remembers its history"

    else:
        message = f"[bold red][!] command `{command}` not found[/]"

    console.print(message, overflow="ellipsis", no_wrap=True)


def display_command_end(command: str, tracker: Tracker) -> None:
    """show a confirmation message at the end of a command"""
    if command == "track":
        message = f"{CONFUSED} ephemeral did not start a task"
        if tracker.current_task is not None:
            message = (
                f"{SUCCESS} ephemeral is now tracking [bold white]{tracker.current_task.task}[/]"
            )

    elif command == "complete":
        message = f"{INFO} ephemeral has remembered this task"

    elif command == "discard":
        message = f"{WARNING} ephemeral has discarded this task"

    elif command == "clear":
        message = f"{SUCCESS} ephemeral has forgotten"

    else:
        message = f"[bold red][!] command `{command}` not found[/]"

    console.print(message, overflow="ellipsis", no_wrap=True)


def show_current_task(tracker: Tracker) -> None:
    message = f"{CONFUSED} no active task found"

    if tracker.current_task is not None:
        message = f"{INFO} tracking [white bold]{tracker.current_task.task}[/]"

    console.print(message, overflow="ellipsis", no_wrap=True)


def show_history(tracker: Tracker) -> None:
    if tracker.current_task is not None:
        console.print(f"{INFO} active task found")
        history_task(tracker.current_task)

    if not tracker.history:
        console.print(f"{CONFUSED} no tasks have been completed")
    else:
        console.print(f"{INFO} completed history found")
        for task in tracker.history[::-1]:
            history_task(task)


def history_task(task: Task) -> None:
    start_dt = _convert_to_datetime(task.start_ts)
    if task.end_ts is not None:
        end_dt = _convert_to_datetime(task.end_ts)
        end_dt_string = f"{end_dt:%Y-%m-%d}"
    else:
        end_dt_string = "now"

    message = f"    [bold black]{start_dt:%Y-%m-%d} -- {end_dt_string}[/]: {task.task}"
    console.print(message, overflow="ellipsis", no_wrap=True)


def _convert_to_datetime(timestamp: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(timestamp)
