from __future__ import annotations

import csv
from pathlib import Path


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
