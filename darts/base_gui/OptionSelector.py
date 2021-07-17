from tkinter import *

from tools37.events import Emitter

from darts.app_data import app_data
from darts.OrderedHash import OrderedHash
from .Button import Button


class OptionSelector(Emitter):
    def __init__(self):
        Emitter.__init__(self)
        self._key: str = ''
        self._buttons: OrderedHash[str, Button] = OrderedHash()

    def add_button(self, key: str, button: Button):
        self._buttons[key] = button
        button.config(command=lambda: self.set(key))

    def del_button(self, key: str):
        del self._buttons[key]

    def set(self, key: str):
        self.emit('set', key)
        self._key = key
        self.update()

    def get(self) -> str:
        return self._key

    def update(self):
        for key, button in self._buttons.items():
            if key == self._key:
                app_data.styles.config(button, tag='selected')
            else:
                app_data.styles.config(button, tag='')
