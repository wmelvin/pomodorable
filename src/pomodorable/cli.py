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


def run() -> None:
    ui = PomodorableApp()
    ui.run()


@click.command()
@click.version_option(get_app_version(), prog_name=DIST_NAME)
def cli() -> None:
    run()


if __name__ == "__main__":
    cli()
