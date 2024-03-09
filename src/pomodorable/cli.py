from importlib import metadata

import click

from pomodorable.ui import PomodorableApp

DIST_NAME = "pomodorable"
MOD_VERSION = "cli-240307.1"


def get_app_version() -> str:
    try:
        return metadata.version(DIST_NAME)
    except metadata.PackageNotFoundError:
        return MOD_VERSION


def handled_option(csv_date) -> bool:
    if csv_date is not None:
        print(f"{csv_date =}")  # noqa: T201
        # TODO: Handle it.
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
