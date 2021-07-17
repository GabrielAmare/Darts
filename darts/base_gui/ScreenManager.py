from tkinter import *
from typing import Type, Optional

from darts.base_events import Emitter
from darts.app_data import app_data
from .ButtonTabs import ButtonTabs


class ScreenManager(Frame, Emitter):
    menu_factory: Type[ButtonTabs] = ButtonTabs
    STYLE_MENU = {}
    PACK_CONFIG = dict(side=LEFT, fill=Y, expand=True)

    def __init__(self, root, style: str):
        Frame.__init__(self, root)
        Emitter.__init__(self)

        self.menu = self.menu_factory(self, style=style + '.menu.button')
        app_data.styles.build(self.menu, style + '.menu')

        self.menu.on('select', self.on_select)

        self.widget = None
        self.widgets = []

    def add_tab(self, key: str, widget: Widget, enabled: bool = True, **cfg):
        self.widgets.append(widget)
        self.menu.add_button(key=key, enabled=enabled, **cfg)

    def set_tab(self, key: str, widget: Widget):
        index = self.menu.buttons.keys.index(key)
        self.widgets[index] = widget

    def get_tab(self, key: str) -> Optional[Widget]:
        index = self.menu.buttons.keys.index(key)
        return self.widgets[index]

    def on_select(self, key: str):
        index = self.menu.buttons.keys.index(key)
        widget = self.widgets[index]

        if widget is not self.widget:
            if self.widget:
                self.widget.pack_forget()

            self.widget = widget
            if self.widget:
                self.widget.pack(side=TOP, fill=BOTH, expand=True)

        self.emit('select', key)

    def select(self, key: str):
        self.menu.select(key)

    def enable(self, key: str):
        self.menu.enable(key)

    def disable(self, key: str):
        self.menu.disable(key)
