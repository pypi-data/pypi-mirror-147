import click
from pvx.env import (
    PVX_PYTHON_INSTALLATION_PATH,
    PY_BUILD_ARCHIVE_PATH,
    PY_BUILD_BIN_PATH,
    join_path,
)
from pvx.handler.py import PyInstallationStatus, pyHandler
from pvx.tools.rich_pvx_console import console

import pvx.commands.py_help as help


@click.command("install")
@click.argument(
    "version",
    metavar="<VERSION>",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="Remove before we install (if the version exists)",
)
def cli(version: str, force: bool):

    """Install the specified version of Python."""

    py_path = join_path(PVX_PYTHON_INSTALLATION_PATH, version)

    def _do_when_non_installed():
        _archives = pyHandler.archive(PY_BUILD_ARCHIVE_PATH, version)
        if len(_archives) == 0:
            console.text(
                f"{version} is an unarchived version. Try get the python archive that you can download."
            ).help(help.py_archive).print()

            return
        elif len(_archives) > 1:
            from rich.columns import Columns

            console.print(
                Columns(
                    _archives,
                    expand=True,
                    title="🐍 Found more than one version archive. Choose one:\n",
                )
            )
            return
        pyHandler.remove(py_path)
        res = pyHandler.install(PY_BUILD_BIN_PATH, version, py_path)
        if "done" == res:
            console.print(f"Done!\nPython version: {version} \npath: {py_path}")

        else:
            console.print(res)

    def _do_when_installed():
        console.text(f"{version} has been installed.").nlp().text(f"{py_path}").print()

    def _do_when_installed_broken():
        console.text(f"{version}  has been broken. Try reinstall:").help(
            help.py_install
        ).print()

    status = pyHandler.verify(py_path)

    if PyInstallationStatus.INSTALLED == status and force:
        _do_when_non_installed()
    if PyInstallationStatus.INSTALLED == status and not force:
        _do_when_installed()
    elif PyInstallationStatus.INSTALLED_BROKEN == status and force:
        _do_when_non_installed()
    elif PyInstallationStatus.INSTALLED_BROKEN == status and not force:
        _do_when_installed_broken()
    elif PyInstallationStatus.NON_INSTALLED == status:
        _do_when_non_installed()
