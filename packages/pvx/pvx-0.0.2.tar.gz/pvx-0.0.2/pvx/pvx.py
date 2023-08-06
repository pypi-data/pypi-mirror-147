import os
from typing import Dict

import click
from click import Context, Parameter
from click.formatting import HelpFormatter
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme


class OptionHighlighter(RegexHighlighter):
    highlights = [
        r"(?P<switch>^\-[\w\-]+)",
        r"(?P<option>^\-\-[\w\-]+)",
    ]


highlighter = OptionHighlighter()
console = Console(
    theme=Theme(
        {
            "option": "bold cyan",
            "switch": "bold green",
        }
    ),
    highlighter=highlighter,
)


class PVXCommands(click.Group):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:

        # PVX help title
        console.print("[bold sea_green3]PVX Cli[/] 🐍\n", justify="center")
        # PVX help
        console.print(
            self.help if self.help is None else self.help + "\n", justify="center"
        )
        # PVX usage
        console.print(self.get_usage(ctx) + "\n")
        # PVX optinon
        options_table = Table(highlight=True, box=None, show_header=False)

        for param in self.get_params(ctx):
            get_rich_option(options_table, param, param.get_help_record(ctx))
        console.print(
            Panel(
                options_table,
                border_style="dim",
                title="Options",
                title_align="left",
            )
        )
        # PVX commands
        commands_table = Table(highlight=True, box=None, show_header=False)
        for k, v in self.commands.items():
            commands_table.add_row(k, v.help)

        if commands_table.row_count > 0:
            console.print(
                Panel(
                    commands_table,
                    border_style="dim",
                    title="Commands",
                    title_align="left",
                )
            )


class GroupCommands(click.Group):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:

        # PVX help title
        console.print("[bold sea_green3]PVX Cli[/] 🐍\n", justify="center")
        # PVX help
        console.print(
            self.help if self.help is None else self.help + "\n", justify="center"
        )

        # remove group help option
        ctx.help_option_names.remove("--help")

        # get group options
        options = self.get_params(ctx)
        if len(options) > 0:
            options_table = Table(highlight=True, box=None, show_header=False)

            for param in self.get_params(ctx):
                get_rich_option(options_table, param, param.get_help_record(ctx))
            console.print(
                Panel(
                    options_table,
                    border_style="dim",
                    title="Options",
                    title_align="left",
                )
            )
        # PVX usage
        console.print(" ".join([ctx.command_path, "COMMAND", "[OPTIONS]", "[ARGS]", "\n"]))

        # commands and options
        from rich import box

        table = Table(
            highlight=True,
            box=box.MINIMAL,
            show_header=False,
            leading=1,
            expand=True,
        )

        for k, command in self.commands.items():
            command_options_table = Table(
                highlight=True,
                box=None,
                show_header=False,
                title="[sea_green3]Options[/]",
                padding=(0, 1, 1, 1),
            )

            command_args = []
            for param in command.params:
                if param.get_help_record(ctx) is not None:
                    get_rich_option(
                        command_options_table, param, param.get_help_record(ctx)
                    )
                else:
                    if param.metavar:
                        command_args.append(param.metavar)
            _command = Table(highlight=True, box=None, show_header=False)
            _command.add_row(
                f"[bold sea_green3]{k}[/]", f"[bold yellow]{','.join(command_args)}[/]"
            )
            table.add_row(_command, command.help)
            if command_options_table.row_count > 0:
                table.add_row("", command_options_table)

        console.print(
            Panel(
                table,
                border_style="dim",
                title="Commands",
                title_align="left",
            )
        )


def get_rich_option(table: Table, option: Parameter, help):
    if len(option.opts) == 2:
        opt1 = highlighter(option.opts[0])
        opt2 = highlighter(option.opts[1])
    else:
        opt2 = highlighter(option.opts[0])
        opt1 = Text("")

    if option.metavar:
        opt2 += Text(f" {option.metavar}", style="bold yellow")

    table.add_row(
        opt1,
        opt2,
        highlighter(Text.from_markup(help[-1] or "", emoji=False)),
        end_section=True,
    )


@click.group(
    cls=PVXCommands,
)
@click.version_option("0.1")
def pvx():
    """Python [medium_spring_green]version[/] & [medium_spring_green]venv[/] management"""


@pvx.group(cls=GroupCommands)
def py():
    """Manages python version."""


@pvx.group(cls=GroupCommands)
def venv():
    """Manages python version."""


class Registry:
    """Register commands in the `./commands` folder.

    If you want to extend commands, be familiar with the following points.
    1. The folder where the `pvx.py` file resides is the `root`.
    2. `root/commands` is the folder where the `.py` command scripts are stored.
    3. If `filenamed` is true, use the file name command, otherwise use the argument to `@click.command`.
            - the `.py` files are named `pvx_{group}_{command}.py`.For example: `pvx_py_install.py`, which means we can call it with `pvx py install`.
    4. `.py` file must have a method called `cli` and decorated with `@click.command` .
    """

    def __init__(
        self,
        pvx_group: Dict[str, click.Group],
        cmd_folder: str = None,
        filenamed: bool = True,
    ) -> None:
        self._pvx_group = pvx_group
        self._cmd_folder = cmd_folder or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "commands")
        )
        self._filenamed = filenamed

        self.register_commands()

    def register_commands(self):
        for k, group in self._pvx_group.items():

            for filename in os.listdir(self._cmd_folder):
                if filename.endswith(".py") and filename.startswith(f"pvx_{k}_"):

                    command = self.get_command(filename.split(".")[0])

                    if command is not None and isinstance(command, click.Command):
                        self.register_command(
                            group,
                            command,
                            filename[4:-3].split("_")[-1] if self._filenamed else None,
                        )

    def get_command(self, filename: str):

        try:
            mod = __import__(f"pvx.commands.{filename}", None, None, ["cli"])
        except ImportError as e:
            print(e)
            return None
        return mod.cli

    def register_command(self, group: click.Group, command: click.Command, name: str):
        group.add_command(command, name)


_pvx_group = {
    "py": py,
    "venv": venv,
}

Registry(_pvx_group)


if __name__ == "__main__":
    pvx()
