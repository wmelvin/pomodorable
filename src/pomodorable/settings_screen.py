
from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Static

from pomodorable.app_data import AppConfig


class SettingInput(Static):

    def compose (self) -> ComposeResult:
        yield Horizontal(
            Label("setting"),
            Input(placeholder="setting"),
            Button("x", id="btn-clear"),
        )
        yield Label("(warnings)", id="warn")


class SettingsScreen(Screen):

    def __init__(self, app_config: AppConfig) -> None:
        self.app_config = app_config
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Horizontal(
            Button("Close", id="btn-close"),
            id="frm-buttons",
        )
        # TODO: Implement settings input.
        yield ScrollableContainer(
            SettingInput(id="setting-1"),
            SettingInput(id="setting-2"),
            SettingInput(id="setting-3"),
            SettingInput(id="setting-4"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "btn-close":
            self.app.pop_screen()
