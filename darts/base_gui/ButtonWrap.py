from tkinter import *

from darts.OrderedHash import OrderedHash
from darts.app_data import app_data
from .Button import Button
from .OptionSelector import OptionSelector
from .WidgetWrap import WidgetWrap


class ButtonWrap(WidgetWrap):
    """Displays a grid of buttons."""

    def __init__(self, root, wrap_width: int, style: str, grid_config: dict = None, **cfg):
        super().__init__(root, wrap_width, grid_config, **cfg)

        self.style: str = style

        self.selector: OptionSelector = OptionSelector()

        self.buttons: OrderedHash[str, Button] = OrderedHash()

    def set(self, key: str):
        self.selector.set(key)

    def get(self) -> str:
        return self.selector.get()

    def disable(self, key: str):
        self.buttons[key].disable()

    def enable(self, key: str):
        self.buttons[key].enable()

    def new_button(self, key: str, **config) -> Button:
        assert key not in self.buttons

        button = self.new_widget(Button, **config)

        self.buttons[key] = button
        app_data.styles.config(button, self.style)

        self.selector.add_button(key, button)

        return button

    def del_button(self, key: str):
        del self.buttons[key]
