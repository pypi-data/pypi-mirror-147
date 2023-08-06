import click
from pvx.env import PVX_PYTHON_INSTALLATION_PATH
from pvx.handler.py import PyInstallationStatus, pyHandler
from rich.prompt import Confirm
from pvx.tools.rich_pvx_console import console, pvx_hint_color
from pvx.tools.utils import join_path

import pvx.commands.py_help as help


@click.command("remove")
@click.argument("version", metavar="<VERSION>")
def cli(version: str):
    """Remove the specified version of Python."""
    py_path = join_path(PVX_PYTHON_INSTALLATION_PATH, version)
    if PyInstallationStatus.NON_INSTALLED != pyHandler.verify(py_path):
        if Confirm.ask("Are you sure?"):
            pyHandler.remove(py_path)
            console.print(f"Done! [{pvx_hint_color}]{py_path}[/] has been uninstalled")
    else:
        console.text(
            f"[{pvx_hint_color}]{version}[/] is not found! You can print installed versions. Try:"
        ).help(help.py_list).print()
