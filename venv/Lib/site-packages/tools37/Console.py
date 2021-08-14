from datetime import datetime

from tools37.colors import hex_to_rgb
from tools37.ProgressBar import ProgressBar


class _Style:
    end = '\33[0m'
    bold = '\33[1m'
    # ?? = '\33[2m'
    italic = '\33[3m'
    url = '\33[4m'
    blink = '\33[5m'
    blink2 = '\33[6m'
    selected = '\33[7m'


class Chart:
    # TODO : add styling handling (with bold/italic/underlined)
    DEFAULT_FG = "#FFFFFF"
    DEFAULT_BG = "#000000"

    @staticmethod
    def foreground(code: str) -> str:
        """Convert hexadecimal color code into console foreground color code"""
        if code == "black":
            return '\33[30m'
        elif code == "red":
            return '\33[31m'
        elif code == "green":
            return '\33[32m'
        elif code == "yellow":
            return '\33[33m'
        elif code == "blue":
            return '\33[34m'
        elif code == "violet":
            return '\33[35m'
        elif code == "beige":
            return '\33[36m'
        elif code == "white":
            return '\33[37m'
        else:
            r, g, b = hex_to_rgb(code)
            return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def background(code: str) -> str:
        """Convert hexadecimal color code into console background color code"""
        if code == "black":
            return '\33[40m'
        elif code == "red":
            return '\33[41m'
        elif code == "green":
            return '\33[42m'
        elif code == "yellow":
            return '\33[43m'
        elif code == "blue":
            return '\33[44m'
        elif code == "violet":
            return '\33[45m'
        elif code == "beige":
            return '\33[46m'
        elif code == "white":
            return '\33[47m'
        else:
            r, g, b = hex_to_rgb(code)
            return f"\033[48;2;{r};{g};{b}m"

    def __init__(self, **config):
        self.config = {}
        for key, val in config.items():
            fg = Chart.foreground(val.get("fg", self.DEFAULT_FG))
            bg = Chart.background(val.get("bg", self.DEFAULT_BG))
            self.config[key] = {"prefix": fg + bg, "suffix": _Style.end}

        self.label_length = max(map(len, config.keys()), default=0)

        for key, val in self.config.items():
            val["label"] = key.rjust(self.label_length, " ")

        self.config[""] = dict(
            prefix=Chart.background(self.DEFAULT_BG) + Chart.foreground(self.DEFAULT_FG),
            suffix=_Style.end,
            label=self.label_length * " "
        )

    def get(self, tag: str):
        if tag in self.config:
            cfg = self.config[tag]
        else:
            cfg = self.config[""]

        return cfg["label"], cfg["prefix"], cfg["suffix"]


class Console:
    DEFAULT_CHART = Chart(
        LOG=dict(fg="#1ADC11", bg="#000000"),
        SQL=dict(fg="#34B7EB", bg="#000000"),
        URL=dict(fg="#11DCCF", bg="#000000"),

        DEBUG=dict(fg="#FF9300", bg="#000000"),

        INPUT=dict(fg="#FFFF00", bg="#000000"),

        WARN=dict(fg="#FFFF00", bg="#000000"),
        ERROR=dict(fg="#FF0000", bg="#000000"),

        ACTION=dict(fg="#B770FF", bg="#000000"),

        FILE=dict(fg="#CDFF70", bg="#000000"),

        START=dict(fg="#0004FF", bg="#000000"),
        END=dict(fg="#0004FF", bg="#000000"),
        ITER=dict(fg="#0BA1EA", bg="#000000"),
    )

    DEFAULT_SEPARATOR = " │ "
    DOUBLE_SEPARATOR = " ║ "

    def __init__(self, chart=None,
                 show_colors: bool = True,
                 show_times: bool = True,
                 show_count: bool = True,
                 show_debug: bool = True,
                 show_warn: bool = True,
                 width: int = 256,
                 max_lines_order: int = 6,
                 separator: str = DEFAULT_SEPARATOR
                 ):
        self.chart: Chart = chart or Console.DEFAULT_CHART

        self._show_colors: bool = show_colors
        self._show_times: bool = show_times
        self._show_count: bool = show_count

        self._show_debug: bool = show_debug
        self._show_warn: bool = show_warn

        self._separator: str = separator
        self._width: int = width

        self._level: int = 0
        self._lines: int = 0
        self._max_lines_order: int = max_lines_order

    def _make_indent(self):
        return (self.chart.label_length * " " + self._separator) * self._level

    def _make_header(self, timecode: str, indent: str, label: str) -> str:
        args = []

        if self._show_count:
            args.append(str(self._lines).zfill(self._max_lines_order))

        if self._show_times:
            args.append(timecode)

        args.append(indent + label)
        args.append("")
        return self._separator.join(args)

    def _make_hempty(self, timecode: str, indent: str) -> str:
        args = []

        if self._show_count:
            args.append(self._max_lines_order * " ")

        if self._show_times:
            args.append(len(timecode) * " ")

        args.append(indent + self.chart.label_length * " ")
        args.append("")
        return self._separator.join(args)

    def _text(self, tag: str, message: str) -> str:
        if self._show_times:
            timecode = datetime.now().isoformat()
        else:
            timecode = ""

        label, prefix, suffix = self.chart.get(tag)

        if not self._show_colors:
            prefix = ""
            suffix = ""

        indent = self._make_indent()
        header = self._make_header(timecode, indent, label)
        hempty = self._make_hempty(timecode, indent)

        first, *lines = message.split("\n")

        lines = [prefix + (header + first).ljust(self._width, " ") + suffix] + \
                [prefix + (hempty + line).ljust(self._width, " ") + suffix for line in lines]
        return "\n".join(lines)

    def print(self, message: str, tag: str = ""):
        self._lines += 1
        return print(self._text(tag, message))

    def input(self, message: str = "", tag: str = "INPUT"):
        return input(self._text(tag, message) + "\n")

    def sql(self, message: str = ""):
        self.print(message, "SQL")

    def log(self, message: str = ""):
        self.print(message, "LOG")

    def url(self, message: str = ""):
        self.print(message, "URL")

    def debug(self, message: str = ""):
        if self._show_debug:
            self.print(message, "DEBUG")

    def error(self, message: str = ""):
        self.print(message, "ERROR")

    def warn(self, message: str = ""):
        if self._show_warn:
            self.print(message, "WARN")

    def file(self, message: str = ""):
        self.print(message, "FILE")

    def action(self, message: str):
        return _Action(self, message)

    def iter(self, message: str, data: list, each: int = 1):
        assert each >= 1
        with self.action(message):
            progress_bar = ProgressBar(data)
            for item in progress_bar:
                if each != 0:
                    if progress_bar.number % each == 0:
                        self.print(
                            f"{progress_bar.progress} "
                            f"[{str(progress_bar.percent()).zfill(3)}%] "
                            f"~ {progress_bar.estimate()} remaining",
                            "ITER"
                        )
                yield item

    def __iadd__(self, delta: int):
        self._level += delta
        return self

    def __isub__(self, delta: int):
        self._level -= delta
        return self


class _Action:
    def __init__(self, csl: Console, message: str):
        self.csl: Console = csl
        self.message: str = message

    def __enter__(self):
        self.csl.print(self.message, "START")
        self.csl += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.csl -= 1
        self.csl.print(self.message, "END")

