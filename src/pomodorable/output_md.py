from __future__ import annotations

from pathlib import Path


def rows_as_md(data_rows: list[dict]) -> list[str]:
    md = []
    for row in data_rows:
        out_str = None
        if row["action"] == "Start":
            out_str = f"- {row['message']}"
            out_str += f"    - Start {row['time']}"

        elif row["action"] == "Pause":
            if row["notes"] == "extended":
                msg = "Pause (extended):"
            else:
                msg = "Pause (resumed):"
            out_str = f"    - {msg} {row['message']}"

        elif row["action"] == "Stop":
            out_str = f"    - Stop: {row['message']}"

        elif row["action"] == "Finish":
            out_str = f"    - Finish: {row['notes']}"
        if out_str is not None:
            md.append(out_str)
    return md


def write_to_daily_md(
    md_file: Path, heading: str, append_only: bool, data_rows: list[dict]
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

    md.extend(rows_as_md(data_rows))

    a = lines[:insert_index]
    b = lines[insert_index:]

    # Keep a blank line after the inserted section.
    if (not b) or (b[0].strip() != ""):
        b.insert(0, "")

    md = [*a, *md, *b]

    with md_file.open("w") as f:
        for s in md:
            f.write(f"{s}\n")
