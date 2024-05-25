import sys
from importlib import metadata
from pathlib import Path

import click

from pomodorable.app_data import AppData
from pomodorable.app_utils import get_date_from_str
from pomodorable.ui import PomodorableApp

DIST_NAME = "pomodorable"
MOD_VERSION = "cli-240509.1"


def get_app_version() -> str:
    try:
        return metadata.version(DIST_NAME)
    except metadata.PackageNotFoundError:
        return MOD_VERSION


def handled_option(csv_date, md_date, end_date, export_path, filters) -> bool:
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

    if end_date is not None:
        end_date = get_date_from_str(end_date)
        if end_date is None:
            sys.stderr.write(f"\nInvalid date: {end_date}\n")
            sys.exit(1)

    if csv_date is not None:
        csv_date = get_date_from_str(csv_date)
        if csv_date is None:
            sys.stderr.write(f"\nInvalid date: {csv_date}\n")
            sys.exit(1)

    if csv_date is not None and end_date is not None and csv_date > end_date:
        sys.stderr.write("\nStart date must be before end date.\n")
        sys.exit(1)

    if md_date is not None:
        md_date = get_date_from_str(md_date)
        if md_date is None:
            sys.stderr.write(f"\nInvalid date: {md_date}\n")
            sys.exit(1)

    app_data = AppData()

    filters = "" if filters is None else filters.upper()

    if csv_date is not None:
        if end_date is not None:
            app_data.cli_export_date_range_csv(csv_date, end_date, filters, export_path)
        else:
            app_data.cli_export_daily_csv(csv_date, filters, export_path)

    if md_date is not None:
        app_data.cli_export_daily_markdown(md_date, filters, export_path)

    return True


def run(enable_screenshots: bool, enable_testkey: bool) -> None:
    ui = PomodorableApp(
        enable_screenshots=enable_screenshots, enable_testkey=enable_testkey
    )
    ui.run()


CLICK_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.version_option(get_app_version(), prog_name=DIST_NAME)
@click.option(
    "--csv-date",
    default=None,
    help="Export a Daily CSV file for a given date (provide the date as YYYY-MM-DD "
    "or YY-MM-DD). If a 'Daily CSV Folder' is not configured, then you must provide "
    "the --export-path option as well. Existing files are not overwritten. "
    "Exits when finished.",
)
@click.option(
    "--md-date",
    default=None,
    help="Export a Daily Markdown file for a given date (provide the date as "
    "YYYY-MM-DD or YY-MM-DD). If a 'Daily Markdown Folder' is not configured, "
    "then you must provide the --export-path option as well. Existing files "
    "are not overwritten. Exits when finished.",
)
@click.option(
    "--end-date",
    default=None,
    help="Export a range of sessions from the start date to the end date "
    "(provide the dates as YYYY-MM-DD or YY-MM-DD). This option is only valid "
    "with the --csv-date or --md-date option.",
)
@click.option(
    "--export-path",
    default=None,
    help="Path to export a Daily CSV or Markdown file. "
    "This option is required if a 'Daily CSV Folder' or 'Daily Markdown Folder' is "
    "not configured, or you want the files written to a different location.",
)
@click.option(
    "--filters",
    default="",
    help="Filter specified actions from exported CSV data. "
    "The filter is specified as a string with no spaces, where each character "
    "represents a type of action to exclude. The characters are: "
    "F (Finish), P (Pause - all), R (pause w/o Reason), and X (Stop).",
)
@click.option(
    "--ctrl-s",
    is_flag=True,
    default=False,
    help="Enable [Ctrl]+[s] for saving SVG screenshots in the app. "
    "Screenshots are saved to the Desktop.",
)
@click.option(
    "--ctrl-t",
    is_flag=True,
    default=False,
    help="Enable [Ctrl]+[t] to run manual testing functions.",
)
def cli(csv_date, md_date, end_date, export_path, filters, ctrl_s, ctrl_t) -> None:
    """Handle command-line options or run the Textual User Interface."""
    if handled_option(csv_date, md_date, end_date, export_path, filters):
        return
    run(enable_screenshots=ctrl_s, enable_testkey=ctrl_t)


if __name__ == "__main__":
    cli()
