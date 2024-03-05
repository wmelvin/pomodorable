
from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label

from pomodorable.app_data import AppConfig


class SettingsScreen(Screen):

    def __init__(self, app_config: AppConfig) -> None:
        self.app_config = app_config
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Horizontal(
            Button("Close", id="btn-close"),
        )
        # TODO: Implement settings input.
        yield ScrollableContainer(
            Horizontal(
                Label("setting1"),
                Input(placeholder="setting1"),
                Button("x", id="btn-clr-1"),
            ),
            Horizontal(
                Label("setting2"),
                Input(placeholder="setting2"),
                Button("x", id="btn-clr-2"),
            ),
            Horizontal(
                Label("setting3"),
                Input(placeholder="setting3"),
                Button("x", id="btn-clr-3"),
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "btn-close":
            self.app.pop_screen()
