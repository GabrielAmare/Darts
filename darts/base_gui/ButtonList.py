from tkinter import *

from darts.OrderedHash import OrderedHash
from darts.app_data import app_data
from .Button import Button


class ButtonList(Frame):
    """Displays a list of buttons."""

    def __init__(self, root, style: str):
        super().__init__(root)

        self.style: str = style

        self.buttons: OrderedHash[str, Button] = OrderedHash()

    def disable(self, key: str):
        self.buttons[key].disable()

    def enable(self, key: str):
        self.buttons[key].enable()

    def add_button(self, key: str, enabled: bool = True, **config) -> Button:
        assert key not in self.buttons

        button = self.buttons[key] = Button(self, **config)

        app_data.styles.build(button, self.style)

        if enabled:
            button.enable()
        else:
            button.disable()

        return button

    def del_button(self, key: str):
        del self.buttons[key]
