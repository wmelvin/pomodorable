from __future__ import annotations

import logging
from pathlib import Path

from textual import on
from textual.app import ComposeResult  # noqa: TCH002
from textual.containers import Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.validation import Function, Integer
from textual.widgets import Button, Header, Input, Label, Static, Switch

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

    def get_status(self) -> tuple[bool, bool, bool]:
        """Return a tuple of (changed, is_valid, value).
        The Switch widget does not have validation, so is_valid is always True.
        """
        switch = self.query_one(Switch)
        changed = switch.value != self.initial_value
        return (changed, True, switch.value)


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

    def get_status(self) -> tuple[bool, bool, str]:
        """Return a tuple of (changed, is_valid, value)."""
        inp = self.query_one(Input)
        changed = inp.value != self.initial_value
        return (changed, inp.is_valid, inp.value)


class SettingsScreen(Screen[str]):
    def __init__(self, app_config: AppConfig) -> None:
        self.app_config = app_config
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            SettingInput(id="set-minutes"),
            SettingInput(id="set-csv-dir"),
            SettingInput(id="set-md-dir"),
            SettingInput(id="set-md-heading"),
            SettingSwitch(id="set-md-append"),
            SettingInput(id="set-log-ret"),
        )
        yield Horizontal(
            Button("Close", id="btn-close"),
            id="frm-buttons",
        )

    def on_mount(self) -> None:
        self.title = "Settings"
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

    def save_changes(self) -> tuple[bool, bool]:
        """Return a tuple of (has_changes, has_errors).

        has_changes is True if any settings were changed.

        If has_changes is False, then no data was written to file.

        has_errors is True if any settings have validation errors.

        Changed settings without validation errors are saved even
        if other settings have errors.
        """
        has_changes = False
        has_errors = False

        changed, is_valid, value = self.query_one("#set-minutes").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.session_minutes = int(value)
            has_changes = True

        changed, is_valid, value = self.query_one("#set-csv-dir").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.daily_csv_dir = value
            has_changes = True

        changed, is_valid, value = self.query_one("#set-md-dir").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.daily_md_dir = value
            has_changes = True

        changed, is_valid, value = self.query_one("#set-md-heading").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.daily_md_heading = value
            has_changes = True

        changed, is_valid, value = self.query_one("#set-md-append").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.daily_md_append = value
            has_changes = True

        changed, is_valid, value = self.query_one("#set-log-ret").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.log_retention_days = int(value)
            has_changes = True

        if has_changes:
            self.app_config.save()

        return (has_changes, has_errors)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "btn-close":
            has_changes, has_errors = self.save_changes()
            if has_changes:
                msg = "Saved changes."
                if has_errors:
                    msg += " Settings with validation errors not saved."
            else:
                msg = "No settings changed."
            self.dismiss(msg)


def is_valid_dir_or_empty(path: str) -> bool:
    if not path:
        return True
    try:
        p = Path(path).expanduser().resolve()
        return p.exists() and p.is_dir()
    except Exception:
        logging.exception("Path validation failed")
        return False
