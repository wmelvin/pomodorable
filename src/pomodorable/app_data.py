from __future__ import annotations

import csv
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import dotenv
from platformdirs import user_config_path, user_data_path

from pomodorable.app_config import LOG_RETENTION_MIN, AppConfig
from pomodorable.app_utils import get_date_from_str, sec_to_hms
from pomodorable.mru_list import MRUList
from pomodorable.output_csv import write_to_daily_csv
from pomodorable.output_md import write_to_daily_md

APP_NAME = "pomodorable"
APP_CONFIG_FILE = f"{APP_NAME}-config.toml"
APP_OUTPUT_CSV = f"{APP_NAME}-data.csv"
APP_DATA_VERSION = "1"


@dataclass
class AppDataRow:
    version: str = APP_DATA_VERSION
    date_time: datetime = None
    time: str = ""
    action: str = ""
    message: str = ""
    duration: str = ""
    notes: str = ""


class AppData:
    def __init__(
        self,
        init_app_config: AppConfig | None = None,
        init_data_path: Path | None = None,
    ) -> None:
        self._errors = []
        self.data_path = init_data_path

        if not self.data_path:
            #  If init_data_path is not set, check environment variables for
            #  values to use as the data path.
            #  POMODORABLE_TEST_DATA_DIR is used by the test suite. It takes
            #  precedence over POMODORABLE_DEV_OUTPUT_DIR which is used for
            #  development and manual testing.
            dotenv.load_dotenv()
            dev_output_dir = os.environ.get("POMODORABLE_TEST_DATA_DIR")
            if not dev_output_dir:
                dev_output_dir = os.environ.get("POMODORABLE_DEV_OUTPUT_DIR")
            if dev_output_dir:
                self.data_path = Path(dev_output_dir).expanduser().resolve()
                if not self.data_path.exists():
                    sys.stderr.write(f"\nDirectory does not exist: {self.data_path}\n")
                    sys.exit(1)

        if self.data_path:
            self.config_file = self.data_path / APP_CONFIG_FILE
        else:
            self.config_file = (
                user_config_path(APP_NAME, appauthor=False, ensure_exists=True)
                / APP_CONFIG_FILE
            )
            self.data_path = user_data_path(
                APP_NAME, appauthor=False, ensure_exists=True
            )

        self.output_csv = self.data_path / APP_OUTPUT_CSV

        self._log_handler = None
        self._log_formatter = None
        log_name = f"{APP_NAME}-{datetime.now().strftime('%Y%m%d')}.log"
        self.log_file = self.data_path / log_name
        self._init_logging()

        if init_app_config:
            self.config = init_app_config
        else:
            self.config = AppConfig(self.config_file)
            self.config.load()

        self._purge_log_files()

        self.mru_list = MRUList(self.data_path)
        self.mru_list.load()

    def _init_logging(self) -> None:
        """Add a file handler to the root logger. Do this before loading
        configuration so any errors in that process are logged.
        """
        if not self.log_file:
            return
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        self._log_handler = logging.FileHandler(self.log_file)
        self._log_formatter = logging.Formatter("%(asctime)s %(message)s")
        self._log_handler.setFormatter(self._log_formatter)
        logger.addHandler(self._log_handler)

    def _purge_log_files(self) -> None:
        """Purge log files older than the configured retention period."""

        if self.config.log_retention_days < LOG_RETENTION_MIN:
            logging.error("Log retention days is less than the minimum.")
            return

        # Purge based on distinct dates in filenames (not by date range).
        log_files = sorted(self.log_file.parent.glob(f"{APP_NAME}-*.log"))
        if len(log_files) > self.config.log_retention_days:
            for file in log_files[: -self.config.log_retention_days]:
                file.unlink()

    def _append_data_csv(self, data_row: AppDataRow) -> None:
        """Append a line to the CSV file."""
        csv_str = (
            f"{data_row.version},{self._csv_date_time(data_row.date_time)},"
            f'"{data_row.action}","{data_row.message}",'
            f'"{data_row.duration}","{data_row.notes}"'
        )
        if not self.output_csv.exists():
            self.output_csv.write_text(
                "version,date,time,action,message,duration,notes\n"
            )
        with self.output_csv.open("a") as f:
            f.write(f"{csv_str}\n")

    def _csv_date_time(self, dt: datetime) -> str:
        """Return a datetime as a CSV string where the date and time are in
        separate columns.
        """
        return f'"{dt.strftime("%Y-%m-%d")}","{dt.strftime("%H:%M:%S")}"'

    def queue_error(self, error: str) -> None:
        self._errors.append(error)

    def retrieve_error_list(self) -> list[str]:
        if self._errors:
            err_list = list(self._errors)
            self._errors.clear()
            return err_list
        return []

    def write_start(
        self, start_time: datetime, task: str, session_seconds: int
    ) -> None:
        self._append_data_csv(
            AppDataRow(
                date_time=start_time,
                action="Start",
                message=task,
                duration=sec_to_hms(session_seconds),
            )
        )
        self.mru_list.add_task(task)
        self.mru_list.save()

    def write_pause(
        self,
        pause_time: datetime,
        reason: str,
        pause_seconds: int,
        session_extended: bool,
    ) -> None:
        self._append_data_csv(
            AppDataRow(
                date_time=pause_time,
                action="Pause",
                message=reason,
                duration=sec_to_hms(pause_seconds),
                notes="extended" if session_extended else "",
            )
        )
        self.mru_list.add_reason(reason)
        self.mru_list.save()

    def write_stop(self, stop_time: datetime, reason: str) -> None:
        self._append_data_csv(
            AppDataRow(date_time=stop_time, action="Stop", message=reason)
        )
        self.write_session_to_daily_files()
        # Stop should be infrequent, so do not add reason to the MRU list.

    def write_finish(self, finish_time: datetime, start_time: datetime) -> None:
        self._append_data_csv(
            AppDataRow(
                date_time=finish_time,
                action="Finish",
                notes=f"Started at {start_time.strftime('%H:%M:%S')}",
            )
        )
        self.write_session_to_daily_files()

    def set_daily_csv_dir(self, daily_csv_dir: str) -> None:
        self.config.daily_csv_dir = daily_csv_dir
        self.config.save()

    def get_daily_csv_path(self) -> Path | None:
        if not self.config.daily_csv_dir:
            return None
        path = Path(self.config.daily_csv_dir).expanduser().resolve()
        if not path.exists():
            logging.error("Directory does not exist: %s", path)
            self.queue_error(f"Directory does not exist: {path}")
            return None
        return path

    def set_daily_md_dir(self, daily_md_dir: str) -> None:
        self.config.daily_md_dir = daily_md_dir
        self.config.save()

    def get_daily_md_path(self) -> Path | None:
        if not self.config.daily_md_dir:
            return None
        path = Path(self.config.daily_md_dir).expanduser().resolve()
        if not path.exists():
            logging.error("Directory does not exist: %s", path)
            self.queue_error(f"Directory does not exist: {path}")
            return None
        return path

    def get_latest_session_rows(self) -> list[dict]:
        """Return the latest session rows from the CSV file."""
        if not self.output_csv.exists():
            return []
        with self.output_csv.open() as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        #  Get the index of the last row where action = "Start".
        #  If there is a "Start" action, return the rows from that index to
        #  the end of the list.
        #  If there is no "Start" action, return an empty list.
        last_start = None
        for i, row in enumerate(rows):
            if row["action"] == "Start":
                last_start = i
        if last_start is None:
            return []
        return rows[last_start:]

    def get_session_rows_for_date(self, date: datetime) -> list[dict]:
        """Return the session rows for a given date from the CSV file."""
        if not self.output_csv.exists():
            return []
        with self.output_csv.open() as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return [row for row in rows if row["date"] == date.strftime("%Y-%m-%d")]

    def write_session_to_daily_files(self) -> None:
        #  This must be called after write_finish.
        rows = self.get_latest_session_rows()
        if not rows:
            logging.error("Call to get_latest_session_rows returned no rows.")
            return
        self.write_session_to_daily_csv(rows)
        self.write_sessions_to_daily_md()

    def write_session_to_daily_csv(self, rows: list[dict]) -> None:
        path = self.get_daily_csv_path()
        if path:
            date_str = rows[0]["date"]
            csv_file = path / f"{date_str}.csv"
            write_to_daily_csv(csv_file, rows)

    def write_sessions_to_daily_md(self) -> None:
        """Write sessions to the daily markdown file.
        In the case where the append-only option is set, there may have been
        sessions completed before the file was created by an external
        application, so all rows for the date are passed to the write_to_daily_md
        function.
        """
        path = self.get_daily_md_path()
        if not path:
            return
        #  Get the date from the latest session.
        rows = self.get_latest_session_rows()
        if not rows:
            logging.error("Call to get_latest_session_rows returned no rows.")
            return
        date_str = rows[0]["date"]
        date_val = get_date_from_str(date_str)
        #  Get the rows for that date.
        rows = self.get_session_rows_for_date(date=date_val)
        if not rows:
            logging.error("Call to get_session_rows_for_date returned no rows.")
            return
        md_file = path / f"{date_str}.md"
        write_to_daily_md(
            md_file, self.config.daily_md_heading, self.config.daily_md_append, rows
        )

    def export_daily_csv(self, export_date: datetime, export_path: Path | None) -> None:
        path = export_path if export_path else self.get_daily_csv_path()
        if not path:
            return

        rows = self.get_session_rows_for_date(export_date)
        if not rows:
            return

        date_str = rows[0]["date"]
        csv_file = path / f"{date_str}.csv"

        # Do not overwrite existing files.
        max_num = 99
        next_num = 1
        while csv_file.exists():
            csv_file = path / f"{date_str}_{next_num}.csv"
            next_num += 1
            if next_num > max_num:
                logging.error("Too many files for %s", date_str)
                self.queue_error(f"Too many files for {date_str}")
                return

        write_to_daily_csv(csv_file, rows, start_num=1)

    def export_daily_markdown(
        self, export_date: datetime, export_path: Path | None
    ) -> None:
        path = export_path if export_path else self.get_daily_md_path()
        if not path:
            return

        rows = self.get_session_rows_for_date(export_date)
        if not rows:
            return

        date_str = rows[0]["date"]
        md_file = path / f"{date_str}.md"

        # Do not overwrite existing files.
        max_num = 99
        next_num = 1
        while md_file.exists():
            md_file = path / f"{date_str}_{next_num}.md"
            next_num += 1
            if next_num > max_num:
                logging.error("Too many files for %s", date_str)
                self.queue_error(f"Too many files for {date_str}")
                return

        heading = self.config.daily_md_heading or "# Pomodori"

        write_to_daily_md(md_file, heading, append_only=False, data_rows=rows)
