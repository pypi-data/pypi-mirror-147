from pathlib import Path

import click
from pvx.env import PVX_VENV_DIR_NAME_IN_PROJECT, PVX_VENV_IN_PROJECT, PVX_VENV_PATH
from pvx.handler.venv import venvHandler
from pvx.tools.rich_pvx_console import console, pvx_hint_color


@click.command("activate")
@click.argument("prompt", metavar="<PROMPT>")
def cli(prompt: str):
    """Activate a existing virtual environments."""

    if PVX_VENV_IN_PROJECT:
        if not Path(PVX_VENV_PATH).exists():
            console.print(
                f"[{pvx_hint_color}]{PVX_VENV_DIR_NAME_IN_PROJECT}[/] folder is not found.You should execute commands in the project root directory."
            )
            return

    if not Path(PVX_VENV_PATH).joinpath(prompt).exists():
        console.print(
            f"[{pvx_hint_color}]{prompt}[/] virtual environment does not exist ~"
        )
        return

    venvHandler.activate(PVX_VENV_PATH, prompt)
