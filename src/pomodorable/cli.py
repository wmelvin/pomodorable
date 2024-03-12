import sys
from importlib import metadata

import click

from pomodorable.app_data import AppData
from pomodorable.app_utils import get_date_from_str
from pomodorable.ui import PomodorableApp

DIST_NAME = "pomodorable"
MOD_VERSION = "cli-240312.1"


def get_app_version() -> str:
    try:
        return metadata.version(DIST_NAME)
    except metadata.PackageNotFoundError:
        return MOD_VERSION


def handled_option(csv_date) -> bool:
    if csv_date is not None:
        date_val = get_date_from_str(csv_date)
        if date_val is None:
            sys.stderr.write(f"\nInvalid date: {csv_date}\n")
            sys.exit(1)

        app_data = AppData()
        app_data.export_daily_csv(date_val)
        return True
    return False


def run() -> None:
    ui = PomodorableApp()
    ui.run()


@click.command()
@click.version_option(get_app_version(), prog_name=DIST_NAME)
@click.option(
    "--csv-date", default=None, help="Date to export as YYYY-MM-DD or YY-MM-DD"
)
def cli(csv_date) -> None:
    if handled_option(csv_date):
        return
    run()


if __name__ == "__main__":
    cli()
