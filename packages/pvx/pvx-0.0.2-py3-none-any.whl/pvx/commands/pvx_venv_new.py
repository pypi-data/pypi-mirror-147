import os
import sys
from pathlib import Path

import click
from pvx.env import (
    PVX_PYTHON_INSTALLATION_PATH,
    PVX_VENV_PATH,
    PVX_VENV_IN_PROJECT,
    PVX_VENV_DIR_NAME_IN_PROJECT,
)
from pvx.handler.py import pyHandler
from pvx.handler.venv import venvHandler
from pvx.tools.rich_pvx_console import console, pvx_hint_color
from pvx.tools.utils import join_path

from pvx.commands import py_help


def get_venv_dir_name(py_path) -> str:
    """Name of the virtual environment directory.(It is also the default prompt for the virtual environment)"""
    from os import environ

    from tools.utils import get_py_version, get_random

    return "-".join([Path(environ["PWD"]).name, get_random(), get_py_version(py_path)])


def is_support_version(py_path: str, major: int, minor: int) -> bool:
    from tools.utils import get_py_version

    current = get_py_version(py_path).split(".")
    if major >= current[0] and minor >= current[1]:
        return True
    return False


@click.command("new")
@click.argument(
    "version_or_path",
    metavar="<VERSION|PATH>",
    default="",
)
@click.option(
    "--prompt",
    metavar="[PROMPT]",
    default=None,
    help="Provides an alternative prompt prefix for this environment.(optional, pvx sets the prompt.)",
)
@click.option(
    "--system-site-packages",
    is_flag=True,
    default=False,
    help="Give the virtual environment access to the system site-packages dir.(Consistent with the python venv option)",
)
@click.option(
    "--symlinks",
    is_flag=True,
    default=False,
    help="Try to use symlinks rather than copies, when symlinks are not the default for the platform.(Consistent with the python venv option)",
)
@click.option(
    "--copies",
    is_flag=True,
    default=False,
    help="Try to use copies rather than symlinks, even when symlinks are the default for the platform.(Consistent with the python venv option)",
)
@click.option(
    "--clear",
    is_flag=True,
    default=False,
    help="Delete the contents of the environment directory if it already exists, before environment creation.(Consistent with the python venv option)",
)
@click.option(
    "--upgrade",
    is_flag=True,
    default=False,
    help="Upgrade the environment directory to use this version of Python, assuming Python has been upgraded in-place.(Consistent with the python venv option)",
)
@click.option(
    "--without-pip",
    is_flag=True,
    default=False,
    help="Skips installing or upgrading pip in the virtual environment. (pip is bootstrapped by default)(Consistent with the python venv option)",
)
@click.option(
    "--upgrade-deps",
    is_flag=True,
    default=False,
    help="Skips installing or upgrading pip in the virtual environment. (pip is bootstrapped by default)(Consistent with the python venv option)",
)
def cli(
    version_or_path: str,
    prompt: str,
    system_site_packages: bool,
    symlinks: bool,
    copies: bool,
    clear: bool,
    upgrade: bool,
    without_pip: bool,
    upgrade_deps: bool,
):
    """Create a new venv by the specified version of Python or full path to Python executable, default current executable.(Python >= 3.6. Python >= 3.10 is best if you use ZSH and PK10 theme.($VIRTUAL_ENV_PROMPT is required))"""

    if Path(version_or_path).is_absolute():
        # mean using python abs path
        path = version_or_path
    elif "" == version_or_path or "system" == version_or_path:
        # mean using current python , usually /usr/bin/python3 or {venv_path}/bin/python3
        path = sys.executable
    else:
        # mean use python install by pvx or other(eg. pyenv)
        # check whether it has been installed
        if version_or_path not in pyHandler.list(PVX_PYTHON_INSTALLATION_PATH)[0]:
            console.text(
                f"[{pvx_hint_color}]{version_or_path}[/] is not installed! Try install:"
            ).help(py_help.py_install).nl().print()
            console.text(
                "Also you can get the python archive that you can download. Try:"
            ).help(py_help.py_archive).print()
            return
        path = join_path(PVX_PYTHON_INSTALLATION_PATH, version_or_path, "bin/python")

    prompt = prompt if prompt is not None else get_venv_dir_name(path)

    params = []
    if system_site_packages:
        params.append(f"--system-site-packages")
    if symlinks:
        params.append(f"--symlinks")
    if copies:
        params.append("--copies")
    if clear:
        params.append("--clear")
    if upgrade:
        params.append("--upgrade")
    if without_pip:
        params.append("--without-pip")
    if upgrade_deps and is_support_version(path, 3, 9):
        params.append("--upgrade-deps")

    res = venvHandler.new(path, prompt, PVX_VENV_PATH, params)

    if "done" == res:
        if not PVX_VENV_IN_PROJECT:
            _venv_record_path = Path().cwd().joinpath(PVX_VENV_DIR_NAME_IN_PROJECT)
            if not _venv_record_path.exists():
                _venv_record_path.mkdir()

            with open(str(_venv_record_path.joinpath(".pvx")), "a") as f:
                f.write(f"{join_path(PVX_VENV_PATH,prompt)}{os.linesep}")
        console.print("Complete ~")
    else:
        console.print(res)
