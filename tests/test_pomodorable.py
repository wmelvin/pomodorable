from click.testing import CliRunner

from pomodorable.cli import cli
from pomodorable.ui import PomodorableApp


async def test_app_is_created():
    app = PomodorableApp()
    async with app.run_test() as pilot:
        footer = pilot.app.query_one("Footer")
        assert footer


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
    assert "Options:" in result.output
    assert "--daily-csv-dir" in result.output
    assert "--clear-daily-csv" in result.output
    assert "--daily-md-dir" in result.output
    assert "--clear-daily-md" in result.output
    assert "Show this message and exit." in result.output
