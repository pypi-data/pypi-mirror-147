import os

import click
from pvx.env import PY_BUILD_ARCHIVE_PATH
from pvx.handler.py import pyHandler
from pvx.tools.rich_pvx_console import PvxConsole, console

import pvx.commands.py_help as help


@click.command("archive")
@click.argument("version", metavar="<VERSION>", required=False)
def cli(version: str):
    """A list that you can download by version number."""

    res = pyHandler.archive(PY_BUILD_ARCHIVE_PATH, version)

    if len(res) > 0:
        from rich.columns import Columns

        title = (
            "🐍 Similar results" + os.linesep
            if version
            else "🐍 If the results are too much, try "
            + f"[medium_spring_green]{help.py_archive}[/medium_spring_green]"
            + " to get similar results."
            + os.linesep
        )
        PvxConsole.pager(
            Columns(res, expand=True, title=title),
        )
    else:
        console.text(f"Nothing found. Try:").help(help.py_archive).print()
