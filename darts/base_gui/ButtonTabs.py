from darts.base_events import Emitter
from darts.app_styles import app_styles
from .ButtonList import ButtonList
from .ButtonMenu import ButtonMenu


class ButtonTabs(ButtonMenu, Emitter):
    """Displays a list of buttons and emit an event when some is clicked, also keep the selected key in memory."""

    def __init__(self, root, style: str):
        ButtonList.__init__(self, root, style)
        Emitter.__init__(self)

        self.selected: str = ''

    def select(self, key: str):
        assert key in self.buttons or key == '', key

        for c_key, button in self.buttons.items():
            if c_key == key:
                app_styles.config(button, tag='selected')
                self.selected = key
            else:
                app_styles.config(button, tag='')

        super().select(key)

    def del_button(self, key: str):
        super().del_button(key)
        if self.selected == key:
            self.select('')