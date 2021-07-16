from tkinter import *

from darts.app_styles import app_styles
from darts.base_games import BaseConfig
from darts.base_games import BooleanOption, IntegerOption, StringOption
from darts.base_gui import Label, ButtonTabs


class GameSettings(Frame):
    """This interface support generic functions to edit game settings."""

    def __init__(self, root, game_uid: str, config: BaseConfig, **cfg):
        super().__init__(root, **cfg)
        self.game_uid: str = game_uid
        self.cfg: BaseConfig = config
        self.labels = []
        self.options = []

        for key, option in self.cfg.options.items():
            self.new_option(key, option)

    def new_option(self, key, option):
        label = Label(self, code=f'{self.game_uid.upper()}.SETTINGS.{key.upper()}.TITLE')
        options = ButtonTabs(self, style='GameSettings.options.button')

        value = self.cfg.get(key)

        if isinstance(option, BooleanOption):
            options.add_button(key='True', code=option.key_true)
            options.add_button(key='False', code=option.key_false)

            options.select('True' if value else 'False')

            options.on('select', lambda val: self.cfg.set(key, eval(val)))

        elif isinstance(option, IntegerOption):
            for v in option.values:
                options.add_button(key=str(v), text=str(v))

            options.select(str(value))

            options.on('select', lambda val: self.cfg.set(key, int(val)))

        elif isinstance(option, StringOption):
            for v in option.values:
                code = f'{self.game_uid.upper()}.SETTINGS.{key.upper()}.VALUE.{str(v).upper()}'
                options.add_button(key=v, code=code)

            options.select(value)

            options.on('select', lambda val: self.cfg.set(key, val))

        else:
            raise ValueError(option)

        app_styles.config(label, 'GameSettings.label')
        app_styles.config(options, 'GameSettings.options')

        label.grid(row=len(self.labels), column=0, sticky=NSEW, padx=4, pady=4)
        options.grid(row=len(self.options), column=1, sticky=NSEW, padx=4, pady=4)

        self.labels.append(label)
        self.options.append(options)
