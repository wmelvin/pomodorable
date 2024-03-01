from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Footer, Header, Input, Label, Log, Static

APP_NAME = "Pomodorable"


class CountdownDisplay(Static):
    """00:00 (minutes:seconds)"""


class TimeDisplay(Static):
    """00:00:00 (hours:minutes:seconds)"""


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
            id="set-time"
        )
        yield Horizontal(
            Button("Start", id="btn-start"), Input(id="input-task", placeholder="(task description)"), id="frm-start"
        )
        yield Horizontal(Button("Pause", id="btn-pause"), Input(id="input-reason", placeholder="(reason)"), id="frm-pause")
        yield Horizontal(
            Button("Resume", id="btn-resume"), Button("Extend", id="btn-extend"), Button("Stop", id="btn-stop"), id="frm-paused"
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

    def action_exit_app(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = PomodoroApp()
    app.run()
