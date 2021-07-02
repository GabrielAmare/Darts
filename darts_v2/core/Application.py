from dataclasses import dataclass
from typing import Dict, List

from tools37 import JsonFile, Console
from text_engine import Engine
from .engine import engine


class SimpleEmitter:
    def __init__(self):
        self.__functions: Dict[str, List[callable]] = {}

    def on(self, key: str, func: callable):
        self.__functions.setdefault(key, [])
        self.__functions[key].append(func)
        return lambda: (func in self.__functions[key]) and self.__functions[key].remove(func)

    def emit(self, key: str, value: object):
        for callback in self.__functions.get(key, []):
            callback(value)

    def map_to(self, key: str, obj: object, alt: str = ""):
        alt = alt or key
        return self.on(key, lambda val: setattr(obj, alt, val))


@dataclass
class Version:
    major: int
    minor: int
    patch: int


@dataclass
class Style:
    path: str
    data: dict


class Application(SimpleEmitter):
    DEFAULT_CONFIG = {
        "app_name": "Darts",
        "version": {
            "major": 1,
            "minor": 1,
            "patch": 0
        },
        "lang_IETF": "fr-FR",
        "production": True,
        "images_fp": "assets/images/",
        "styles_fp": "assets/styles/",
        "logs_fp": "logs/",
        "styles": {
            "default": "default.json",
        },
        "style": "default"
    }

    def __init__(self, wrapper, config_fp: str):
        super().__init__()

        self.wrapper = wrapper
        self.engine: Engine = engine

        self.config_fp = config_fp
        config = JsonFile.load_init(config_fp, Application.DEFAULT_CONFIG)

        self.app_name: str = config["app_name"]
        self.lang_IETF: str = config["lang_IETF"]
        self.production: bool = config["production"]
        self.version: Version = Version(**config["version"])

        self.images_fp: str = config["images_fp"]
        self.styles_fp: str = config["styles_fp"]
        self.logs_fp: str = config["logs_fp"]

        self.styles: Dict[str, Style] = {
            name: Style(path, JsonFile.load(self.styles_fp + path))
            for name, path in config["styles"].items()
        }

        self.style: str = config["style"]

        self.__original_config = config

        self.console = Console()

        self.feedback_icon = "neutral"
        self.feedback_text = ""

    def save(self):
        config = {
            "app_name": self.app_name,
            "version": {
                "major": self.version.major,
                "minor": self.version.minor,
                "patch": self.version.patch
            },
            "lang_IETF": self.lang_IETF,
            "production": self.production,
            "images_fp": self.images_fp,
            "styles_fp": self.styles_fp,
            "logs_fp": self.logs_fp,
            "styles": {name: style.path for name, style in self.styles.items()},
            "style": self.style
        }
        if config != self.__original_config:
            JsonFile.save(
                fp=self.config_fp,
                data=config
            )

    @property
    def app_name(self):
        return self._app_name

    @app_name.setter
    def app_name(self, value):
        self._app_name = value
        self.emit("app_name", value)

    @property
    def lang_IETF(self):
        return self._lang_IETF

    @lang_IETF.setter
    def lang_IETF(self, value):
        self._lang_IETF = value
        self.emit("lang_IETF", value)

    @property
    def feedback_icon(self):
        return self._feedback_icon

    @feedback_icon.setter
    def feedback_icon(self, value):
        self._feedback_icon = value
        self.emit("feedback_icon", value)

    @property
    def feedback_text(self):
        return self._feedback_text

    @feedback_text.setter
    def feedback_text(self, value):
        self._feedback_text = value
        self.emit("feedback_text", value)

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        self._style = value
        self.emit("style", value)

    def _get_style(self, tag: str) -> dict:
        if self.style not in self.styles:
            self.console.error(f"Unknown style : {self.style!r}")
            return {}

        style_data = self.styles[self.style]

        if not isinstance(style_data, Style):
            self.console.error(f"Invalid style type : {type(style_data)!r}")
            return {}

        style_data = style_data.data

        if tag not in style_data:
            self.console.error(f"Unknown style key for {self.style!r} : {tag!r}")
            return {}

        return style_data[tag]

    def apply_graphic_style(self, widget, *tags: str):
        widget_keys = widget.config().keys()

        config = {}
        for tag in ("*", *tags):
            for key, val in self._get_style(tag).items():
                if key in widget_keys:
                    config[key] = val

        widget.configure(**config)
