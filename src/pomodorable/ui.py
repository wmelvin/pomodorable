from __future__ import annotations

import logging
from datetime import datetime, timedelta

from plyer import notification
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    RichLog,
    Static,
)

from pomodorable.about_screen import AboutScreen
from pomodorable.app_data import AppData, sec_to_hms
from pomodorable.app_utils import q_text
from pomodorable.mru_screen import MRUScreen
from pomodorable.settings_screen import SettingsScreen
from pomodorable.timerbar import TimerBar

APP_NAME = "Pomodorable"

ONE_MINUTE = 60
FIVE_MINUTES = 5 * ONE_MINUTE
DEFAULT_SESSION_SECONDS = 25 * ONE_MINUTE

UPDATE_INTERVAL = 1 / 3  # Update three times per second.


class CountdownDisplay(Static):
    """[00:]00:00 ([hours:]minutes:seconds)"""

    seconds = reactive(DEFAULT_SESSION_SECONDS)
    start_seconds: int = DEFAULT_SESSION_SECONDS
    start_time: datetime | None = None
    pause_time: datetime | None = None
    seconds_added: int = 0
    last_minute: int = 0

    def on_mount(self) -> None:
        secs = self.app.app_data.config.session_seconds
        self.seconds = secs
        self.start_seconds = secs
        self.update_timer = self.set_interval(UPDATE_INTERVAL, self.update_countdown)

    def update_countdown(self) -> None:
        if self.app.has_class("paused"):
            self.seconds = (
                self.start_seconds - (self.pause_time - self.start_time).seconds
            )
        elif self.app.has_class("running"):
            self.seconds = (
                self.start_seconds - (datetime.now() - self.start_time).seconds
            )
        self.seconds += self.seconds_added

    def watch_seconds(self, seconds: datetime) -> None:
        self.update(sec_to_hms(seconds))

        # Update the TimerBar when the minute changes.
        minute = int(self.seconds / 60)
        if minute != self.last_minute:
            self.app.query_one(TimerBar).update_bar(minute)
            self.last_minute = minute

        # Finish the session when running and no seconds remain.
        if (
            self.seconds <= 0
            and self.app.has_class("running")
            and not self.app.has_class("paused")
        ):
            self.update_timer.pause()
            self.app.countdown_finished()
            self.update_timer.resume()

    def seconds_up(self, secs_up: int) -> None:
        if self.seconds < secs_up:
            self.seconds = secs_up
        else:
            self.seconds += secs_up

    def seconds_down(self, secs_down: int) -> None:
        if self.seconds < (secs_down + ONE_MINUTE):
            return
        self.seconds -= secs_down

    def reset(self) -> None:
        self.update_timer.pause()
        self.seconds = self.app.app_data.config.session_seconds
        self.start_time = None
        self.pause_time = None
        self.seconds_added = 0
        self.update_timer.resume()

    def set_start_time(self) -> None:
        self.start_time = datetime.now()
        self.start_seconds = self.seconds
        self.app.app_data.write_start(
            self.start_time,
            self.app.query_one("#input-task").value,
            self.seconds,
        )

    def pause(self) -> None:
        self.pause_time = datetime.now()

    def resume(self) -> None:
        duration = (datetime.now() - self.pause_time).seconds
        self.app.app_data.write_pause(
            self.pause_time,
            self.app.query_one("#input-reason").value,
            duration,
            False,
        )
        self.pause_time = None

    def extend(self) -> None:
        if self.pause_time:
            extend_secs = (datetime.now() - self.pause_time).seconds
            self.seconds_added += extend_secs
            self.app.app_data.write_pause(
                self.pause_time,
                self.app.query_one("#input-reason").value,
                extend_secs,
                True,
            )
        self.pause_time = None


class TimeDisplay(Static):
    """00:00:00 (hours:minutes:seconds)"""

    time = reactive(datetime.now())
    add_seconds: int = 0

    def on_mount(self) -> None:
        self.set_interval(UPDATE_INTERVAL, self.update_time)

    def sync_time(self, add_seconds: int) -> None:
        self.add_seconds = add_seconds
        self.time = datetime.now() + timedelta(seconds=self.add_seconds)

    def update_time(self) -> None:
        #  While the countdown is not running, show the current time plus any
        #  added seconds.
        if not self.app.has_class("running"):
            self.time = datetime.now() + timedelta(seconds=self.add_seconds)

    def watch_time(self, time: datetime) -> None:
        self.update(f"{time.strftime('%H:%M:%S')}")


class PomodorableApp(App):
    def __init__(self, init_app_data: AppData = None) -> None:
        if init_app_data:
            self.app_data = init_app_data
        else:
            self.app_data = AppData()
        super().__init__()

    ENABLE_COMMAND_PALETTE = False
    # See: https://textual.textualize.io/guide/command_palette/

    CSS_PATH = "app.tcss"

    BINDINGS = [
        # ("d", "toggle_dark", "Toggle dark mode"),
        ("down", "select_input", "Recent inputs"),
        ("ctrl+q", "exit_app", "Quit"),
        # ("ctrl+t", "manual_testing", "Testing"),
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
            Button("+5", id="btn-plus-five", classes="updn"),
            Button("+1", id="btn-plus-one", classes="updn"),
            Button("-1", id="btn-minus-one", classes="updn"),
            Button("-5", id="btn-minus-five", classes="updn"),
            Button("?", id="btn-about"),
            Button("Settings...", id="btn-settings"),
            id="frm-set",
        )
        yield Horizontal(
            Input(id="input-task", placeholder="(task description)"),
            Button("Start", id="btn-start"),
            id="frm-start",
        )
        yield Horizontal(
            Button("Pause", id="btn-pause"),
            Input(id="input-reason", placeholder="(reason)"),
            id="frm-pause",
        )
        yield Horizontal(
            Button("Extend", id="btn-extend"),
            Button("Resume", id="btn-resume"),
            Button("Stop", id="btn-stop"),
            id="frm-paused",
        )
        yield TimerBar()
        yield RichLog(id="log", markup=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = APP_NAME
        self.sub_title = ""
        log = self.query_one(RichLog)
        log.write("Hello.")
        time_disp = self.query_one("#time-ending")
        time_disp.sync_time(self.app_data.config.session_seconds)
        self.query_one("#input-task").focus()

    def say(self, message: str, console_text: str = "") -> None:
        log = self.query_one(RichLog)
        msg = message if console_text == "" else console_text
        log.write(f"{datetime.now().strftime('%H:%M:%S')} - {msg}")
        logging.info(message)

    def show_queued_errors(self) -> None:
        errs = self.app_data.retrieve_error_list()
        for err in errs:
            self.say(err, console_text=f"[bold italic]{err}")

    def update_widgets_enabled(self) -> None:
        paused = self.has_class("paused")
        running = self.has_class("running")
        self.query_one("#btn-start").disabled = running
        self.query_one("#btn-pause").disabled = not running
        self.query_one("#btn-resume").disabled = not paused
        self.query_one("#btn-extend").disabled = not paused
        self.query_one("#btn-stop").disabled = not paused
        self.query_one("#input-task").disabled = running
        self.query_one("#input-reason").disabled = not paused
        self.query_one("#btn-settings").disabled = running
        self.query_one("#btn-about").disabled = running
        self.query_one("#btn-reset").disabled = running
        self.query_one("#btn-plus-five").disabled = running
        self.query_one("#btn-plus-one").disabled = running
        self.query_one("#btn-minus-one").disabled = running
        self.query_one("#btn-minus-five").disabled = running

    def on_button_pressed(self, event: Button.Pressed) -> None:
        try:
            countdown = self.query_one(CountdownDisplay)
            time_ending = self.query_one("#time-ending")
        except NoMatches:
            logging.exception("Exception in app.on_button_pressed()")
            return

        btn = event.button.id
        if btn == "btn-reset":
            self.say("Reset")
            countdown.reset()

        elif btn == "btn-plus-five":
            self.say("Add 5 minutes")
            countdown.seconds_up(FIVE_MINUTES)
            time_ending.sync_time(countdown.seconds)

        elif btn == "btn-plus-one":
            self.say("Add 1 minute")
            countdown.seconds_up(ONE_MINUTE)
            time_ending.sync_time(countdown.seconds)

        elif btn == "btn-minus-one":
            self.say("Subtract 1 minute")
            countdown.seconds_down(ONE_MINUTE)
            time_ending.sync_time(countdown.seconds)

        elif btn == "btn-minus-five":
            self.say("Subtract 5 minutes")
            countdown.seconds_down(FIVE_MINUTES)
            time_ending.sync_time(countdown.seconds)

        elif btn == "btn-start":
            task = self.query_one("#input-task").value
            self.say(f"Start{q_text(task)}")
            countdown.set_start_time()
            self.add_class("running")
            time_ending.sync_time(countdown.seconds)
            self.update_widgets_enabled()
            self.query_one("#btn-pause").focus()

        elif btn == "btn-pause":
            self.say("Pause...")
            if not self.has_class("paused"):
                countdown.pause()
                self.add_class("paused")
                self.update_widgets_enabled()
                self.query_one("#input-reason").focus()

        elif btn == "btn-resume":
            reason = self.query_one("#input-reason").value
            self.say(f"Resume{q_text(reason)}")
            countdown.resume()
            self.remove_class("paused")
            self.update_widgets_enabled()
            self.query_one("#btn-pause").focus()

        elif btn == "btn-extend":
            reason = self.query_one("#input-reason").value
            self.say(f"Extend{q_text(reason)}")
            countdown.extend()
            time_ending.sync_time(countdown.seconds)
            self.remove_class("paused")
            self.update_widgets_enabled()
            self.query_one("#btn-pause").focus()

        elif btn == "btn-stop":
            reason = self.query_one("#input-reason").value
            self.say(f"STOP '{reason}'", console_text=f"[bold]STOP{q_text(reason)}")
            self.app_data.write_stop(
                datetime.now(), self.query_one("#input-reason").value
            )
            self.remove_class("paused")
            self.remove_class("running")
            countdown.reset()
            time_ending.sync_time(countdown.seconds)
            self.show_queued_errors()
            self.update_widgets_enabled()
            self.query_one("#input-task").focus()

        elif btn == "btn-about":
            if not self.has_class("running"):
                countdown.update_timer.pause()
                self.push_screen(
                    AboutScreen(),
                    self.about_closed,
                )

        elif btn == "btn-settings":
            if not self.has_class("running"):
                countdown.update_timer.pause()
                self.push_screen(
                    SettingsScreen(app_config=self.app_data.config),
                    self.settings_closed,
                )

    def about_closed(self, msg: str) -> None:
        # The about dialog returns the app version.
        self.say(msg)
        self.query_one(CountdownDisplay).update_timer.resume()

    def settings_closed(self, msg: str) -> None:
        self.say(msg)
        self.query_one(CountdownDisplay).update_timer.resume()

    def countdown_finished(self):
        self.say("Finished", console_text="[bold]Finished")
        if self.has_class("running"):
            countdown = self.query_one(CountdownDisplay)
            self.app_data.write_finish(datetime.now(), countdown.start_time)
            time_ending = self.query_one("#time-ending")
            self.remove_class("paused")
            self.remove_class("running")
            self.update_widgets_enabled()
            countdown.reset()
            time_ending.sync_time(countdown.seconds)

            # TODO: Configure notification - enable/disable, timeout, etc.
            # If there is no timeout will notification stay on screen until
            # dismissed?

            #  Show plyer.notification.
            try:
                notification.notify(
                    title=APP_NAME,
                    message=f"{APP_NAME}:  Session finished.",
                    app_name=APP_NAME,
                    timeout=15,
                )
            except Exception as e:
                logging.exception("Exception in notification")
                self.say(f"Notification error: {e}")

            self.show_queued_errors()
            self.query_one("#input-task").focus()

    def action_manual_testing(self) -> None:
        # Short countdown to observe Finish.
        countdown = self.query_one(CountdownDisplay)
        countdown.seconds = 7
        # # Fake error messages in app_data.
        # for i in range(3):
        #     self.app_data.queue_error(f"Fake error {i + 1}")

    def action_select_input(self) -> None:
        """Open the MRUScreen for the focused input field."""
        if self.focused.id not in ["input-task", "input-reason"]:
            return
        mru = None
        if self.has_class("paused"):
            mru = self.app_data.mru_list.get_reasons()
        elif not self.has_class("running"):
            mru = self.app_data.mru_list.get_tasks()
        if mru:
            countdown = self.query_one(CountdownDisplay)
            countdown.update_timer.pause()
            self.push_screen(
                MRUScreen(mru),
                self.mru_closed,
            )

    def mru_closed(self, text: str) -> None:
        if text:
            if self.has_class("paused"):
                inp: Input = self.query_one("#input-reason")
            else:
                inp: Input = self.query_one("#input-task")
            inp.clear()
            inp.insert_text_at_cursor(text)
        self.query_one(CountdownDisplay).update_timer.resume()

    def action_exit_app(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = PomodorableApp()
    app.run()
