from __future__ import annotations

from csv import DictReader
from datetime import datetime, timedelta

import pytest

from pomodorable.app_data import AppData
from pomodorable.app_utils import get_date_from_str


def test_data_csv_fields(app_data_with_test_sessions):
    app_data, start_times = app_data_with_test_sessions
    with app_data.output_csv.open() as f:
        reader = DictReader(f)
        fields = reader.fieldnames
        assert fields == [
            "version",
            "date",
            "time",
            "action",
            "message",
            "duration",
            "notes",
        ]


def test_get_latest_session_rows(app_data_with_test_sessions):
    app_data, start_times = app_data_with_test_sessions

    rows = app_data.get_latest_session_rows()
    assert rows
    assert len(rows) == 3
    assert rows[0]["action"] == "Start"
    assert rows[0]["message"] == "Test session 4"
    assert rows[0]["time"] == start_times[-1].strftime("%H:%M:%S")
    assert rows[1]["action"] == "Pause"
    assert rows[2]["action"] == "Finish"


#  Date input may come fom command-line args, so should support both full and
#  short date formats. TODO: Maybe more formats?
@pytest.mark.parametrize("date_arg", ["2024-01-02", "24-01-02"])
def test_get_session_rows_for_date(app_data_with_test_sessions, date_arg):
    app_data, start_times = app_data_with_test_sessions
    date_val = get_date_from_str(date_arg)
    rows = app_data.get_session_rows_for_date(date_val)
    assert rows
    assert len(rows) == 6


# TODO: Maybe some (but not all) of these should be valid?
@pytest.mark.parametrize(
    "date_arg", ["1/2/24", "04-MAY-23", "2024-13-01", "fatfingerdeathmunch"]
)
def test_bad_date_arg(date_arg):
    assert get_date_from_str(date_arg) is None


def test_writes_daily_csv_file(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app_data.set_daily_csv_dir(str(tmp_path))
    start_time = datetime.fromisoformat("2024-01-02T08:30:01")
    app_data.write_start(start_time, "Test session", 10)
    app_data.write_finish(
        finish_time=start_time + timedelta(seconds=10), start_time=start_time
    )
    csv_file = tmp_path / "2024-01-02.csv"
    assert csv_file.exists()
    with csv_file.open() as f:
        reader = DictReader(f)
        fields = reader.fieldnames
        assert fields == ["date", "time", "num", "task", "message", "notes"]


def test_writes_daily_markdown_file(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app_data.set_daily_md_dir(str(tmp_path))
    start_time = datetime.fromisoformat("2024-01-02T08:30:01")
    app_data.write_start(start_time, "Test session", 10)
    app_data.write_finish(
        finish_time=start_time + timedelta(seconds=10), start_time=start_time
    )
    md_file = tmp_path / "2024-01-02.md"
    assert md_file.exists()
    md_text = md_file.read_text()
    assert "# 2024-01-02" in md_text
