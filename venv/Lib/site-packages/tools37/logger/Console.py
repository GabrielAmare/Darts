from __future__ import annotations

from typing import Dict

from tools37.colors import BLACK, WHITE
from tools37.console import Console as BaseConsole
from .Entry import Entry

__all__ = ["Console"]


class Console(BaseConsole):
    """
        Console implementation to display the log lines in a fancy way
    """

    def __init__(self, width: int = 100, styles: Dict[str, Console.Style] = None):
        if styles is None:
            styles = {}

        if '_time' not in styles:
            styles['_time'] = Console.Style(bg=BLACK, fg='#AAAAFF')

        if '_code' not in styles:
            styles['_code'] = Console.Style(bg=BLACK, fg='#2222FF')

        if '_content' not in styles:
            styles['_content'] = Console.Style(bg=BLACK, fg=WHITE)

        self.styles = styles
        super().__init__(26, max([len(key) for key in self.styles.keys() if not key.startswith('_')], default=0), width)

    def print(self, entry: Entry):
        """Print the specified Entry."""
        style = self.styles.get(entry.code)

        self.display(
            objects=[
                entry.at.isoformat(),
                entry.code,
                entry.content
            ],
            styles=[
                self.styles['_time'],
                style or self.styles['_code'],
                style or self.styles['_content']
            ]
        )
