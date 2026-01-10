from pathlib import Path

import pytest
from click.testing import CliRunner

from pomodorable.cli import cli


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "pomodorable, version" in result.output


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS]" in result.output
    assert "Show this message and exit." in result.output


@pytest.mark.parametrize("subdir_param", [None, "exported"])
def test_export_csv_for_date(app_data_with_four_test_sessions, subdir_param, monkeypatch):
    app_data, _ = app_data_with_four_test_sessions
    data_dir = str(app_data.data_path)
    app_data.set_daily_csv_dir(data_dir)

    # Set the environment variable used by the AppData class to override its
    # data_path when initialized via the CLI.
    monkeypatch.setenv("POMODORABLE_TEST_DATA_DIR", data_dir)

    if subdir_param:
        export_path = Path(data_dir) / subdir_param
        export_path.mkdir()
        args = [
            "--csv-date",
            "2024-01-02",
            "--export-path",
            str(export_path),
        ]
    else:
        export_path = app_data.data_path
        args = ["--csv-date", "2024-01-02"]

    runner = CliRunner()
    result = runner.invoke(cli, args)
    print(result.output)
    assert result.exit_code == 0

    csv_file = export_path / "2024-01-02.csv"
    assert csv_file.exists()

    rows = csv_file.read_text().strip().split("\n")
    assert len(rows) == 7  # 1 header + 6 data rows


@pytest.mark.parametrize(
    ("subdir_param", "filter_arg"),
    [(None, None), ("exported", None), ("exported", "--filters=FPD")],
)
def test_export_csv_for_date_range(app_data_with_four_test_sessions, subdir_param, filter_arg, monkeypatch):
    app_data, _ = app_data_with_four_test_sessions
    data_dir = str(app_data.data_path)
    app_data.set_running_csv_dir(data_dir)

    # Set the environment variable used by the AppData class to override its
    # data_path when initialized via the CLI.
    monkeypatch.setenv("POMODORABLE_TEST_DATA_DIR", data_dir)

    if subdir_param:
        export_path = Path(data_dir) / subdir_param
        export_path.mkdir()
        args = [
            "--csv-date",
            "2024-01-02",
            "--end-date",
            "2024-01-03",
            "--export-path",
            str(export_path),
        ]
    else:
        export_path = app_data.data_path
        args = ["--csv-date", "2024-01-02", "--end-date", "2024-01-03"]

    if filter_arg:
        args.append(filter_arg)

    runner = CliRunner()
    result = runner.invoke(cli, args)
    print(result.output)
    assert result.exit_code == 0

    csv_file = export_path / "po-20240102-20240103.csv"
    assert csv_file.exists()

    rows = csv_file.read_text().strip().split("\n")

    #  Check CSV file content.
    if filter_arg is None:
        expect_lines = [
            "date,act,time,task,message,notes",
            "2024-01-02,1,08:30:01,Test session 1,(0:00:10 session < 0:25:00 default),",
            "2024-01-02,R,08:30:03,,Pause (resumed),Test pause 1",
            "2024-01-02,F,08:30:11,,Finish,Started at 08:30:01",
            "2024-01-02,2,09:30:01,Test session 2,(0:00:10 session < 0:25:00 default),",
            "2024-01-02,R,09:30:03,,Pause (resumed),Test pause 2",
            "2024-01-02,F,09:30:11,,Finish,Started at 09:30:01",
            ".,,,,,",
            "2024-01-03,1,08:05:01,Test session 3,(0:00:10 session < 0:25:00 default),",
            "2024-01-03,R,08:05:03,,Pause (resumed),Test pause 3",
            "2024-01-03,F,08:05:11,,Finish,Started at 08:05:01",
            "2024-01-03,2,08:35:01,Test session 4,(0:00:10 session < 0:25:00 default),",
            "2024-01-03,R,08:35:03,,Pause (resumed),Test pause 4",
            "2024-01-03,F,08:35:11,,Finish,Started at 08:35:01",
        ]
    else:
        #  With 'filter=FPD'
        expect_lines = [
            "date,act,time,task,message,notes",
            "2024-01-02,1,08:30:01,Test session 1,(0:00:10 session < 0:25:00 default),",
            ",2,09:30:01,Test session 2,(0:00:10 session < 0:25:00 default),",
            ".,,,,,",
            "2024-01-03,1,08:05:01,Test session 3,(0:00:10 session < 0:25:00 default),",
            ",2,08:35:01,Test session 4,(0:00:10 session < 0:25:00 default),",
        ]

    for a, b in zip(expect_lines, rows, strict=True):
        assert a == b


def test_export_timesheet_csv_for_date_range(app_data_with_four_test_sessions, monkeypatch):
    app_data, _ = app_data_with_four_test_sessions
    data_dir = str(app_data.data_path)
    app_data.set_running_csv_dir(data_dir)

    # Set the environment variable used by the AppData class to override its
    # data_path when initialized via the CLI.
    monkeypatch.setenv("POMODORABLE_TEST_DATA_DIR", data_dir)

    export_path = app_data.data_path
    args = ["--csv-date", "2024-01-02", "--end-date", "2024-01-03", "--timesheet"]

    runner = CliRunner()
    result = runner.invoke(cli, args)
    print(result.output)
    assert result.exit_code == 0

    csv_file = export_path / "ts-20240102-20240103.csv"
    assert csv_file.exists()

    rows = csv_file.read_text().strip().split("\n")
    assert len(rows) == 5  # 1 header + 4 session rows


@pytest.mark.parametrize("subdir_param", [None, "exported"])
def test_export_markdown_for_date(app_data_with_four_test_sessions, subdir_param, monkeypatch):
    app_data, _ = app_data_with_four_test_sessions
    data_dir = str(app_data.data_path)
    app_data.set_daily_md_dir(data_dir)

    # Set the environment variable used by the AppData class to override its
    # data_path when initialized via the CLI.
    monkeypatch.setenv("POMODORABLE_TEST_DATA_DIR", data_dir)

    if subdir_param:
        export_path = Path(data_dir) / subdir_param
        export_path.mkdir()
        args = ["--md-date", "2024-01-02", "--export-path", str(export_path)]
    else:
        export_path = app_data.data_path
        args = ["--md-date", "2024-01-02"]

    runner = CliRunner()
    result = runner.invoke(cli, args)
    print(result.output)
    assert result.exit_code == 0

    md_file = export_path / "2024-01-02.md"
    assert md_file.exists()

    lines = md_file.read_text().strip().split("\n")
    assert len(lines) == 10  # 1 header + 1 blank line + 8 data lines
    assert "Test session 1" in lines[2]
    assert "Test session 2" in lines[6]


def test_export_markdown_for_date_range(app_data_with_four_test_sessions, monkeypatch):
    app_data, _ = app_data_with_four_test_sessions
    data_dir = str(app_data.data_path)
    app_data.set_daily_md_dir(data_dir)

    # Set the environment variable used by the AppData class to override its
    # data_path when initialized via the CLI.
    monkeypatch.setenv("POMODORABLE_TEST_DATA_DIR", data_dir)

    export_path = app_data.data_path
    args = ["--md-date", "2024-01-02", "--end-date", "2024-01-04"]

    runner = CliRunner()
    result = runner.invoke(cli, args)
    print(result.output)
    assert result.exit_code == 0

    md_file_1 = export_path / "2024-01-02.md"
    assert md_file_1.exists()

    lines = md_file_1.read_text().strip().split("\n")
    assert len(lines) == 10  # 1 header + 1 blank line + 8 data lines
    assert "Test session 1" in lines[2]
    assert "Test session 2" in lines[6]

    md_file_2 = export_path / "2024-01-03.md"
    assert md_file_2.exists()
    lines = md_file_2.read_text().strip().split("\n")
    assert len(lines) == 10  # 1 header + 1 blank line + 8 data lines
    assert "Test session 3" in lines[2]
    assert "Test session 4" in lines[6]

    #  Should not make a file for date with no data.
    assert not (export_path / "2024-01-04.md").exists()


def test_export_csv_error_end_date_before_start_date(app_data_with_four_test_sessions):
    app_data, _ = app_data_with_four_test_sessions
    data_dir = str(app_data.data_path)
    app_data.set_daily_csv_dir(data_dir)
    app_data.set_running_csv_dir(data_dir)

    args = ["--csv-date", "2024-01-02", "--end-date", "2024-01-01"]

    runner = CliRunner()
    result = runner.invoke(cli, args)
    print(result.output)
    assert result.exit_code == 1
    assert "Start date must be before end date." in result.output


@pytest.mark.parametrize(("filter_arg", "expected_row_count"), [("X", 7), ("P", 5)])
def test_export_csv_for_date_with_filter(app_data_with_four_test_sessions, filter_arg, expected_row_count, monkeypatch):
    app_data, _ = app_data_with_four_test_sessions
    data_dir = str(app_data.data_path)
    app_data.set_daily_csv_dir(data_dir)

    # Set the environment variable used by the AppData class to override its
    # data_path when initialized via the CLI.
    monkeypatch.setenv("POMODORABLE_TEST_DATA_DIR", data_dir)

    export_path = app_data.data_path
    args = ["--csv-date", "2024-01-02", "--filters", filter_arg]

    runner = CliRunner()
    result = runner.invoke(cli, args)
    print(result.output)
    assert result.exit_code == 0

    csv_file = export_path / "2024-01-02.csv"
    assert csv_file.exists()

    rows = csv_file.read_text().strip().split("\n")
    assert len(rows) == expected_row_count
    # Filter X (there are no Stop actions):  1 header + 6 data rows
    # Filter P (there are 2 pause actions):  1 header + 4 data rows
