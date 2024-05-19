from __future__ import annotations

from typing import TYPE_CHECKING

from textual.binding import Binding
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Select

if TYPE_CHECKING:
    from textual.app import ComposeResult


class MRUScreen(ModalScreen[str]):
    def __init__(self, mru_list: list[str]) -> None:
        self.mru_list = mru_list
        super().__init__()

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        Binding("ctrl+s", "screenshot", "Screenshot", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Select from recent inputs:"),
            Select.from_values(self.mru_list),
            Button("Back", id="btn-back"),
            id="dialog",
        )

    def close_screen(self) -> None:
        s: Select = self.query_one(Select)
        if s.is_blank():
            self.dismiss("")
        else:
            self.dismiss(s.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.close_screen()

    def action_screenshot(self) -> None:
        self.app.take_screenshot()

    def action_cancel(self) -> None:
        self.dismiss("")
