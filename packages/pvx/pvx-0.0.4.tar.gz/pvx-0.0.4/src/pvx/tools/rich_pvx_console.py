import os
from typing import List
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme


class PvxHighlighter(RegexHighlighter):
    """Apply style to pvx cli console.

    Now supported:
    - pvx command
    - python version number
    """

    base_style = "pvx."
    highlights = [
        r"(?P<help>\`.*\`)",
        # r"(?P<version>[.|\-|\w]*[1-9]\.[0-9][.|\-|\w]*)",
        r"(?P<version>[\w|\-|\.]*[1-9]\.[0-9][\w|\-|\.]*)",
    ]


pvx_hint_color = "magenta"
pvx_help_color = "medium_spring_green"

_console = Console(
    highlighter=PvxHighlighter(),
    theme=Theme({"pvx.help": pvx_help_color, "pvx.version": pvx_hint_color}),
)


class PvxConsole:
    def __init__(self) -> None:

        self._text: List[str] = []
        self._pvx_emoji = "🐍 "
        self._new_line_prefix = os.linesep * 2 + " " * 3

    def text(self, text: str):
        """normal text"""
        self._text.append(text)
        return self

    def nlp(self):
        """new line prefix"""
        self._text.append(self._new_line_prefix)
        return self

    def nl(self):
        """new line"""
        self._text.append(os.linesep)
        return self

    def help(self, help_text: str):
        """help text"""
        self._text.append(self._new_line_prefix)
        self._text.append(help_text)
        return self

    def print(self, text: str = None, pvx_emoji: bool = True):
        """print and clear text"""
        if text:
            if pvx_emoji:
                _console.print(self._pvx_emoji + text)
            else:
                _console.print(text)
        else:
            if pvx_emoji:
                _console.print(self._pvx_emoji + "".join(self._text))
            else:
                _console.print("".join(self._text))
        self._text.clear()

    @classmethod
    def pager(cls, *text):
        """
        Render long output by scrolling
        https://rich.readthedocs.io/en/latest/console.html#paging
        """
        with _console.pager(styles=True):
            for _text in text:
                _console.print(_text)


console = PvxConsole()
