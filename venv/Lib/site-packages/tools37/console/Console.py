from itertools import zip_longest
from typing import Tuple, List

from tools37 import colors
from .Style import Style
from .functions import sized_str


class Console:
    Style = Style

    BD = Style(bg=colors.BLACK, fg=colors.GRAY)

    def __init__(self, *widths: int, separator=' │ ', prefix='▌', suffix='▐', bd: Style = BD):
        self.prefix = bd(prefix)
        self.separator = bd(separator)
        self.suffix = bd(suffix)

        self.widths: Tuple[int] = widths

    def _render_line(self, items: List[str]) -> str:
        return self.prefix + self.separator.join(items) + self.suffix

    def _style_items(self, items: List[str], styles: List[Style]) -> List[str]:
        return [style(item) for style, item in zip(styles, items)]

    def _resize_items(self, items: List[str]) -> List[str]:
        return [sized_str(item, width) for item, width in zip(items, self.widths)]

    def display(self, objects: List[object], styles: List[Style]) -> None:
        columns = map(str.splitlines, map(str, objects))
        for items in zip_longest(*columns, fillvalue=''):
            items = self._resize_items(items)
            items = self._style_items(items, styles)
            line = self._render_line(items)
            print(line)
