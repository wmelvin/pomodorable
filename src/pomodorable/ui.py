from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input, Label, Log, Static

APP_NAME = "Pomodorable"

DEFAULT_SESSION_SECONDS = 25 * 60  # TODO: settings.default_session_minutes


class CountdownDisplay(Static):
    """[00:]00:00 ([hours:]minutes:seconds)"""

    seconds = reactive(DEFAULT_SESSION_SECONDS)

    def add_minutes(self, minutes: int) -> None:
        self.seconds += minutes * 60
        if self.seconds < 0:
            self.seconds = 0

    def reset_countdown(self) -> None:
        self.seconds = DEFAULT_SESSION_SECONDS

    def watch_seconds(self, seconds: datetime) -> None:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            self.update(f"{hours:02}:{minutes:02}:{seconds:02}")
        else:
            self.update(f"{minutes:02}:{seconds:02}")


class TimeDisplay(Static):
    """00:00:00 (hours:minutes:seconds)"""

    time = reactive(datetime.now())

    def on_mount(self) -> None:
        self.set_interval(1 / 5, self.update_time)

    def update_time(self) -> None:
        self.time = datetime.now()

    def watch_time(self, time: datetime) -> None:
        self.update(f"{time.strftime('%H:%M:%S')}")


class PomodoroApp(App):
    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("x", "exit_app", "Exit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            Label("Countdown:"),
            CountdownDisplay("25:00", id="countdown"),
            Label("Started:"),
            TimeDisplay("14:05:00", id="time-started"),
            Label("Ending:"),
            TimeDisplay("14:30:00", id="time-ending"),
            id="frm-times",
        )
        yield Horizontal(
            Button("Reset", id="btn-reset"),  # To default session length (not 00:00).
            Button("+ 5 min", id="btn-plus-five"),
            Button("- 5 min", id="btn-minus-five"),
            id="set-time",
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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        log = self.query_one(Log)
        log.write_line(f"You pressed [{btn}].")
        if btn == "btn-plus-five":
            disp = self.query_one(CountdownDisplay)
            disp.add_minutes(5)
        if btn == "btn-minus-five":
            disp = self.query_one(CountdownDisplay)
            disp.add_minutes(-5)

    def action_exit_app(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = PomodoroApp()
    app.run()
