import sys
from importlib import metadata
from pathlib import Path

import click

from pomodorable.app_data import AppData
from pomodorable.app_utils import get_date_from_str
from pomodorable.ui import PomodorableApp

DIST_NAME = "pomodorable"
MOD_VERSION = "cli-240328.1"


def get_app_version() -> str:
    try:
        return metadata.version(DIST_NAME)
    except metadata.PackageNotFoundError:
        return MOD_VERSION


def handled_option(csv_date, md_date, export_path) -> bool:
    """Handle the command-line options for exporting CSV or Markdown files.
    If there are errors in the options, print an error message and exit.
    If options are handled, return True; otherwise, return False.
    """
    if csv_date is None and md_date is None:
        if export_path is not None:
            sys.stderr.write(
                "\n--export-path option requires either --csv-date or "
                "--md-date option.\n"
            )
            sys.exit(1)
        return False

    if export_path is not None:
        export_path = Path(export_path)
        if not export_path.exists():
            sys.stderr.write(f"\nInvalid path: {export_path}\n")
            sys.exit(1)

    if csv_date is not None:
        csv_date = get_date_from_str(csv_date)
        if csv_date is None:
            sys.stderr.write(f"\nInvalid date: {csv_date}\n")
            sys.exit(1)

    if md_date is not None:
        md_date = get_date_from_str(md_date)
        if md_date is None:
            sys.stderr.write(f"\nInvalid date: {md_date}\n")
            sys.exit(1)

    app_data = AppData()

    if csv_date is not None:
        app_data.cli_export_daily_csv(csv_date, export_path)

    if md_date is not None:
        app_data.cli_export_daily_markdown(md_date, export_path)

    return True


def run() -> None:
    ui = PomodorableApp()
    ui.run()


CLICK_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.version_option(get_app_version(), prog_name=DIST_NAME)
@click.option(
    "--csv-date",
    default=None,
    help="Export a Daily CSV file for a given date (provide the date as YYYY-MM-DD "
    "or YY-MM-DD). If a 'Daily CSV Folder' is not configured, then you must provide "
    "the --export-path option as well. Existing files are not overwritten.",
)
@click.option(
    "--md-date",
    default=None,
    help="Export a Daily Markdown file for a given date (provide the date as "
    "YYYY-MM-DD or YY-MM-DD). If a 'Daily Markdown Folder' is not configured, "
    "then you must provide the --export-path option as well. Existing files "
    "are not overwritten.",
)
@click.option(
    "--export-path",
    default=None,
    help="Path to export a Daily CSV or Markdown file. "
    "This option is required if a 'Daily CSV Folder' or 'Daily Markdown Folder' is "
    "not configured, or you want the files written to a different location.",
)
def cli(csv_date, md_date, export_path) -> None:
    """Handle any command-line options or run the TUI."""
    if handled_option(csv_date, md_date, export_path):
        return
    run()


if __name__ == "__main__":
    cli()
