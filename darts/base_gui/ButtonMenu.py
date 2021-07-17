from tools37.events import Emitter

from .ButtonList import ButtonList


class ButtonMenu(ButtonList, Emitter):
    """Displays a list of buttons and emit an event when some is clicked."""

    def __init__(self, root, style: str):
        ButtonList.__init__(self, root, style)
        Emitter.__init__(self)

    def select(self, key: str):
        self.emit('select', key)

    def add_button(self, key: str, enabled: bool = True, **config):
        super().add_button(key, enabled, command=lambda: self.select(key), **config)
