from __future__ import annotations

import csv
from pathlib import Path


def write_to_daily_csv(csv_file: Path, data_rows: list[dict]) -> None:
    #  Note: Output CSV layout is different from the Data CSV.

    #  Write the header row when the file is created.
    if not csv_file.exists():
        csv_file.write_text("date,time,num,task,message,notes\n")

    #  Append data rows.
    #  The num column is left blank in this case.
    with csv_file.open("a") as f:
        writer = csv.writer(f)
        for row in data_rows:
            out_row = None
            if row["action"] == "Start":
                out_row = [
                    row["date"],
                    row["time"],
                    "",
                    row["message"],
                    "",
                    "",
                ]
            elif row["action"] == "Pause":
                if row["notes"] == "extended":
                    msg = "Pause (extended)"
                else:
                    msg = "Pause (resumed)"
                out_row = [
                    row["date"],
                    row["time"],
                    "",
                    "",
                    msg,
                    row["message"],
                ]
            elif row["action"] == "Stop":
                out_row = [
                    row["date"],
                    row["time"],
                    "",
                    "",
                    "Stop",
                    row["message"],
                ]
            elif row["action"] == "Finish":
                out_row = [
                    row["date"],
                    row["time"],
                    "",
                    "",
                    "Finish",
                    row["notes"],
                ]
            if out_row:
                writer.writerow(out_row)
