from pathlib import Path

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


def test_export_csv_for_date(app_data_with_four_test_sessions, monkeypatch):
    app_data, _ = app_data_with_four_test_sessions
    data_dir = str(app_data.data_path)
    app_data.set_daily_csv_dir(data_dir)
    monkeypatch.setenv("POMODORABLE_TEST_DATA_DIR", data_dir)

    runner = CliRunner()
    result = runner.invoke(cli, ["--csv-date", "2024-01-02"])
    assert result.exit_code == 0
    csv_file = Path(app_data.config.daily_csv_dir) / "2024-01-02.csv"
    assert csv_file.exists()
    rows = csv_file.read_text().strip().split("\n")
    assert len(rows) == 7  # 1 header + 6 data rows
