from pathlib import Path

import click
from pvx.env import PVX_VENV_DIR_NAME_IN_PROJECT, PVX_VENV_IN_PROJECT, PVX_VENV_PATH
from pvx.handler.venv import richVenvTable, venvHandler
from pvx.tools.rich_pvx_console import console, pvx_hint_color

import pvx.commands.venv_help as help


@click.command("list")
def cli():
    """List all existing virtual environments. [sea_green3]Highlight activate[/]."""

    if PVX_VENV_IN_PROJECT:
        if not Path(PVX_VENV_PATH).exists():
            console.print(
                f"[{pvx_hint_color}]{PVX_VENV_DIR_NAME_IN_PROJECT}[/] folder is not found.You should execute commands in the project root directory."
            )
            return

    if PVX_VENV_IN_PROJECT:
        venvs = venvHandler.list(PVX_VENV_PATH)
    else:
        # print(str(Path().cwd().joinpath(PVX_VENV_DIR_NAME_IN_PROJECT).joinpath(".pvx")))
        venvs = venvHandler.list_external(
            str(Path().cwd().joinpath(PVX_VENV_DIR_NAME_IN_PROJECT)), ".pvx"
        )

    if len(venvs) > 0:
        console.print(richVenvTable(venvs), pvx_emoji=False)
    else:
        console.text("Not find virtual environments. Try creating a new one:").help(
            help.venvpy_new
        ).print()
