from __future__ import annotations

from pathlib import Path


def write_to_daily_md(md_file: Path, data_rows: list[dict]) -> None:

    date_str = data_rows[0]["date"]

    #  Write the header when the file is created.
    if not md_file.exists():
        md_file.write_text(f"# {date_str}\n\n")

    #  Append data rows.
    with md_file.open("a") as f:
        for row in data_rows:
            out_str = None
            if row["action"] == "Start":
                out_str = f"- {row['message']}\n"
                out_str += f"    - Start {row['time']}\n"

            elif row["action"] == "Pause":
                if row["notes"] == "extended":
                    msg = "Pause (extended):"
                else:
                    msg = "Pause (resumed):"
                out_str = f"    - {msg} {row['message']}\n"

            elif row["action"] == "Stop":
                out_str = f"    - Stop: {row['message']}\n"

            elif row["action"] == "Finish":
                out_str = f"    - Finish: {row['notes']}\n"

            if out_str:
                f.write(out_str)
