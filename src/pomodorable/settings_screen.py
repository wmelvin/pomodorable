from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from textual import on
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.validation import Function, Integer
from textual.widgets import Button, Header, Input, Label, SelectionList, Static, Switch

from pomodorable.app_config import LOG_RETENTION_MIN, AppConfig

if TYPE_CHECKING:
    from textual.app import ComposeResult


class SettingOutputFilter(Static):
    def __init__(self, *args, **kwargs) -> None:
        self.initial_value = None
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Label("(setting)", id="lbl-setting")
        with Horizontal(id="sel-list"):
            yield SelectionList[str]()
            yield Button("undo", id="btn-undo")
        yield Label("(warnings)", id="lbl-warn")

    def on_mount(self) -> None:
        self.query_one(SelectionList).border_title = "Select actions to exclude:"

    def _set_options(self, value: str) -> None:
        flags = value.upper()
        items = [
            ("Finish", "F", "F" in flags),
            ("Pause (all)", "P", "P" in flags),
            ("Pause (w/o Reason)", "R", "R" in flags),
            ("Stop", "X", "X" in flags),
        ]
        sel = self.query_one(SelectionList)
        sel.clear_options()
        sel.add_options(items)

    def _selections_value(self) -> str:
        sel = self.query_one(SelectionList)
        return "".join(sorted(sel.selected))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "btn-undo":
            event.stop()
            self._set_options(self.initial_value)

    def check_data_changed(self):
        btn = self.query_one(Button)
        if self._selections_value() == self.initial_value:
            if btn.has_class("data-changed"):
                btn.remove_class("data-changed")
        elif not btn.has_class("data-changed"):
            btn.add_class("data-changed")

    @on(SelectionList.SelectedChanged)
    def show_validation_results(self) -> None:
        self.check_data_changed()

    def initialize(self, label: str, value: str, validators: list) -> None:
        self.initial_value = value
        self.query_one("#lbl-setting").update(label)
        sel = self.query_one(SelectionList)
        self._set_options(value)
        if validators:
            sel.validators = validators

    def get_status(self) -> tuple[bool, bool, bool]:
        """Return a tuple of (changed, is_valid, value).
        The Switch widget does not have validation, so is_valid is always True.
        """
        str_val = self._selections_value()
        changed = str_val != self.initial_value
        return (changed, True, str_val)


class SettingSwitch(Static):
    def __init__(self, *args, **kwargs) -> None:
        self.initial_value = None
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Label("(setting)", id="lbl-setting")
        yield Horizontal(
            Switch(id="swt-setting"),
            Button("undo", id="btn-undo"),
        )
        yield Label("(warnings)", id="lbl-warn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id
        if btn == "btn-undo":
            event.stop()
            self.query_one(Switch).value = self.initial_value

    def check_data_changed(self):
        btn = self.query_one(Button)
        if self.query_one(Switch).value == self.initial_value:
            if btn.has_class("data-changed"):
                btn.remove_class("data-changed")
        elif not btn.has_class("data-changed"):
            btn.add_class("data-changed")

    @on(Switch.Changed)
    def show_validation_results(self) -> None:
        self.check_data_changed()

    def initialize(self, label: str, value: bool, validators: list) -> None:
        self.initial_value = value
        self.query_one("#lbl-setting").update(label)
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
        yield Label("(setting)", id="lbl-setting")
        yield Horizontal(
            Input(placeholder="(empty - enter setting here)"),
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
        btn = self.query_one(Button)
        if self.query_one(Input).value == self.initial_value:
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
        self.query_one("#lbl-setting").update(label)
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

    BINDINGS = [
        Binding("ctrl+s", "screenshot", "Screenshot", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(
            SettingInput(id="set-minutes"),
            SettingSwitch(id="set-notify"),
            SettingInput(id="set-wavfile"),
            SettingInput(id="set-csv-dir-run"),
            SettingInput(id="set-csv-name-run"),
            SettingInput(id="set-csv-dir-daily"),
            SettingOutputFilter(id="set-filter-csv", classes="set-filter"),
            SettingInput(id="set-md-dir"),
            SettingInput(id="set-md-heading"),
            SettingSwitch(id="set-md-append"),
            SettingOutputFilter(id="set-filter-md", classes="set-filter"),
            SettingInput(id="set-log-ret"),
        )
        yield Horizontal(
            Button("Close", id="btn-close"),
            id="frm-buttons",
        )

    def on_mount(self) -> None:
        self.title = "Settings"
        self.query_one("#set-minutes").initialize(
            "Session Minutes",
            str(self.app_config.session_minutes),
            [
                Integer(
                    minimum=1,
                    failure_description="Must be a number greater than 1.",
                )
            ],
        )

        self.query_one("#set-notify").initialize(
            "Do system notification at end of session",
            self.app_config.do_notify,
            [],
        )

        self.query_one("#set-wavfile").initialize(
            "Play sound file (.wav) at end of session. Optional.",
            self.app_config.wav_file or "",
            [Function(is_valid_file_or_empty, "File does not exist.")],
        )

        self.query_one("#set-csv-dir-run").initialize(
            "Running (milti-day) CSV Folder. Leave empty to disable.",
            self.app_config.running_csv_dir or "",
            [Function(is_valid_dir_or_empty, "Folder does not exist.")],
        )

        self.query_one("#set-csv-name-run").initialize(
            "Running CSV File Name",
            self.app_config.running_csv_name or "",
            [],
        )

        self.query_one("#set-csv-dir-daily").initialize(
            "Daily CSV Folder. Leave empty to disable.",
            self.app_config.daily_csv_dir or "",
            [Function(is_valid_dir_or_empty, "Folder does not exist.")],
        )

        self.query_one("#set-filter-csv").initialize(
            "Filter CSV output",
            self.app_config.filter_csv or "",
            [],
        )

        self.query_one("#set-md-dir").initialize(
            "Daily Markdown Folder. Leave empty to disable.",
            self.app_config.daily_md_dir or "",
            [Function(is_valid_dir_or_empty, "Folder does not exist.")],
        )

        self.query_one("#set-md-heading").initialize(
            "Daily Markdown Heading",
            self.app_config.daily_md_heading or "",
            [],
        )

        self.query_one("#set-md-append").initialize(
            "Daily Markdown Append-only (file is created by another application)",
            self.app_config.daily_md_append,
            [],
        )

        self.query_one("#set-filter-md").initialize(
            "Filter Markdown output",
            self.app_config.filter_md or "",
            [],
        )

        self.query_one("#set-log-ret").initialize(
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

        changed, is_valid, value = self.query_one("#set-notify").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.do_notify = value
            has_changes = True

        changed, is_valid, value = self.query_one("#set-wavfile").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.wav_file = value
            has_changes = True

        changed, is_valid, value = self.query_one("#set-csv-dir-run").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.running_csv_dir = value
            has_changes = True

        changed, is_valid, value = self.query_one("#set-csv-name-run").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.running_csv_name = value
            has_changes = True

        changed, is_valid, value = self.query_one("#set-csv-dir-daily").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.daily_csv_dir = value
            has_changes = True

        changed, is_valid, value = self.query_one("#set-filter-csv").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.filter_csv = value
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

        changed, is_valid, value = self.query_one("#set-filter-md").get_status()
        if not is_valid:
            has_errors = True
        elif changed:
            self.app_config.filter_md = value
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

    def action_screenshot(self) -> None:
        self.app.take_screenshot()


def is_valid_dir_or_empty(path: str) -> bool:
    if not path:
        return True
    try:
        p = Path(path).expanduser().resolve()
        return p.exists() and p.is_dir()
    except Exception:
        logging.exception("Path validation failed")
        return False


def is_valid_file_or_empty(path: str) -> bool:
    if not path:
        return True
    try:
        p = Path(path).expanduser().resolve()
        return p.exists() and p.is_file()
    except Exception:
        logging.exception("Filename validation failed")
        return False
