from tools37.colors import hex_to_rgb
from .constants import FOREGROUND_COLORS, BACKGROUND_COLORS


def as_fg(code: str) -> str:
    """Convert hexadecimal color code into console foreground color code"""
    try:
        return FOREGROUND_COLORS[code]
    except KeyError:
        r, g, b = hex_to_rgb(code)
        return f"\033[38;2;{r};{g};{b}m"


def as_bg(code: str) -> str:
    """Convert hexadecimal color code into console background color code"""
    try:
        return BACKGROUND_COLORS[code]
    except KeyError:
        r, g, b = hex_to_rgb(code)
        return f"\033[48;2;{r};{g};{b}m"


def sized_str(s: str, w: int) -> str:
    """Return the string (s) modified to fit the correct width (w)"""
    n = len(s)
    if n < w:
        return s.ljust(w, ' ')
    elif n > w:
        return s[:w - 1] + '…'
    else:
        return s
