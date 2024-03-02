from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

import dotenv
from platformdirs import user_config_path, user_data_path

APP_NAME = "pomodorable"
APP_CONFIG_FILE = f"{APP_NAME}-config.json"
APP_OUTPUT_CSV = f"{APP_NAME}-data.csv"


class AppData:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.dev_output_path: Path | None = None
        dev_output_dir = os.environ.get("POMODORABLE_DEV_OUTPUT_DIR")
        if dev_output_dir:
            self.dev_output_path = Path(dev_output_dir).expanduser().resolve()
            if not self.dev_output_path.exists():
                sys.stderr.write(
                    f"\nDirectory does not exist: {self.dev_output_path}\n"
                )
                sys.exit(1)

        if self.dev_output_path:
            self.config_file = self.dev_output_path / APP_CONFIG_FILE
            self.output_csv = self.dev_output_path / APP_OUTPUT_CSV
        else:
            self.config_file = (
                user_config_path(APP_NAME, appauthor=False, ensure_exists=True)
                / APP_CONFIG_FILE
            )
            self.output_csv = (
                user_data_path(APP_NAME, appauthor=False, ensure_exists=True)
                / APP_OUTPUT_CSV
            )

    def append_csv(self, csv_str: str) -> None:
        if not self.output_csv.exists():
            self.output_csv.write_text("date,time,action,message,duration,notes\n")
        with self.output_csv.open("a") as f:
            f.write(f"{csv_str}\n")

    def csv_date_time(self, dt: datetime) -> str:
        return f'"{dt.strftime("%Y-%m-%d")}","{dt.strftime("%H:%M:%S")}"'

    def write_start(
        self, start_time: datetime, task: str, session_seconds: int
    ) -> None:
        dt_csv = self.csv_date_time(start_time)
        self.append_csv(f'{dt_csv},"Start","{task}","{sec_to_hms(session_seconds)}",""')

    def write_pause(
        self,
        pause_time: datetime,
        reason: str,
        pause_seconds: int,
        session_extended: bool,
    ) -> None:
        dt_csv = self.csv_date_time(pause_time)
        extended = "extended" if session_extended else ""
        self.append_csv(
            f'{dt_csv},"Pause","{reason}","{sec_to_hms(pause_seconds)}","{extended}"'
        )

    def write_stop(self, stop_time: datetime, reason: str) -> None:
        dt_csv = self.csv_date_time(stop_time)
        self.append_csv(f'{dt_csv},"Stop","{reason}","",""')

    def write_finish(self, finish_time: datetime, start_time: datetime) -> None:
        dt_csv = self.csv_date_time(finish_time)
        start_note = f"Started at {start_time.strftime('%H:%M:%S')}"
        self.append_csv(f'{dt_csv},"Finish","","","{start_note}"')


def sec_to_hms(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"
