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
def test_export_csv_for_date(
    app_data_with_four_test_sessions, subdir_param, monkeypatch
):
    app_data, _ = app_data_with_four_test_sessions
    data_dir = str(app_data.data_path)
    app_data.set_daily_csv_dir(data_dir)

    # Set the environment variable used by the AppData class to override its
    # data_path when initialized via the CLI.
    monkeypatch.setenv("POMODORABLE_TEST_DATA_DIR", data_dir)

    if subdir_param:
        export_path = Path(data_dir) / subdir_param
        export_path.mkdir()
        args = ["--csv-date", "2024-01-02", "--export-path", str(export_path)]
    else:
        export_path = app_data.data_path
        args = ["--csv-date", "2024-01-02"]

    runner = CliRunner()
    result = runner.invoke(cli, args)
    assert result.exit_code == 0

    csv_file = export_path / "2024-01-02.csv"
    assert csv_file.exists()

    rows = csv_file.read_text().strip().split("\n")
    assert len(rows) == 7  # 1 header + 6 data rows


@pytest.mark.parametrize("subdir_param", [None, "exported"])
def test_export_markdown_for_date(
    app_data_with_four_test_sessions, subdir_param, monkeypatch
):
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
    assert result.exit_code == 0

    md_file = export_path / "2024-01-02.md"
    assert md_file.exists()

    lines = md_file.read_text().strip().split("\n")
    assert len(lines) == 10  # 1 header + 1 blank line + 8 data lines
    assert "Test session 1" in lines[2]
    assert "Test session 2" in lines[6]
