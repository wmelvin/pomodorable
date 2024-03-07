from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import dotenv
from platformdirs import user_config_path, user_data_path
from tomlkit import document, dumps, parse

APP_NAME = "pomodorable"
APP_CONFIG_FILE = f"{APP_NAME}-config.toml"
APP_OUTPUT_CSV = f"{APP_NAME}-data.csv"
APP_LOG_FILE = f"{APP_NAME}.log"
APP_DATA_VERSION = "1"

LOG_RETENTION_DEFAULT = 30
LOG_RETENTION_MIN = 5

KEY_DAILY_CSV_DIR = "daily_csv_dir"
KEY_DAILY_MD_DIR = "daily_md_dir"
KEY_LOG_RETENTION_DAYS = "log_retention_days"


@dataclass
class ConfigData:
    daily_csv_dir: str = ""
    daily_md_dir: str = ""
    log_retention_days: int = LOG_RETENTION_DEFAULT


class AppConfig:
    def __init__(self, config_file: Path) -> None:
        self.config_file = config_file
        self.data = ConfigData()

    def _load_toml_doc(self) -> document:
        """Load the TOML document from the configuration file. If the file
        doesn't exist or there is an error parsing it, return an empty
        document. If there is an error parsing the file, rename it with a
        '.bad' extension before returning the empty document.
        """
        if self.config_file.exists():
            try:
                text = self.config_file.read_text()
                return parse(text)
            except Exception:
                logging.exception("Error parsing configuration.")
                bad_file = self.config_file.with_suffix(".bad")
                logging.info("Rename bad file to '%s'", bad_file)
                self.config_file.rename(bad_file)
                return document()
        return document()

    def load(self) -> None:
        if self.config_file.exists():
            logging.info("Load '%s'", self.config_file)
            try:
                doc = self._load_toml_doc()
                self.data.daily_csv_dir = doc.get(KEY_DAILY_CSV_DIR, "")
                self.data.daily_md_dir = doc.get(KEY_DAILY_MD_DIR, "")
                self.data.log_retention_days = doc.get(
                    KEY_LOG_RETENTION_DAYS, LOG_RETENTION_DEFAULT
                )
            except Exception:
                logging.exception("Error loading configuration.")
        else:
            # Save initial config.
            self.save()

    def save(self) -> None:
        logging.info("Save '%s'", self.config_file)
        try:
            if self.config_file.exists():
                logging.info("Save to existing file")
                doc = self._load_toml_doc()
            else:
                logging.info("Save to new file")
                doc = document()
            doc[KEY_DAILY_CSV_DIR] = self.data.daily_csv_dir
            doc[KEY_DAILY_MD_DIR] = self.data.daily_md_dir
            doc[KEY_LOG_RETENTION_DAYS] = self.data.log_retention_days
            text = dumps(doc)
            self.config_file.write_text(text)
        except Exception:
            logging.exception("Error saving configuration.")


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
    def __init__(self, init_app_config: AppConfig | None = None) -> None:
        dotenv.load_dotenv()
        self._dev_output_path: Path | None = None
        dev_output_dir = os.environ.get("POMODORABLE_DEV_OUTPUT_DIR")
        if dev_output_dir:
            self._dev_output_path = Path(dev_output_dir).expanduser().resolve()
            if not self._dev_output_path.exists():
                sys.stderr.write(
                    f"\nDirectory does not exist: {self._dev_output_path}\n"
                )
                sys.exit(1)

        if self._dev_output_path:
            self.config_file = self._dev_output_path / APP_CONFIG_FILE
            self.data_path = self._dev_output_path
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
        self.log_file = self.data_path / APP_LOG_FILE
        self._init_logging()

        if init_app_config:
            self.config = init_app_config
        else:
            self.config = AppConfig(self.config_file)
            self.config.load()

        self._update_logging()

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

    def _update_logging(self) -> None:
        """Update logging after configuration is loaded. Replace the FileHandler
        with a TimedRotatingFileHandler that rotates based on the configured
        log retention days.
        """
        if not self.log_file:
            return
        logger = logging.getLogger()
        if self._log_handler:
            logger.removeHandler(self._log_handler)
        self._log_handler = TimedRotatingFileHandler(
            self.log_file,
            interval=1,
            when="D",
            backupCount=self.config.data.log_retention_days,
        )
        self._log_handler.setFormatter(self._log_formatter)
        logger.addHandler(self._log_handler)

    def _append_data_csv(self, data_row: AppDataRow) -> None:
        """Append a line to the CSV file."""
        csv_str = (
            f"{data_row.version},{self._csv_date_time(data_row.date_time)},"
            f'"{data_row.time}","{data_row.action}","{data_row.message}",'
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

    def write_stop(self, stop_time: datetime, reason: str) -> None:
        self._append_data_csv(
            AppDataRow(date_time=stop_time, action="Stop", message=reason)
        )

    def write_finish(self, finish_time: datetime, start_time: datetime) -> None:
        self._append_data_csv(
            AppDataRow(
                date_time=finish_time,
                action="Finish",
                notes=f"Started at {start_time.strftime('%H:%M:%S')}",
            )
        )

    def set_daily_csv_dir(self, daily_csv_dir: str) -> None:
        self.config.data.daily_csv_dir = daily_csv_dir
        self.config.save()

    def set_daily_md_dir(self, daily_md_dir: str) -> None:
        self.config.data.daily_md_dir = daily_md_dir
        self.config.save()


def sec_to_hms(seconds: int) -> str:
    """Convert seconds to a string in the form "HH:MM:SS" or "MM:SS" if less
    than an hour.
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"
