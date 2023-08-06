import os
from typing import Optional
from pvx.tools.utils import join_path


def strtobool(val: Optional[str]) -> bool:

    if val is None:
        return False
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        return False


def variable(key: str) -> Optional[str]:
    """Not sure if the environment variable exists"""
    return os.getenv(key)


# optional
PVX_ROOT_PATH = join_path(os.environ["HOME"], ".pvx")

# optional
PVX_PYTHON_INSTALLATION_PATH = variable("PVX_PYTHON_INSTALLATION_PATH") or join_path(
    PVX_ROOT_PATH, "versions"
)

# optional
PVX_VENV_EXTERNAL_PATH = variable("PVX_VENV_EXTERNAL_PATH") or join_path(
    PVX_ROOT_PATH, "venv"
)

# optional
PVX_VENV_DIR_NAME_IN_PROJECT = variable("PVX_VENV_DIR_NAME_IN_PROJECT") or ".venv"

# optional
PVX_VENV_IN_PROJECT = (
    True
    if variable("PVX_VENV_IN_PROJECT") is None
    else strtobool(variable("PVX_VENV_IN_PROJECT"))
)

# If you have not executed `install.sh` please make sure to set it, usually `~/.pyenv/plugins/python-build`, otherwise it is optional.
# The installation of Python is provided by the plugin "python-build" of "pyenv".
# https://github.com/pyenv/pyenv/tree/master/plugins/python-build
# 👍 Thanks !!! 👏
PVX_PY_BUILD_HOME = (
    variable("PVX_PY_BUILD_PATH") or os.environ["HOME"] + "/.pyenv/plugins/python-build"
)

PY_BUILD_BIN_PATH = join_path(PVX_PY_BUILD_HOME, "bin/python-build")

PY_BUILD_ARCHIVE_PATH = join_path(PVX_PY_BUILD_HOME, "share/python-build")


def get_venv_path() -> str:
    if PVX_VENV_IN_PROJECT:
        return join_path(os.environ["PWD"], PVX_VENV_DIR_NAME_IN_PROJECT)
    else:
        # FIXME how to pair with current project
        return PVX_VENV_EXTERNAL_PATH


PVX_VENV_PATH = get_venv_path()
