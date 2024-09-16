from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from pomodorable.app_utils import hms_to_sec


def get_start_msg(row_notes: str, row_duration: str):
    # If row_notes contains the indicator for a non-default session duration
    # return a formatted message.
    if row_notes.startswith(("(< ", "(> ")):
        return f"({row_duration} session {row_notes[1:-1]} default)"
    return ""


def write_to_sessions_csv(
    csv_file: Path, filters: str, data_rows: list[dict], start_num: int = 0
) -> None:
    #  Note: Output CSV layout is different from the Data CSV.

    exclude_pause_all = "P" in filters
    exclude_pause_no_reason = "R" in filters
    exclude_stop = "X" in filters
    exclude_finish = "F" in filters

    #  Write the header row when the file is created.
    if not csv_file.exists():
        csv_file.write_text("date,act,time,task,message,notes\n")

    #  If start_num is greater than 0, then session_num will be
    #  incremented at each 'Start' row, and the session_num will
    #  be in the 'act' column for the 'Start' action. Otherwise,
    #  and for other actions, the 'act' column will contain a
    #  single character code for the action.
    #
    session_num = start_num

    #  Append data rows.
    with csv_file.open("a", newline="") as f:
        writer = csv.writer(f)
        last_date = None
        for row in data_rows:
            action = row["action"]
            row_message = row["message"]
            row_notes = row["notes"]
            out_row = None
            if action == "Start":
                # If a start_num was provided and the current row begins a new
                # date (exporting a date range), then reset the session_num.
                if start_num > 0 and last_date is not None and row["date"] != last_date:
                    session_num = 1
                    # Write a row with only the date as a separator between days.
                    writer.writerow([row["date"], "", "", "", "", ""])

                out_row = [
                    row["date"],
                    session_num or "S",
                    row["time"],
                    row_message,  # task
                    get_start_msg(row_notes, row["duration"]),
                    "",
                ]
                if start_num > 0:
                    session_num += 1
                last_date = row["date"]
            elif action == "Pause":
                if exclude_pause_all:
                    continue
                if exclude_pause_no_reason and len(row_message) == 0:
                    continue
                if row_notes == "extended":
                    out_act = "E"
                    out_msg = "Pause (extended)"
                else:
                    out_act = "R"
                    out_msg = "Pause (resumed)"
                out_row = [
                    row["date"],
                    out_act,
                    row["time"],
                    "",
                    out_msg,
                    row_message,
                ]
            elif action == "Stop":
                if exclude_stop:
                    continue
                out_row = [
                    row["date"],
                    "X",
                    row["time"],
                    "",
                    "Stop",
                    row_message,
                ]
            elif action == "Finish":
                if exclude_finish:
                    continue
                out_row = [
                    row["date"],
                    "F",
                    row["time"],
                    "",
                    "Finish",
                    row_notes,
                ]
            if out_row:
                writer.writerow(out_row)


class TaskSession:
    def __init__(self, date: str, start_time: str, task: str, duration: str):
        self.date = date
        self.start_time = start_time
        self.stop_time = None
        self.task = task
        self.reasons = ""
        self.task_seconds = hms_to_sec(duration)
        self.pause_seconds = 0

    def pause(self, message: str, duration: str, notes: str) -> None:
        if notes == "extended":
            act = "Extend"
        else:
            act = "Resume"
            self.pause_seconds += hms_to_sec(duration)
        if message:
            self.reasons += f"{act}: {message} | "

    def stop(self, stop_date: str, stop_time: str, message: str) -> None:
        self.stop_time = stop_time

        start_datetime: datetime = datetime.strptime(  # noqa: DTZ007
            f"{self.date} {self.start_time}", "%Y-%m-%d %H:%M:%S"
        )

        stop_datetime: datetime = datetime.strptime(  # noqa: DTZ007
            f"{stop_date} {stop_time}", "%Y-%m-%d %H:%M:%S"
        )

        assert stop_datetime >= start_datetime  # noqa: S101

        self.task_seconds = (stop_datetime - start_datetime).total_seconds()

        if message:
            self.reasons += f"STOP: {message}"
        else:
            self.reasons += "STOP"

    def finish(self, finish_time: str) -> None:
        self.stop_time = finish_time

    def as_dict(self):
        """Return a dictionary with the session data for writing to a CSV file."""

        # For the time-on-task, only completed minutes are counted (no rounding).
        task_minutes_initial = int(self.task_seconds / 60)
        task_minutes_final = int((self.task_seconds - self.pause_seconds) / 60)
        pause_minutes = task_minutes_initial - task_minutes_final

        reason_notes = self.reasons.rstrip(" |")

        return {
            "date": self.date,
            "start_time": self.start_time,
            "stop_time": self.stop_time,
            "task_minutes": task_minutes_final,
            "pause_minutes": pause_minutes,
            "task": self.task,
            "notes": reason_notes,
        }


def write_to_timesheet_csv(csv_file: Path, data_rows: list[dict]) -> None:
    header = "date,start_time,stop_time,task_minutes,pause_minutes,task,notes"

    #  Write the header row when the file is created.
    if not csv_file.exists():
        csv_file.write_text(f"{header}\n")

    #  Append data rows.
    with csv_file.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header.split(","))
        session: TaskSession = None
        for row in data_rows:
            action = row["action"]
            if action == "Start":
                if session is not None:
                    writer.writerow(session.as_dict())
                session = TaskSession(
                    row["date"], row["time"], row["message"], row["duration"]
                )
            elif action == "Pause":
                session.pause(row["message"], row["duration"], row["notes"])
            elif action == "Stop":
                session.stop(row["date"], row["time"], row["message"])
            elif action == "Finish":
                session.finish(row["time"])
                if session is not None:
                    writer.writerow(session.as_dict())
                session = None
        if session is not None:
            writer.writerow(session.as_dict())
