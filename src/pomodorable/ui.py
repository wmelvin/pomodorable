from __future__ import annotations

from datetime import datetime, timedelta

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input, Label, Log, Static

APP_NAME = "Pomodorable"

DEFAULT_SESSION_SECONDS = 25 * 60  # TODO: settings.default_session_minutes


class CountdownDisplay(Static):
    """[00:]00:00 ([hours:]minutes:seconds)"""

    seconds = reactive(DEFAULT_SESSION_SECONDS)
    start_seconds: int = DEFAULT_SESSION_SECONDS
    start_time: datetime | None = None
    pause_time: datetime | None = None
    seconds_added: int = 0

    def on_mount(self) -> None:
        self.set_interval(1 / 5, self.update_countdown)

    def update_countdown(self) -> None:
        if self.app.has_class("paused"):
            self.seconds = self.start_seconds - (
                self.pause_time - self.start_time
            ).seconds
        elif self.app.has_class("running"):
            self.seconds = self.start_seconds - (
                datetime.now() - self.start_time
            ).seconds
        self.seconds += self.seconds_added
        if self.seconds <= 0:
            self.app.countdown_finished()

    def watch_seconds(self, seconds: datetime) -> None:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            self.update(f"{hours:02}:{minutes:02}:{seconds:02}")
        else:
            self.update(f"{minutes:02}:{seconds:02}")

    def add_minutes(self, minutes: int) -> None:
        self.seconds += minutes * 60
        if self.seconds < 0:
            self.seconds = 0

    def reset(self) -> None:
        self.seconds = DEFAULT_SESSION_SECONDS
        self.start_time = None
        self.pause_time = None
        self.seconds_added = 0

    def set_start_time(self) -> None:
        self.start_time = datetime.now()
        self.start_seconds = self.seconds

    def pause(self) -> None:
        self.pause_time = datetime.now()

    def resume(self) -> None:
        self.pause_time = None

    def extend(self) -> None:
        if self.pause_time:
            extend_secs = (datetime.now() - self.pause_time).seconds
            self.seconds_added += extend_secs
        self.pause_time = None

    def remaining_seconds(self):
        return self.seconds


class TimeDisplay(Static):
    """00:00:00 (hours:minutes:seconds)"""

    time = reactive(datetime.now())
    add_seconds: int = 0

    def on_mount(self) -> None:
        self.set_interval(1 / 5, self.update_time)

    def set_add_seconds(self, add_seconds: int) -> None:
        self.add_seconds = add_seconds
        self.time = datetime.now() + timedelta(seconds=self.add_seconds)

    def update_time(self) -> None:
        if not self.app.has_class("running"):
            if self.add_seconds:
                self.time = datetime.now() + timedelta(seconds=self.add_seconds)
            else:
                self.time = datetime.now()

    def watch_time(self, time: datetime) -> None:
        self.update(f"{time.strftime('%H:%M:%S')}")


class PomodoroApp(App):
    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("x", "exit_app", "Exit"),
        ("t", "ten_seconds", "Ten"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            Label("Countdown:"),
            CountdownDisplay("25:00", id="countdown"),
            Label("Start:"),
            TimeDisplay("14:05:00", id="time-started"),
            Label("End:"),
            TimeDisplay("14:30:00", id="time-ending"),
            id="frm-times",
        )
        yield Horizontal(
            Button("Reset", id="btn-reset"),
            Button("+ 5 min", id="btn-plus-five"),
            Button("- 5 min", id="btn-minus-five"),
            id="frm-set",
        )
        yield Horizontal(
            Button("Start", id="btn-start"),
            Input(id="input-task", placeholder="(task description)"),
            id="frm-start",
        )
        yield Horizontal(
            Button("Pause", id="btn-pause"),
            Input(id="input-reason", placeholder="(reason)"),
            id="frm-pause",
        )
        yield Horizontal(
            Button("Resume", id="btn-resume"),
            Button("Extend", id="btn-extend"),
            Button("Stop", id="btn-stop"),
            id="frm-paused",
        )
        yield Log()
        yield Footer()

    def on_mount(self) -> None:
        self.title = APP_NAME
        log = self.query_one(Log)
        log.write_line("Hello.")
        time_disp = self.query_one("#time-ending")
        time_disp.set_add_seconds(DEFAULT_SESSION_SECONDS)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id

        log = self.query_one(Log)
        log.write_line(f"You pressed [{btn}].")
        countdown = self.query_one(CountdownDisplay)

        if btn == "btn-reset":
            countdown.reset()

        elif btn == "btn-plus-five":
            countdown.add_minutes(5)

        elif btn == "btn-minus-five":
            countdown.add_minutes(-5)

        elif btn == "btn-start":
            countdown.set_start_time()
            self.add_class("running")

        elif btn == "btn-pause":
            if not self.has_class("paused"):
                countdown.pause()
                self.add_class("paused")

        elif btn == "btn-resume":
            countdown.resume()
            self.remove_class("paused")

        elif btn == "btn-extend":
            countdown.extend()
            time_ending = self.query_one("#time-ending")
            time_ending.set_add_seconds(countdown.remaining_seconds())
            self.remove_class("paused")

        elif btn == "btn-stop":
            self.remove_class("paused")
            self.remove_class("running")
            countdown.reset()

    def countdown_finished(self):
        if self.has_class("running"):
            countdown = self.query_one(CountdownDisplay)
            time_ending = self.query_one("#time-ending")
            self.remove_class("paused")
            self.remove_class("running")
            time_ending.set_add_seconds(0)
            countdown.reset()

    def action_ten_seconds(self) -> None:
        # For manual testing.
        countdown = self.query_one(CountdownDisplay)
        countdown.seconds = 10

    def action_exit_app(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = PomodoroApp()
    app.run()
