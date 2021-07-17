from tkinter import *
from typing import Type

from darts.app_data import app_data
from darts.base_gui import ScreenManager
from darts.constants import GUI
from .AppTabManager import AppTabManager
from .GameMenu import GameMenu
from .SettingsMenu import SettingsMenu


class Body(ScreenManager):
    menu_factory = AppTabManager

    def __init__(self, root):
        super().__init__(root, style='Body')

        self.new_tab(GUI.TABS.GAME_MENU, GameMenu, style='GameMenu', enabled=True)
        self.new_tab(GUI.TABS.APP_SETTINGS, SettingsMenu, style='SettingsMenu', enabled=True)
        self.new_tab(GUI.TABS.CURRENT_PARTY, Frame, style='CurrentParty', enabled=app_data.has_party())
        self.new_tab(GUI.TABS.GAME_SETTINGS, Frame, style='GameSettings', enabled=False)

    def new_tab(self, key: str, cls: Type[Widget], style: str, enabled: bool = True, **cfg):
        widget = cls(self, **cfg)
        self.add_tab(key, widget, enabled=enabled)
        app_data.styles.config(widget, style)
