import os
from typing import Tuple


class Terminal:
    @classmethod
    def size(self) -> Tuple[int, int]:
        """
        Get current termianl window size
        """
        ws = os.get_terminal_size()
        return (ws.lines, ws.columns)
