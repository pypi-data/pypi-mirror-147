from enum import Enum
from os import environ
from typing import Tuple

import pexpect

from pvx.tools.terminal import Terminal


class ShellType(Enum):
    BASH = "bash"
    ZSH = "zsh"
    FISH = "fish"
    CSH = "csh"
    TCSH = "tsch"


class Shell:
    def __init__(self) -> None:
        self._executable = environ["SHELL"]
        self._name = ShellType(self._executable.split("/")[-1].lower())

    @property
    def executable(self):
        return self._executable

    @property
    def name(self):
        return self._name

    def venv_shell(
        self, venv_activate_path: str, terminal_size: Tuple[int, int] = Terminal.size()
    ):
        c = pexpect.spawn(self._executable, ["-i"], dimensions=terminal_size)
        if self._name == ShellType.ZSH:
            c.setecho(False)
        c.sendline(f"{self._source_cammand()} {venv_activate_path}")
        c.interact(escape_character=None)
        c.close()

    def _source_cammand(self):
        if self._name in (ShellType.FISH, ShellType.CSH, ShellType.TCSH):
            return "source"
        return "."


shell = Shell()
