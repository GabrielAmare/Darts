from tkinter import *
from typing import Dict

from .AppLogger import AppLogger


class AppStyles:
    def __init__(self, config_styles, pack_styles, logger: AppLogger):
        self.config_styles = config_styles
        self.pack_styles = pack_styles
        self.logger: AppLogger = logger

        self.keys: Dict[int, str] = {}
        self.tags: Dict[int, str] = {}

    def set_key(self, widget: Widget, key: str) -> None:
        self.keys[id(widget)] = key

    def get_key(self, widget: Widget) -> str:
        return self.keys.get(id(widget), 'default')

    def set_tag(self, widget: Widget, tag: str) -> None:
        self.tags[id(widget)] = tag

    def get_tag(self, widget: Widget) -> str:
        return self.tags.get(id(widget), '')

    def get_config(self, key: str = 'default', tag: str = '') -> dict:
        if tag:
            path = key + ':' + tag
        else:
            path = key

        if path not in self.config_styles:
            self.logger.warning(f"the config style {path!r} is not defined !")
            path = key

        if path not in self.config_styles:
            self.logger.warning(f"the config style {path!r} is not defined !")
            path = 'default'

        if path in self.config_styles:
            config = self.config_styles[path]
        else:
            config = {}
            self.logger.warning(f"the config style {path!r} is not defined !")

        return config

    def config(self, widget: Widget, key: str = None, tag: str = None):
        if key is None:
            key = self.get_key(widget)
        self.set_key(widget, key)

        if tag is None:
            tag = self.get_tag(widget)
        self.set_tag(widget, tag)

        config = self.get_config(key, tag)

        widget.config(**config)

    def pack(self, widget: Widget, key: str = None, tag: str = None):
        if key is None:
            key = self.get_key(widget)
        self.set_key(widget, key)

        if tag is None:
            tag = self.get_tag(widget)
        self.set_tag(widget, tag)

        if tag:
            path = key + ':' + tag
        else:
            path = key

        if path not in self.pack_styles:
            self.logger.warning(f"the pack style {path!r} is not defined !")
            path = key

        if path not in self.pack_styles:
            self.logger.warning(f"the pack style {path!r} is not defined !")
            path = 'default'

        if path in self.pack_styles:
            config = self.pack_styles[path]
        else:
            config = {}
            self.logger.warning(f"the pack style {path!r} is not defined !")

        widget.pack(**config)

    def build(self, widget: Widget, key: str):
        self.config(widget, key)
        self.pack(widget, key)
