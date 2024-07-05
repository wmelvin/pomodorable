from __future__ import annotations

from pathlib import Path


def rows_as_md(filters: str, data_rows: list[dict]) -> list[str]:
    exclude_pause_all = "P" in filters
    exclude_pause_no_reason = "R" in filters
    exclude_stop = "X" in filters
    exclude_finish = "F" in filters
    md = []
    for row in data_rows:
        row_time = row["time"]
        # Remove seconds from time (HH:MM:SS to HH:MM).
        if row_time.count(":") == 2:  # noqa: PLR2004
            row_time = row_time.rsplit(":", 1)[0]

        if row["action"] == "Start":
            if row["notes"].startswith(("(< ", "(> ")):
                add_msg = f" ({row['duration']} session {row['notes'][1:-1]} default)"
            else:
                add_msg = ""

            msg = "(?)" if not row["message"] else row["message"]
            md.append(f"- **{msg}**")
            md.append(f"    - Start {row_time}{add_msg}")

        elif row["action"] == "Pause":
            if exclude_pause_all:
                continue
            if exclude_pause_no_reason and not row["message"]:
                continue
            act = (
                f"extend {row['duration']}" if row["notes"] == "extended" else "resume"
            )
            md.append(f"    - Pause {row_time} '{row['message']}' ({act})")

        elif row["action"] == "Stop":
            if exclude_stop:
                continue
            md.append(f"    - STOP {row_time} '{row['message']}'")

        elif row["action"] == "Finish":
            if exclude_finish:
                continue
            md.append(f"    - Finish {row_time} ({row['notes']})")
    return md


def write_to_daily_md(
    md_file: Path, filters: str, heading: str, append_only: bool, data_rows: list[dict]
) -> None:
    md_heading = f"{heading}" if heading else f"# Pomodori {data_rows[0]['date']}"

    if md_file.exists():
        lines = md_file.read_text().splitlines()
    else:
        if append_only:
            return
        lines = []

    heading_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith(md_heading):
            heading_index = i
            break

    insert_index = None
    if heading_index is None:
        hx = -1
    else:
        hx = heading_index + 2
        for i, line in enumerate(lines[hx:], start=hx):
            #  Section ends at a heading or horizontal rule.
            if line.strip().startswith(("#", "---", "***", "___")):
                insert_index = i
                break

    if insert_index is None:
        #  Append to end of file.
        insert_index = len(lines)

    if insert_index is not None:
        #  Close the gap within the section. Only leave a blank line after
        #  the heading.
        while (
            insert_index > hx
            and insert_index > 0
            and lines[insert_index - 1].strip() == ""
        ):
            insert_index -= 1

    md = [md_heading, ""] if heading_index is None else []

    if heading_index is None:
        md.extend(rows_as_md(filters, data_rows))
    else:
        md_rows = rows_as_md(filters, data_rows)
        section_rows = lines[hx:insert_index]
        md.extend([row for row in md_rows if row not in section_rows])

    a = lines[:insert_index]
    b = lines[insert_index:]

    # Keep a blank line after the inserted section.
    if (not b) or (b[0].strip() != ""):
        b.insert(0, "")

    md = [*a, *md, *b]

    with md_file.open("w") as f:
        for s in md:
            f.write(f"{s}\n")
