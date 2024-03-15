import logging
from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.validation import Function, Integer
from textual.widgets import Button, Footer, Header, Input, Label, Static, Switch

from pomodorable.app_config import LOG_RETENTION_MIN, AppConfig


class SettingSwitch(Static):
    def __init__(self, *args, **kwargs) -> None:
        self.initial_value = None
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Label("setting", id="lbl-setting")
        yield Horizontal(
            Switch(id="swt-setting"),
            Button("undo", id="btn-undo"),
        )
        yield Label("(warnings)", id="lbl-warn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "btn-undo":
            event.stop()
            switch = self.query_one(Switch)
            switch.value = self.initial_value

    def check_data_changed(self):
        switch = self.query_one(Switch)
        btn = self.query_one(Button)
        if switch.value == self.initial_value:
            if btn.has_class("data-changed"):
                btn.remove_class("data-changed")
        elif not btn.has_class("data-changed"):
            btn.add_class("data-changed")

    @on(Switch.Changed)
    def show_validation_results(self) -> None:
        self.check_data_changed()

    def initialize(self, label: str, value: bool, validators: list) -> None:
        self.initial_value = value
        lbl = self.query_one("#lbl-setting")
        lbl.update(label)
        switch = self.query_one(Switch)
        switch.value = value
        if validators:
            switch.validators = validators

    def has_valid_changes(self) -> bool:
        switch = self.query_one(Switch)
        return switch.value != self.initial_value


class SettingInput(Static):
    def __init__(self, *args, **kwargs) -> None:
        self.initial_value = None
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Label("setting", id="lbl-setting")
        yield Horizontal(
            Input(placeholder="setting"),
            Button("undo", id="btn-undo"),
        )
        yield Label("(warnings)", id="lbl-warn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "btn-undo":
            event.stop()
            inp = self.query_one(Input)
            inp.clear()
            inp.insert_text_at_cursor(self.initial_value)

    def check_data_changed(self):
        inp = self.query_one(Input)
        btn = self.query_one(Button)
        if inp.value == self.initial_value:
            if btn.has_class("data-changed"):
                btn.remove_class("data-changed")
        elif not btn.has_class("data-changed"):
            btn.add_class("data-changed")

    @on(Input.Changed)
    def show_validation_results(self, event: Input.Changed) -> None:
        self.check_data_changed()

        #  If no validators are set then validation_result is None.
        if event.validation_result is None:
            return

        wrn = self.query_one("#lbl-warn")
        if event.validation_result.is_valid:
            wrn.remove_class("show-warnings")
        else:
            wrn.update(" ".join(event.validation_result.failure_descriptions))
            wrn.add_class("show-warnings")

    def initialize(self, label: str, value: str, validators: list) -> None:
        self.initial_value = value
        lbl = self.query_one("#lbl-setting")
        lbl.update(label)
        inp = self.query_one(Input)
        inp.insert_text_at_cursor(value)
        if validators:
            inp.validators = validators

    def has_valid_changes(self) -> bool:
        inp = self.query_one(Input)
        return inp.is_valid and inp.value != self.initial_value


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
        yield ScrollableContainer(
            SettingInput(id="set-minutes"),
            SettingInput(id="set-csv-dir"),
            SettingInput(id="set-md-dir"),
            SettingInput(id="set-md-heading"),
            SettingSwitch(id="set-md-append"),
            SettingInput(id="set-log-ret"),
        )

    def on_mount(self) -> None:
        set_minutes = self.query_one("#set-minutes")
        set_minutes.initialize(
            "Session Minutes",
            str(self.app_config.session_minutes),
            [
                Integer(
                    minimum=1,
                    failure_description="Must be a number greater than 1.",
                )
            ],
        )

        set_csv_dir = self.query_one("#set-csv-dir")
        set_csv_dir.initialize(
            "Daily CSV Folder",
            self.app_config.daily_csv_dir or "",
            [Function(is_valid_dir_or_empty, "Folder does not exist.")],
        )

        set_md_dir = self.query_one("#set-md-dir")
        set_md_dir.initialize(
            "Daily Markdown Folder",
            self.app_config.daily_md_dir or "",
            [Function(is_valid_dir_or_empty, "Folder does not exist.")],
        )

        set_md_heading = self.query_one("#set-md-heading")
        set_md_heading.initialize(
            "Daily Markdown Heading",
            self.app_config.daily_md_heading or "",
            [],
        )

        set_md_append = self.query_one("#set-md-append")
        set_md_append.initialize(
            "Daily Markdown Append-only (file is created by another application)",
            self.app_config.daily_md_append,
            [],
        )

        set_log_ret = self.query_one("#set-log-ret")
        set_log_ret.initialize(
            "Log Retention Days",
            str(self.app_config.log_retention_days),
            [
                Integer(
                    minimum=LOG_RETENTION_MIN,
                    failure_description="Must be a number greater than "
                    f"{LOG_RETENTION_MIN - 1}.",
                )
            ],
        )

    def save_changes(self) -> None:
        has_changes = False

        set_minutes = self.query_one("#set-minutes")
        if set_minutes.has_valid_changes():
            inp_minutes = set_minutes.query_one(Input)
            self.app_config.session_minutes = int(inp_minutes.value)
            has_changes = True

        set_csv_dir = self.query_one("#set-csv-dir")
        if set_csv_dir.has_valid_changes():
            inp_csv_dir = set_csv_dir.query_one(Input)
            self.app_config.daily_csv_dir = inp_csv_dir.value
            has_changes = True

        set_md_dir = self.query_one("#set-md-dir")
        if set_md_dir.has_valid_changes():
            inp_md_dir = set_md_dir.query_one(Input)
            self.app_config.daily_md_dir = inp_md_dir.value
            has_changes = True

        set_md_heading = self.query_one("#set-md-heading")
        if set_md_heading.has_valid_changes():
            inp_md_heading = set_md_heading.query_one(Input)
            self.app_config.daily_md_heading = inp_md_heading.value
            has_changes = True

        set_md_append = self.query_one("#set-md-append")
        if set_md_append.has_valid_changes():
            switch_md_append = set_md_append.query_one(Switch)
            self.app_config.daily_md_append = switch_md_append.value
            has_changes = True

        set_log_ret = self.query_one("#set-log-ret")
        if set_log_ret.has_valid_changes():
            inp_log_ret = set_log_ret.query_one(Input)
            self.app_config.log_retention_days = int(inp_log_ret.value)
            has_changes = True

        if has_changes:
            self.app_config.save()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "btn-close":
            self.save_changes()
            self.app.pop_screen()


def is_valid_dir_or_empty(path: str) -> bool:
    if not path:
        return True
    try:
        p = Path(path).expanduser().resolve()
        return p.exists() and p.is_dir()
    except Exception:
        logging.exception("Path validation failed")
        return False
