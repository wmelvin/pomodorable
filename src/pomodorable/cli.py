from importlib import metadata

import click

from pomodorable.app_data import AppData
from pomodorable.ui import PomodorableApp

DIST_NAME = "pomodorable"
MOD_VERSION = "cli-240302.1"


def get_app_version() -> str:
    try:
        return metadata.version(DIST_NAME)
    except metadata.PackageNotFoundError:
        return MOD_VERSION


def run() -> None:
    ui = PomodorableApp()
    ui.run()


def configure(daily_csv_dir, clear_daily_csv, daily_md_dir, clear_daily_md) -> bool:
    configured = False
    if any([daily_csv_dir, clear_daily_csv, daily_md_dir, clear_daily_md]):
        app_data = AppData()

    if daily_csv_dir:
        print(f"Setting daily CSV dir to {daily_csv_dir}")  # noqa: T201
        app_data.set_daily_csv_dir(daily_csv_dir)
        configured = True

    if clear_daily_csv:
        print("Clearing daily CSV dir")  # noqa: T201
        app_data.set_daily_csv_dir(None)
        configured = True

    if daily_md_dir:
        print(f"Setting daily Markdown dir to {daily_md_dir}")  # noqa: T201
        app_data.set_daily_md_dir(daily_md_dir)
        configured = True

    if clear_daily_md:
        print("Clearing daily Markdown dir")  # noqa: T201
        app_data.set_daily_md_dir(None)
        configured = True

    return configured


@click.command()
@click.version_option(get_app_version(), prog_name=DIST_NAME)
@click.option("--daily-csv-dir", default=None, help="Directory for daily CSV files.")
@click.option("--clear-daily-csv", is_flag=True, help="Clear the daily CSV directory.")
@click.option(
    "--daily-md-dir", default=None, help="Directory for daily Markdown files."
)
@click.option(
    "--clear-daily-md", is_flag=True, help="Clear the daily Markdown directory."
)
def cli(daily_csv_dir, clear_daily_csv, daily_md_dir, clear_daily_md) -> None:
    if configure(daily_csv_dir, clear_daily_csv, daily_md_dir, clear_daily_md):
        return
    run()


if __name__ == "__main__":
    cli()
