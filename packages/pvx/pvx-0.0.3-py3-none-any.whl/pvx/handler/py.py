import shlex
import subprocess
from enum import Enum
from pathlib import Path
from time import sleep
from typing import List, Tuple

from pvx.tools import utils


class PyInstallationStatus(Enum):
    NON_INSTALLED = 0
    INSTALLED = 1
    INSTALLED_BROKEN = 2


class PyHandler:
    """Python version handler"""

    def verify(self, py_path: str) -> PyInstallationStatus:
        """Verify the installation of the specified version of Python"""
        if Path(py_path).is_dir():
            if (
                Path(py_path).joinpath("bin", "python").is_symlink()
                or Path(py_path).joinpath("bin", "python3").is_symlink()
            ):
                return PyInstallationStatus.INSTALLED
            else:
                return PyInstallationStatus.INSTALLED_BROKEN
        else:
            return PyInstallationStatus.NON_INSTALLED

    def install(self, py_build_path: str, version: str, install_path: str):
        if not Path(install_path).exists():
            Path(install_path).mkdir(mode=0o755)

        if not Path(install_path).joinpath(version).exists():
            Path(install_path).joinpath(version).mkdir(mode=0o755)

        cmd = f"{py_build_path} {version} {install_path}"
        p = subprocess.Popen(
            shlex.split(cmd),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        from rich.status import Status

        with Status(f"[bold blue]Installing {version} ...", spinner="moon") as status:
            while p.poll() is None:
                sleep(1)
            if p.poll() != 0:
                stdout, stderr = p.communicate()
                return stderr.decode()
            else:
                return "done"

    def archive(self, archive_path: str, pattern: str = None) -> List[str]:
        """Python archive, which you can download by version number"""

        archives = [item.name for item in Path(archive_path).iterdir()]
        import re

        res = []
        if "" == pattern or pattern is not None:
            for _archive in archives:
                x = re.match(pattern, _archive)
                if x is not None:
                    res.append(x.string)
        else:
            res = archives

        res.sort(key=lambda x: x)
        return res

    def list(self, install_path: str) -> Tuple[List[str], List[str]]:
        """Gets a list of installed Python versions"""

        installed = []
        installed_broken = []
        for dir in Path(install_path).iterdir():

            verify_res = self.verify(str(dir))

            if PyInstallationStatus.INSTALLED == verify_res:
                installed.append(dir.name)
            elif PyInstallationStatus.INSTALLED_BROKEN == verify_res:
                installed_broken.append(dir.name)
        return installed, installed_broken

    def remove(self, py_path: str):
        if Path(py_path).exists():
            utils.remove_directory(py_path)


pyHandler = PyHandler()
