import os
import shutil
from pathlib import Path
from typing import List


def join_path(*paths) -> str:
    res = None
    for part in paths:
        if res is None:
            res = Path(part)
        else:
            res = res.joinpath(part)
    return str(res)


def clear_directory(path):
    """Clear all files and directories in a given directory"""
    for fn in os.listdir(path):
        fn = os.path.join(path, fn)
        if os.path.islink(fn) or os.path.isfile(fn):
            os.remove(fn)
        elif os.path.isdir(fn):
            shutil.rmtree(fn)


def remove_directory(path):
    """Remove a whole directory (This resembles `rm -rf path`)"""
    clear_directory(path)
    os.rmdir(path)


def glob(root_path: str, pattern: str, depth: int = 1) -> List[str]:
    """Get matching files under the giving path and depth with iteration"""
    match = []

    def _glob(root_path: str):
        return match.extend([str(dir) for dir in Path.glob(Path(root_path), pattern)])

    def _iter_glob(root_path: str):
        nonlocal depth
        depth -= 1
        for dir in Path(root_path).iterdir():
            _glob(str(dir))

        # Iteration stops when the depth is less than 1
        if depth > 1:
            _iter_glob(str(dir))

    if depth == 1 or depth < 1:
        _glob(root_path)
    else:
        _glob(root_path)
        _iter_glob(root_path)

    return match


def get_py_version(path: str):
    import subprocess

    return subprocess.check_output([path, "--version"]).decode().split(" ")[-1]


def get_random():
    import random
    import string

    random_str = random.sample(string.hexdigits, k=6)
    return "".join(random_str)
