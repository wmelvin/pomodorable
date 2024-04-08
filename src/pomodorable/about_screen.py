from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static

from pomodorable.__about__ import __version__


class AboutScreen(ModalScreen[str]):
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("About", id="about-about"),
            Static(self.app.title, id="about-title"),
            Static(f"Version {__version__}", id="about-version"),
            Static(f"Data path: {self.app.app_data.data_path}", classes="about-info"),
            Static(
                f"Configuration: {self.app.app_data.config_file}", classes="about-info"
            ),
            Horizontal(Button("Close", id="about-close"), id="about-buttons"),
            id="about-dialog",
        )

    def close_screen(self) -> None:
        self.dismiss(f"About: Version {__version__}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "about-close":
            self.close_screen()

    def action_cancel(self) -> None:
        self.close_screen()
