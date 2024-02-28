
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static

class PomodoroApp(App):
    
    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("x", "exit_app", "Exit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Static("More widgets will go here.")
        yield Footer()

    def action_exit_app(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = PomodoroApp()
    app.run()
