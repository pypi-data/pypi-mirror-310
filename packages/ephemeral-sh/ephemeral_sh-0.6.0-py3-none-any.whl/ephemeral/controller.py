from ephemeral import __version__
from ephemeral.display import Display
from ephemeral.model import Tracker


class Controller:
    def __init__(self, tracker: Tracker | None = None, display: Display | None = None) -> None:
        self.tracker = tracker if tracker else Tracker.load()
        self.display = display if display else Display()

    @property
    def active(self) -> bool:
        return len(self.tracker) > 0

    @property
    def tracking(self) -> bool:
        return self.tracker.current_task is not None

    def start_new_task(self, task: str) -> None:
        self.tracker.update(task)
        self.tracker.save()
        self.display.success(f"ephemeral is now tracking [bold white]{task}[/]")

    def complete_current_task(self) -> None:
        if not self.tracking:
            self.display.confused("ephemeral is not tracking anything")
            raise ControllerError("no task to complete")

        self.display.success(f"ephemeral is completing [bold white]{self.tracker.current_task}[/]")
        self.tracker.update(new_task=None)  # this saves current task to history by default
        self.tracker.save()
        self.display.success("ephemeral has remembered this task")

    # show

    def show_current_task(self) -> None:
        if not self.tracking:
            self.display.confused("ephemeral is not tracking anything")
            raise ControllerError("no task to show")

        self.display.show_task(self.tracker.current_task)

    def show_history(self) -> None:
        if not self.active:
            self.display.confused("ephemeral has no memory of the past")
            raise ControllerError("no memory to show")

        self.display.info("ephemeral remembers its history")
        if not self.tracking:
            self.display.show_task(self.tracker.current_task)

        self.display.info("available history")
        history = self.tracker.history[::-1]
        if self.tracking:
            history.insert(0, self.tracker.current_task)
        for task in history:
            self.display.show_history_task(task)

    # discarding

    def discard_current_task(self) -> None:
        if not self.tracking:
            self.display.confused("ephemeral is not tracking anything")
            raise ControllerError("no task to discard")

        self.display.warning(f"ephemeral is forgetting [bold white]{self.tracker.current_task}[/]")
        self.tracker.clear(task=True, history=False)
        self.tracker.save()
        self.display.success("ephemeral has forgotten")

    def discard_history(self) -> None:
        if not self.active:
            self.display.confused("ephemeral has no memory of the past")
            raise ControllerError("no history to discard")

        self.display.warning(
            f"ephemeral is forgetting [bold white]{len(self.tracker)} completed tasks[/]"
        )
        self.tracker.clear(task=False, history=True)
        self.tracker.save()
        self.display.success("ephemeral has forgotten")

    # warnings

    def warn_current_task(self) -> None:
        if self.tracking:
            self.display.warning("ephemeral remembers its present")

    def warn_history(self) -> None:
        if self.active:
            self.display.warning("ephemeral remembers its past")

    # diagnostics

    def show_version(self) -> None:
        self.display.diagnostic(f"{__package__} {__version__}")

    def show_no_change(self) -> None:
        self.display.diagnostic("ephemeral has not changed")

    def prompt_continue(self) -> None:
        self.display.diagnostic("would you like to continue?")


class ControllerError(Exception):
    pass
