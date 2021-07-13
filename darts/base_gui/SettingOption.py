from tkinter import *
from typing import Dict

from darts.app_styles import app_styles
from .ButtonTabs import ButtonTabs
from .Label import Label


class SettingOption(ButtonTabs):
    def __init__(self, root, game_uid: str, key: str, options: Dict[str, dict], default_option: str = '',
                 parse_key: callable = str):
        assert key.isidentifier()
        super().__init__(root, style='SettingOption.button')
        self.label = Label(self, code=f"{game_uid.upper()}.SETTINGS.{key.upper()}")
        app_styles.build(self.label, 'SettingOption.label')

        for key, cfg in options.items():
            self.add_button(key, **cfg)

        if default_option:
            self.select(default_option)

        self.on('select', lambda val: self.emit('choose', parse_key(val)))
