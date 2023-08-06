import shlex
import subprocess
from os import linesep, sep
from time import sleep
from typing import List

from rich.status import Status
from rich.table import Table
from pvx.tools import utils


class Venv(object):
    def __init__(self, pyvenv_config_path: str) -> None:
        self.config_path = pyvenv_config_path

        self.config_context = self._reade_pyvenv()
        self.path = self._venv_path()
        self.version = self.config_context.get("version")
        self.prompt = self.config_context.get("prompt")
        self.create_by = self.config_context.get("home")
        self.is_activate = self._is_activate()

    def as_list(self) -> List[str]:
        return [
            self.prompt or "Non",
            self.version,
            self.path,
            self.create_by,
            str(self.is_activate),
        ]

    @classmethod
    def headers(cls) -> List[str]:
        return ["Id", "Prompt", "Version", "Path", "Create_by"]

    @classmethod
    def title(cls):
        return "Venv List ⭐"

    @classmethod
    def rich_table(cls, venvs: List["Venv"]) -> Table:
        from rich import box

        venvs.sort(key=lambda x: x.is_activate, reverse=True)

        my_table = Table(*cls.headers(), title=cls.title(), box=box.ASCII)
        for id, _venv in enumerate(venvs, start=1):
            if _venv.is_activate:
                style = "sea_green3 bold"
            else:
                style = None

            my_table.add_row(
                str(id),
                _venv.prompt or "Non",
                _venv.version,
                _venv.path,
                _venv.create_by,
                style=style,
            )
        return my_table

    def _is_activate(self):
        from env import variable

        if variable("VIRTUAL_ENV") and variable("VIRTUAL_ENV") == self.path:
            return True
        return False

    # read config
    def _reade_pyvenv(self):
        with open(self.config_path, "r") as cf:
            context = {}
            for line in cf.readlines():
                line_kv = [s.strip() for s in line.replace(linesep, "").split("=")]
                context[line_kv[0]] = line_kv[1].replace("'", "").replace('"', "")
            return context

    def _venv_path(self) -> str:
        return sep.join(self.config_path.split(sep)[:-1])


class VenvHandler:
    """
    Virtual Environment Commands.
    """

    def new(self, py_path: str, prompt: str, output: str, params: List[str]):
        venv_final_path = utils.join_path(output, prompt)

        cmd = (
            f"{py_path} -m venv "
            + " ".join(params)
            + f" --prompt {prompt} "
            + venv_final_path
        )

        p = subprocess.Popen(shlex.split(cmd))

        with Status(
            "[bold blue]Preparing the virtual environment...", spinner="moon"
        ) as status:
            while p.poll() is None:
                sleep(0.5)
            if p.poll() != 0:
                stdout, stderr = p.communicate()
                return stderr.decode()
            else:
                return "done"

    def activate(self, venv_path: str, prompt: str):
        """Activate virtual environment"""
        from tools.shell import ShellType, shell

        def _activate_script_suffix() -> str:
            if shell.name == ShellType.CSH:
                return ".csh"
            elif shell.name == ShellType.FISH:
                return ".fish"
            return ""

        venv_activate_path = utils.join_path(
            venv_path,
            prompt,
            "bin",
            "activate",
            _activate_script_suffix(),
        )

        shell.venv_shell(venv_activate_path)

    def list(self, venv_path: str) -> List[Venv]:
        """List all installed virtual environment and markup the activated."""

        # get all virtual environments config path
        venv_config_paths = utils.glob(venv_path, "pyvenv.cfg", depth=2)
        return [Venv(config_path) for config_path in venv_config_paths]

    def list_external(self, record_path: str, record_file_name: str) -> List[Venv]:
        """Lists all virtual environments installed on external paths and marks those that are active."""

        venv_config_paths = []

        with open(utils.join_path(record_path, record_file_name), "r") as f:
            venv_path = f.readlines()
            print(venv_path)
            # get all virtual environments config path
            for path in venv_path:
                venv_config_paths.extend(
                    utils.glob(path.replace(linesep, ""), "pyvenv.cfg")
                )
        return [Venv(config_path) for config_path in venv_config_paths]

    def remove(self, venv_path: str, prompt: str):
        """List all installed virtual environment and markup the activated"""

        utils.remove_directory(utils.join_path(venv_path, prompt))


venvHandler = VenvHandler()

richVenvTable = Venv.rich_table
