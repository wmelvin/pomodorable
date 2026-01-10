from __future__ import annotations

import logging
from csv import DictReader
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import pytest

from pomodorable.app_config import AppConfig
from pomodorable.app_data import AppData
from pomodorable.app_utils import get_date_from_str
from pomodorable.output_md import write_to_daily_md


def test_data_csv_fields(app_data_with_four_test_sessions):
    app_data, _ = app_data_with_four_test_sessions
    with app_data._data_csv.open() as f:
        reader = DictReader(f)
        fields = reader.fieldnames
        assert fields == [
            "version",
            "started",
            "date",
            "time",
            "action",
            "message",
            "duration",
            "notes",
        ]


def test_get_latest_session_rows(app_data_with_four_test_sessions):
    app_data, start_times = app_data_with_four_test_sessions

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
def test_get_session_rows_for_date(app_data_with_four_test_sessions, date_arg):
    app_data, _ = app_data_with_four_test_sessions
    date_val = get_date_from_str(date_arg)
    rows = app_data.get_session_rows_for_date(date_val)
    assert rows
    assert len(rows) == 6


# TODO: Maybe some (but not all) of these should be valid?
@pytest.mark.parametrize("date_arg", ["1/2/24", "04-MAY-23", "2024-13-01", "fatfingerdeathmunch"])
def test_bad_date_arg(date_arg):
    assert get_date_from_str(date_arg) is None


def test_writes_daily_csv_file(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app_data.set_daily_csv_dir(str(tmp_path))

    # Write first session with pauses and finish.
    start_time = datetime.fromisoformat("2024-01-02T08:30:01")

    app_data.write_start(start_time, "Test session 1", 10)

    t = start_time + timedelta(seconds=5)
    app_data.write_pause(
        start_time=start_time,
        pause_time=t,
        reason="Pause, extended",
        pause_seconds=5,
        session_extended=True,
    )

    t = start_time + timedelta(seconds=12)
    app_data.write_pause(
        start_time=start_time,
        pause_time=t,
        reason="Pause, resume",
        pause_seconds=2,
        session_extended=False,
    )

    t = start_time + timedelta(seconds=15)
    app_data.write_finish(finish_time=t, start_time=start_time)

    # Write second session with stop.
    start_time = datetime.fromisoformat("2024-01-02T09:00:00")

    app_data.write_start(start_time, "Test session 2", 10)

    t = start_time + timedelta(seconds=5)
    app_data.write_stop(start_time=start_time, stop_time=t, reason="Test stop")

    csv_file = tmp_path / "2024-01-02.csv"
    assert csv_file.exists()
    with csv_file.open() as f:
        reader = DictReader(f)
        fields = reader.fieldnames
        assert fields == ["date", "act", "time", "task", "message", "notes"]
    text = csv_file.read_text()
    assert "Test session 1" in text
    assert "Pause, extended" in text
    assert "Pause, resume" in text
    assert "Finish" in text
    assert "Test session 2" in text
    assert "Test stop" in text

    # Check for note when session length is not the default.
    assert "(0:00:10 session < 0:25:00 default)" in text


def test_writes_running_csv_file_default_name(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app_data.set_running_csv_dir(str(tmp_path))

    start_time = datetime.fromisoformat("2024-01-02T08:30:01")
    app_data.write_start(start_time, "Test session 1", 10)

    t = start_time + timedelta(seconds=5)
    app_data.write_stop(start_time=start_time, stop_time=t, reason="Test stop")

    csv_file = tmp_path / "pomodorable-sessions.csv"
    assert csv_file.exists()


def test_writes_running_csv_file_specify_name(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app_data.set_running_csv_dir(str(tmp_path))
    app_data.set_running_csv_name("test-sessions.csv")

    start_time = datetime.fromisoformat("2024-01-02T08:30:01")
    app_data.write_start(start_time, "Test session 1", 10)

    t = start_time + timedelta(seconds=5)
    app_data.write_stop(start_time=start_time, stop_time=t, reason="Test stop")

    csv_file = tmp_path / "test-sessions.csv"
    assert csv_file.exists()


def test_daily_markdown_writes_file(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app_data.set_daily_md_dir(str(tmp_path))

    start_time = datetime.fromisoformat("2024-01-02T08:30:01")

    app_data.write_start(start_time, "Test session", 10)
    app_data.write_finish(finish_time=start_time + timedelta(seconds=10), start_time=start_time)

    md_file = tmp_path / "2024-01-02.md"
    assert md_file.exists()

    md_text = md_file.read_text()
    assert "# Pomodori 2024-01-02" in md_text

    # Check for note when session length is not the default.
    assert "(0:00:10 session < 0:25:00 default)" in md_text


def test_daily_markdown_does_not_create_when_append_only(tmp_path):
    app_data = AppData(init_data_path=tmp_path)
    app_data.config.daily_md_append = True
    app_data.set_daily_md_dir(str(tmp_path))

    start_time = datetime.fromisoformat("2024-01-02T08:30:01")

    app_data.write_start(start_time, "Test session", 10)
    app_data.write_finish(finish_time=start_time + timedelta(seconds=10), start_time=start_time)

    md_files = list(tmp_path.glob("*.md"))
    assert not md_files


def test_daily_markdown_written(app_data_with_four_test_sessions):
    app_data, start_times = app_data_with_four_test_sessions
    p = app_data.data_path
    md_file: Path = p / "test.md"

    rows = app_data.get_session_rows_for_date(start_times[0])
    assert len(rows) == 6

    write_to_daily_md(md_file=md_file, filters="", heading="", append_only=False, data_rows=rows[:3])

    # Make a copy for manual review in tmp location.
    (p / "test-1.md").write_text(md_file.read_text())

    write_to_daily_md(md_file=md_file, filters="", heading="", append_only=False, data_rows=rows[3:])


def test_daily_markdown_append(app_data_with_six_test_sessions):
    app_data, start_times = app_data_with_six_test_sessions
    p = app_data.data_path
    md_file: Path = p / "test.md"

    rows = app_data.get_session_rows_for_date(start_times[0])
    assert len(rows) == 12

    a = "# Blah\n\nblah blah\n\n## Pomodori\n"
    b = "\n# More blah\n\n"

    md_file.write_text(f"{a}{b}")

    (p / "test-cp-1-before-write.md").write_text(md_file.read_text())

    write_to_daily_md(
        md_file=md_file,
        filters="",
        heading="## Pomodori",
        append_only=True,
        data_rows=rows[:6],
    )

    (p / "test-cp-2-after-write.md").write_text(md_file.read_text())

    write_to_daily_md(
        md_file=md_file,
        filters="",
        heading="## Pomodori",
        append_only=True,
        data_rows=rows,
    )

    s = md_file.read_text()
    assert s.startswith(a)
    assert s.endswith(b)
    assert "Test session 1" in s
    assert "Test session 2" in s
    assert "Test session 3" in s


def test_daily_markdown_append_when_created_after_session(
    app_data_with_six_test_sessions,
):
    app_data, start_times = app_data_with_six_test_sessions
    p = app_data.data_path
    md_file: Path = p / "test.md"

    rows = app_data.get_session_rows_for_date(start_times[0])
    assert len(rows) == 12

    write_to_daily_md(
        md_file=md_file,
        filters="",
        heading="## Pomodori",
        append_only=True,
        data_rows=rows,
    )

    assert not md_file.exists()

    a = "# Blah\n\nblah blah\n\n## Pomodori\n"
    b = "\n# More blah\n\n"
    md_file.write_text(f"{a}{b}")

    (p / "test-cp-1-before-write.md").write_text(md_file.read_text())

    write_to_daily_md(
        md_file=md_file,
        filters="",
        heading="## Pomodori",
        append_only=True,
        data_rows=rows,
    )

    s = md_file.read_text()
    assert s.startswith(a)
    assert s.endswith(b)
    assert "Test session 1" in s
    assert "Test session 2" in s
    assert "Test session 3" in s


def test_daily_markdown_append_when_task_revisited(
    app_data_six_sessions_alt_tasks_w_pause,
):
    app_data, start_times = app_data_six_sessions_alt_tasks_w_pause
    p = app_data.data_path
    md_file: Path = p / "test.md"

    rows = app_data.get_session_rows_for_date(start_times[0])
    assert len(rows) == 24

    a = "# Blah\n\nblah blah\n\n## Pomodori\n"
    b = "\n# More blah\n\n"
    md_file.write_text(f"{a}{b}")

    (p / "test-cp-1-before-write.md").write_text(md_file.read_text())

    write_to_daily_md(
        md_file=md_file,
        filters="",
        heading="## Pomodori",
        append_only=True,
        data_rows=rows,
    )

    s = md_file.read_text()

    #  Sessions should be inserted before second level-1 heading.
    assert s.startswith(a)
    assert s.endswith(b)

    #  Both tasks should appear in output.
    assert "Task 1" in s
    assert "Task 2" in s

    #  Task 1 should appear again after Task 2.
    a = s.split("Task 2")
    assert len(a) == 2
    assert "Task 1" in a[0]
    assert "Task 1" in a[1]


def test_daily_markdown_append_tasks_stray_start(tmp_path: Path):
    #  What happens when the app is terminated before Stop or Finish?
    config_file = tmp_path / "pomodorable-config.toml"

    app_config = AppConfig(config_file)
    app_config.daily_md_heading = "## Pomodori"
    app_config.daily_md_append = True
    # app_config.filter_md = "FR"
    app_data = AppData(init_app_config=app_config, init_data_path=tmp_path)
    app_data.set_daily_md_dir(str(app_data.data_path))

    start_times = [
        datetime.fromisoformat("2025-12-28T08:30:01"),
        datetime.fromisoformat("2025-12-28T09:30:01"),
        datetime.fromisoformat("2025-12-28T10:05:01"),
        datetime.fromisoformat("2025-12-28T11:35:01"),
        datetime.fromisoformat("2025-12-28T12:05:01"),
        datetime.fromisoformat("2025-12-28T13:35:01"),
    ]

    tasks = [
        "Task 1",
        "Task 1",
        "Task 2",
        "Task 3",
        "Task 4",
        "Task 5",
    ]

    md_file: Path = app_data.data_path / "2025-12-28.md"

    # #  Create as if done by an external program (such as Obsidian).
    a = "# Blah\n\nblah blah\n\n## Pomodori\n"
    b = "\n# More blah\n\n"
    md_file.write_text(f"{a}{b}")

    i = 0
    app_data.write_start(start_times[i], tasks[0], 300)

    # #  Simulate restart.
    # app_config = AppConfig(config_file)
    # app_config.daily_md_heading = "## Pomodori"
    # app_config.daily_md_append = True
    # app_config.filter_md = "FR"
    # app_data = AppData(init_app_config=app_config, init_data_path=tmp_path)
    # app_data.set_daily_md_dir(str(app_data.data_path))

    i = 1
    app_data.write_start(start_times[i], tasks[i], 300)
    app_data.write_pause(
        start_times[i],
        pause_time=start_times[i] + timedelta(seconds=10),
        reason="",
        pause_seconds=10,
        session_extended=True,
    )
    app_data.write_finish(finish_time=start_times[i] + timedelta(seconds=310), start_time=start_times[i])

    for i in range(2, 6):
        app_data.write_start(start_times[i], tasks[i], 300)
        app_data.write_finish(finish_time=start_times[i] + timedelta(seconds=310), start_time=start_times[i])

    assert md_file.exists()
    s = md_file.read_text()

    #  Sessions should be inserted before second level-1 heading.
    assert s.startswith(a)
    assert s.endswith(b)

    assert s.count("Task 1") == 2
    assert s.count("Task 2") == 1
    assert s.count("Task 3") == 1
    assert s.count("Task 4") == 1
    assert s.count("Task 5") == 1


def test_purge_log_files(tmp_path):
    config_file = tmp_path / "pomodorable-config.toml"
    app_config = AppConfig(config_file)
    app_data = AppData(init_app_config=app_config, init_data_path=tmp_path)

    # Make 8 fake log files.
    for i in range(8):
        p = tmp_path / f"pomodorable-2024010{i + 1}.log"
        p.write_text("")

    # Should create a new log file.
    assert app_data.log_file.exists()

    # Default retention days is 30. Change it to 5.
    app_data.config.log_retention_days = 5

    # Run the private method to purge older log files.
    app_data._purge_log_files()

    # Check that all but 5 most recent were purged.
    log_files = sorted(tmp_path.glob("*.log"))
    assert len(log_files) == 5
    assert log_files[0].name == "pomodorable-20240105.log"
    assert log_files[-2].name == "pomodorable-20240108.log"
    assert log_files[-1].name == app_data.log_file.name


@pytest.mark.parametrize(
    ("env_value", "log_level"),
    [
        ("", "INFO"),
        ("False", "INFO"),
        ("No", "INFO"),
        ("0", "INFO"),
        ("True", "DEBUG"),
        ("yes", "DEBUG"),
        ("Y", "DEBUG"),
        ("1", "DEBUG"),
        ("Marbles", "INFO"),
    ],
)
def test_set_debug_logging(tmp_path, env_value, log_level, monkeypatch):
    monkeypatch.setenv("POMODORABLE_DEBUG", env_value)
    config_file = tmp_path / "pomodorable-config.toml"
    app_config = AppConfig(config_file)
    app_data = AppData(init_app_config=app_config, init_data_path=tmp_path)
    assert app_data
    logr = logging.getLogger()
    levl = logging.getLevelName(logr.level)
    assert levl == log_level


@pytest.mark.parametrize(
    ("filter_value", "act_code", "expected_count"),
    [
        ("", "F", 1),
        ("F", "F", 0),
        ("", "E", 2),
        ("", "R", 2),
        ("P", "E", 0),
        ("P", "R", 0),
        ("R", "E", 1),
        ("R", "R", 1),
        ("", "X", 1),
        ("X", "X", 0),
    ],
)
def test_filters_csv_output(tmp_path, filter_value, act_code, expected_count):
    app_data = AppData(init_data_path=tmp_path)
    app_data.set_daily_csv_dir(str(tmp_path))
    app_data.config.filter_csv = filter_value

    # Write first session with pauses and finish.
    start_time = datetime.fromisoformat("2024-01-02T08:30:01")

    app_data.write_start(start_time, "Test session 1", 10)

    # Extend (E) with a reason noted.
    t = start_time + timedelta(seconds=10)
    app_data.write_pause(
        start_time=start_time,
        pause_time=t,
        reason="Pause, extended",
        pause_seconds=5,
        session_extended=True,
    )

    # Resume (R) with a reason noted.
    t = t + timedelta(seconds=10)
    app_data.write_pause(
        start_time=start_time,
        pause_time=t,
        reason="Pause, resume",
        pause_seconds=2,
        session_extended=False,
    )

    # Extend (E) without a reason noted.
    t = t + timedelta(seconds=10)
    app_data.write_pause(
        start_time=start_time,
        pause_time=t,
        reason="",
        pause_seconds=5,
        session_extended=True,
    )

    # Resume (R) without a reason noted.
    t = t + timedelta(seconds=10)
    app_data.write_pause(
        start_time=start_time,
        pause_time=t,
        reason="",
        pause_seconds=2,
        session_extended=False,
    )

    # Finish (F).
    t = t + timedelta(seconds=10)
    app_data.write_finish(finish_time=t, start_time=start_time)

    # Write second session with stop.
    start_time = datetime.fromisoformat("2024-01-02T09:00:00")

    app_data.write_start(start_time, "Test session 2", 10)

    # Stop (X).
    t = start_time + timedelta(seconds=5)
    app_data.write_stop(start_time=start_time, stop_time=t, reason="Test stop")

    csv_file = tmp_path / "2024-01-02.csv"
    assert csv_file.exists()

    with csv_file.open() as f:
        reader = DictReader(f)
        fields = reader.fieldnames
        assert fields == ["date", "act", "time", "task", "message", "notes"]
        acts = [row["act"] for row in reader]

    assert acts.count(act_code) == expected_count


@pytest.mark.parametrize(
    ("filter_value", "find_str", "expected_count"),
    [
        ("", "- Finish", 1),
        ("F", "- Finish", 0),
        ("", "(extend", 2),
        ("", "(resume", 2),
        ("P", "(extend", 0),
        ("P", "(resume", 0),
        ("R", "(extend", 1),
        ("R", "(resume", 1),
        ("", "- STOP", 1),
        ("X", "- STOP", 0),
    ],
)
def test_filters_markdown_output(tmp_path, filter_value, find_str, expected_count):
    app_data = AppData(init_data_path=tmp_path)
    app_data.set_daily_md_dir(str(tmp_path))
    app_data.config.filter_md = filter_value

    # Write first session with pauses and finish.
    start_time = datetime.fromisoformat("2024-01-02T08:30:01")

    app_data.write_start(start_time, "Test session 1", 10)

    # Extend (E) with a reason noted.
    t = start_time + timedelta(seconds=10)
    app_data.write_pause(
        start_time=start_time,
        pause_time=t,
        reason="Pause, extended",
        pause_seconds=5,
        session_extended=True,
    )

    # Resume (R) with a reason noted.
    t = t + timedelta(seconds=10)
    app_data.write_pause(
        start_time=start_time,
        pause_time=t,
        reason="Pause, resume",
        pause_seconds=2,
        session_extended=False,
    )

    # Extend (E) without a reason noted.
    t = t + timedelta(seconds=10)
    app_data.write_pause(
        start_time=start_time,
        pause_time=t,
        reason="",
        pause_seconds=5,
        session_extended=True,
    )

    # Resume (R) without a reason noted.
    t = t + timedelta(seconds=10)
    app_data.write_pause(
        start_time=start_time,
        pause_time=t,
        reason="",
        pause_seconds=2,
        session_extended=False,
    )

    # Finish (F).
    t = t + timedelta(seconds=10)
    app_data.write_finish(finish_time=t, start_time=start_time)

    # Write second session with stop.
    start_time = datetime.fromisoformat("2024-01-02T09:00:00")

    app_data.write_start(start_time, "Test session 2", 10)

    # Stop (X).
    t = start_time + timedelta(seconds=5)
    app_data.write_stop(start_time=start_time, stop_time=t, reason="Test stop")

    md_file = tmp_path / "2024-01-02.md"
    assert md_file.exists()

    text = md_file.read_text()
    assert text.count(find_str) == expected_count


def test_data_csv_exists_but_is_empty(tmp_path):
    # Make empty data file.
    data_file = tmp_path / "pomodorable-data.csv"
    data_file.touch()

    app_data = AppData(init_data_path=tmp_path)
    app_data.set_daily_csv_dir(str(tmp_path))

    # On initialization, app_data._check_data_csv should have renamed and
    # replaced the empty file.
    assert len(list(tmp_path.glob("*.bad"))) == 1

    # Cause trouble by making the data file empty again.
    data_file.write_text("")

    # Write some actions.
    app_data.write_start(datetime.now(), "Test session", 10)
    app_data.write_finish(datetime.now(), datetime.now())
    app_data.write_session_to_output_files()

    # On writing to the data file, app_data._check_data_csv should have
    # renamed and replaced the empty file.
    assert len(list(tmp_path.glob("*.bad"))) == 2

    # Output should be successful.
    p = app_data.get_daily_csv_path()
    assert p.exists()


def test_timesheet_export_handles_stop_after_extend(tmp_path: Path):
    test_data_rows = [
        "version,started,date,time,action,message,duration,notes",
        '2,2025-07-09T12:46:43.058968,"2025-07-09","12:46:43","Start","Project work","0:25:00",""',
        '2,2025-07-09T12:46:43.058968,"2025-07-09","13:11:43","Finish","","","Started at 12:46:43"',
        '2,2025-07-09T14:19:50.055301,"2025-07-09","14:19:50","Start","Project work","0:25:00",""',
        '2,2025-07-09T14:19:50.055301,"2025-07-09","14:36:43","Pause","","0:05:52","extended"',
        '2,2025-07-09T14:19:50.055301,"2025-07-09","14:50:42","Finish","","","Started at 14:19:50"',
        # Start - Stop (in less than a minute):
        '2,2025-07-09T16:06:56.738636,"2025-07-09","16:06:56","Start","","0:25:00",""',
        '2,2025-07-09T16:06:56.738636,"2025-07-09","16:07:04","Stop","","",""',
        # Start - Pause - Extend - Stop:
        '2,2025-07-09T16:07:12.665355,"2025-07-09","16:07:12","Start","Project work","0:25:00",""',
        '2,2025-07-09T16:07:12.665355,"2025-07-09","16:12:18","Pause","","0:27:59","extended"',
        '2,2025-07-09T16:07:12.665355,"2025-07-09","16:44:29","Stop","Have to leave","",""',
    ]
    data_file = tmp_path / "pomodorable-data.csv"
    data_file.write_text("\n".join(test_data_rows))

    app_data = AppData(init_data_path=tmp_path)
    app_data.set_daily_csv_dir(str(tmp_path))

    lines = data_file.read_text().splitlines()
    assert len(lines) == len(test_data_rows)

    out_path = tmp_path / "output"
    out_path.mkdir()

    app_data.cli_export_date_range_csv(
        datetime.fromisoformat("2025-07-08"),
        datetime.fromisoformat("2025-07-10"),
        True,
        "",
        out_path,
    )

    #  Should be one csv file in output.
    files = sorted(out_path.glob("*.csv"))
    assert len(files) == 1

    #  Should be five lines in the file.
    ts = files[0]
    lines = ts.read_text().splitlines()
    assert len(lines) == 5

    #  First line should be the CSV header.
    assert lines[0] == "date,start_time,stop_time,task_minutes,pause_minutes,task,notes"

    #  Verify task_minutes.
    assert lines[0].split(",")[3] == "task_minutes"
    assert lines[1].split(",")[3] == "25"

    #  Pause-to-Extend time should be subtracted from Start-to-Finish.
    assert lines[2].split(",")[3] == "25"

    #  Stoping less than a minute into a session should result in zero minutes.
    assert lines[3].split(",")[3] == "0"

    #  Pause-to-Extend time should be subtracted from Start-to-Stop.
    assert lines[4].split(",")[3] == "9"
