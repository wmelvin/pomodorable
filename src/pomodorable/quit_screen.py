"""QuitScreen class for the Pomodorable application."""

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class QuitScreen(ModalScreen):
    """A modal screen dialog that confirms quitting the application."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Quit now?", id="question"),
            Button("Cancel", variant="primary", id="cancel"),
            Button("Quit", variant="error", id="quit"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()
