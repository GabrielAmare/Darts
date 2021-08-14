from .constants import STYLES, END
from .functions import as_fg, as_bg
from tools37 import colors


class Style:
    def __init__(self,
                 bg: str = colors.BLACK,
                 fg: str = colors.WHITE,
                 italic: bool = False,
                 bold: bool = False,
                 selected: bool = False,
                 url: bool = False,
                 blink: int = 0):
        assert blink in (0, 1, 2)
        self.bg: str = bg
        self.fg: str = fg
        self.italic: bool = italic
        self.bold: bool = bold
        self.selected: bool = selected
        self.url: bool = url
        self.blink: int = blink

    @property
    def prefix(self):
        prefix = as_bg(self.bg) + as_fg(self.fg)
        if self.italic:
            prefix += STYLES['italic']
        if self.bold:
            prefix += STYLES['bold']
        if self.selected:
            prefix += STYLES['selected']
        if self.url:
            prefix += STYLES['url']
        if self.blink == 1:
            prefix += STYLES['blink']
        elif self.blink == 2:
            prefix += STYLES['blink2']
        return prefix

    def __call__(self, text: str) -> str:
        return self.prefix + text + END
