# 🐍 pvx
Python version &amp; venv management (maybe more ...)

## 🤪 What can pvx do ?

![pvx-help](./asset/pvx-help.png)

## 📦 Install

- Use pipx (recommend)

    ```bash
    pipx install pvx
    ```

- Use pip

    ```bash
    pip install pvx
    ```

## 🔧 Usage

- List  version number that you can download.

    ```bash
    pvx py archive 

    # If you want to filter it, do this
    pvx py archive 3.10
    ```

- Install.

    ```bash
    pvx py insetall 3.10.4
    ```

- List versions of installed.

    ```bash
    pvx py list
    ```

- Remove the specified version of Python.

    ```bash
    pvx py remove 3.10.4
    ```

- Create a virtual environment (pvx use [Python Venv](https://docs.python.org/3/tutorial/venv.html))

    ```bash
    # All default (current python and default venv prompt)
    pvx venv new

    # Specify the version (which install by pvx)
    pvx venv new 3.10.4

    # Use existing Python
    pvx venv new ~/.pyenv/versions/3.10.4/bin/python

    # Use venv's parameters, such as specifying prompt
    pvx venv new 3.10.4 --prompt venv_prompt_name

    # Use current python and venv's parameters
    pvx venv new --prompt venv_prompt_name
    ```

- List all virtual environments

    ```bash
    # You'll see a table , highlight the activate one.
    pvx venv list
    ```

- Activate virtual environment with `PROMPT`

    ```bash
    # use `pvx venv list` to show prompt
    pvx venv activate prompt_name
    ```

- Remove virtual environment with `PROMPT`

    ```bash
    # use `pvx venv list` to show prompt
    pvx venv remove prompt_name
    ```

## 🌟 Extend functionality

If you want to extend commands, be familiar with the following points.

1. The folder where the `pvx.py` file resides is the `root`.
2. `root/commands` is the folder where the `.py` command scripts are stored.
3. If `filenamed` is true, use the file name command, otherwise use the argument to `@click.command`.
        - The `.py` files are named `pvx_{group}_{command}.py`.For example: `pvx_py_install.py`, which means we can call it with `pvx py install`.
4. `.py` file must have a method called `cli` and decorated with `@click.command` .

## 👻 Thanks

- [python-build (pyenv's plugin)](https://github.com/pyenv/pyenv/tree/master/plugins/python-build), which pvx depend to install different versions of Python
- [rich](https://github.com/Textualize/rich), a Python library for rich text and beautiful formatting in the terminal.
- [click](https://github.com/pallets/click), a python composable command line interface toolkit
