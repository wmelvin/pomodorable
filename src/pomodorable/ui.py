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
    Log,
    Static,
)

from pomodorable.app_data import AppData, sec_to_hms
from pomodorable.settings_screen import SettingsScreen
from pomodorable.timerbar import TimerBar

APP_NAME = "Pomodorable"

ONE_MINUTE = 60
FIVE_MINUTES = 5 * ONE_MINUTE
DEFAULT_SESSION_SECONDS = 25 * ONE_MINUTE

UPDATE_INTERVAL = 1 / 4  # Update four times per second.


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
        self.set_interval(UPDATE_INTERVAL, self.update_countdown)

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

        # Update the TimerBar when the minute changes.
        minute = int(self.seconds / 60)
        if minute != self.last_minute:
            self.app.query_one(TimerBar).update_bar(minute)
            self.last_minute = minute

        if (
            self.seconds <= 0
            and self.app.has_class("running")
            and not self.app.has_class("paused")
        ):
            self.app.app_data.write_finish(datetime.now(), self.start_time)
            self.app.countdown_finished()

    def watch_seconds(self, seconds: datetime) -> None:
        self.update(sec_to_hms(seconds))

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
        self.seconds = self.app.app_data.config.session_seconds
        self.start_time = None
        self.pause_time = None
        self.seconds_added = 0

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
    # TODO: Explore this https://textual.textualize.io/guide/command_palette/

    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("ctrl+x", "exit_app", "Exit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        # ("t", "ten_seconds", "Ten"),
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
            Button("-5", id="btn-minus-five", classes="updn"),
            Button("+1", id="btn-plus-one", classes="updn"),
            Button("-1", id="btn-minus-one", classes="updn"),
            Button("Settings...", id="btn-settings"),
            id="frm-set",
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
            Button("Extend", id="btn-extend"),
            Button("Resume", id="btn-resume"),
            Button("Stop", id="btn-stop"),
            id="frm-paused",
        )
        yield TimerBar()
        yield Log(id="log")
        yield Footer()

    def on_mount(self) -> None:
        self.title = APP_NAME
        self.sub_title = ""
        log = self.query_one(Log)
        log.write_line("Hello.")
        time_disp = self.query_one("#time-ending")
        time_disp.sync_time(self.app_data.config.session_seconds)

    def say(self, message: str) -> None:
        log = self.query_one(Log)
        log.write_line(f"{datetime.now().strftime('%H:%M:%S')} - {message}")
        logging.info(message)

    def show_queued_errors(self) -> None:
        errs = self.app_data.retrieve_error_list()
        for err in errs:
            self.say(err)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        try:
            countdown = self.query_one(CountdownDisplay)
            time_ending = self.query_one("#time-ending")
        except NoMatches:
            logging.exception("Exception in app.on_button_pressed()")
            return

        btn = event.button.id
        if btn == "btn-reset":
            self.say("Reset.")
            countdown.reset()

        elif btn == "btn-plus-five":
            self.say("Add 5 minutes.")
            countdown.seconds_up(FIVE_MINUTES)
            time_ending.sync_time(countdown.seconds)

        elif btn == "btn-plus-one":
            self.say("Add 1 minute.")
            countdown.seconds_up(ONE_MINUTE)
            time_ending.sync_time(countdown.seconds)

        elif btn == "btn-minus-one":
            self.say("Subtract 1 minute.")
            countdown.seconds_down(ONE_MINUTE)
            time_ending.sync_time(countdown.seconds)

        elif btn == "btn-minus-five":
            self.say("Subtract 5 minutes.")
            countdown.seconds_down(FIVE_MINUTES)
            time_ending.sync_time(countdown.seconds)

        elif btn == "btn-start":
            self.say("Start.")
            countdown.set_start_time()
            self.add_class("running")
            time_ending.sync_time(countdown.seconds)

        elif btn == "btn-pause":
            self.say("Pause.")
            if not self.has_class("paused"):
                countdown.pause()
                self.add_class("paused")

        elif btn == "btn-resume":
            self.say("Resume.")
            countdown.resume()
            self.remove_class("paused")

        elif btn == "btn-extend":
            self.say("Extend.")
            countdown.extend()
            time_ending.sync_time(countdown.seconds)
            self.remove_class("paused")

        elif btn == "btn-stop":
            self.say("Stop.")
            self.app_data.write_stop(
                datetime.now(), self.query_one("#input-reason").value
            )
            self.remove_class("paused")
            self.remove_class("running")
            countdown.reset()
            time_ending.sync_time(countdown.seconds)
            self.show_queued_errors()

        elif btn == "btn-settings":
            if not self.has_class("running"):
                self.push_screen(SettingsScreen(app_config=self.app_data.config))

    def countdown_finished(self):
        self.say("Finished.")
        if self.has_class("running"):
            countdown = self.query_one(CountdownDisplay)
            time_ending = self.query_one("#time-ending")
            self.remove_class("paused")
            self.remove_class("running")
            countdown.reset()
            time_ending.sync_time(countdown.seconds)

            #  Show plyer.notification.
            notification.notify(
                title=APP_NAME,
                message=f"{APP_NAME}:  Session finished.",
                app_name=APP_NAME,
                timeout=12,
            )
            # TODO: Configure notification - enable/disable, timeout, etc.
            # If there is no timeout will notification stay on screen until
            # dismissed?

            self.show_queued_errors()

    # def action_ten_seconds(self) -> None:
    #     # For manual testing.
    #     countdown = self.query_one(CountdownDisplay)
    #     countdown.seconds = 10

    def action_exit_app(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = PomodorableApp()
    app.run()
