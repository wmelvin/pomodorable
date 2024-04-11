import logging
import webbrowser

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Static

from pomodorable.__about__ import __version__


class AboutScreen(ModalScreen[str]):
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="about-dialog"):
            yield Static("About", id="about-about")
            yield Static(self.app.title, id="about-title")
            yield Static(f"version {__version__}", id="about-version")
            with Horizontal(classes="about-buttons"):
                yield Button("GitHub", id="about-source")
            with VerticalScroll(id="about-scroll"):
                yield Static(
                    f"[b]Data path:[/b] {self.app.app_data.data_path}",
                    classes="about-info",
                )
                yield Static(
                    f"[b]Configuration:[/b] {self.app.app_data.config_file}",
                    classes="about-info",
                )
            with Horizontal(classes="about-buttons"):
                yield Button("Close", id="about-close")

    def on_mount(self) -> None:
        self.query_one("#about-close").focus()

    def open_browser(self) -> None:
        try:
            webbrowser.open("https://github.com/wmelvin/pomodorable#readme")
        except Exception:
            logging.exception("Failed to open web browser")
            self.query_one("#about-source").disabled = True

    def close_screen(self) -> None:
        self.dismiss(f"About: Version {__version__}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "about-source":
            self.open_browser()
        elif event.button.id == "about-close":
            self.close_screen()

    def action_cancel(self) -> None:
        self.close_screen()
