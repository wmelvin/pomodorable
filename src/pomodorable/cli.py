from importlib import metadata

import click

from pomodorable.ui import PomodorableApp

DIST_NAME = "pomodorable"
MOD_VERSION = "cli-240302.1"


def get_app_version() -> str:
    try:
        return metadata.version(DIST_NAME)
    except metadata.PackageNotFoundError:
        return MOD_VERSION


@click.command()
@click.version_option(get_app_version())
def run() -> None:
    ui = PomodorableApp()
    ui.run()


if __name__ == "__main__":
    print(f"\n{get_app_version() = }")  # noqa: T201
