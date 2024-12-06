import datetime

from rich.console import Console

from ephemeral.model import Task

console = Console()


class Display:
    def __init__(self, console: Console | None = None) -> None:
        self.console = console if console else Console()

    def show(self, message: str) -> None:
        self.console.print(message, overflow="ellipsis", no_wrap=True)

    def show_task(self, task: Task) -> None:
        self.info(f"tracking [white bold]{task}[/]")

    def show_history_task(self, task: Task) -> None:
        start_dt_string = f"{datetime.datetime.fromtimestamp(task.start_ts):%Y-%m-%d}"
        end_dt_string = "now"
        if task.end_ts is not None:
            end_dt_string = f"{datetime.datetime.fromtimestamp(task.end_ts):%Y-%m-%d}"

        self.show(f"[bold black][ ] {start_dt_string} -- {end_dt_string}[/]: {task}")

    # message types
    def success(self, message: str) -> None:
        self.show(f"[bold blue][*][/] {message}")

    def info(self, message: str) -> None:
        self.show(f"[bold green][+][/] {message}")

    def confused(self, message: str) -> None:
        self.show(f"[bold yellow][?][/] {message}")

    def warning(self, message: str) -> None:
        self.show(f"[bold red][!][/] {message}")

    def diagnostic(self, message: str) -> None:
        self.show(f"[white bold][?][/] {message}")
