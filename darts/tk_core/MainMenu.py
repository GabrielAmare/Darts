from tkinter import *

from darts.game_engine import SelectPartyType
from ..app_config import STYLE, APP_CFG


class MainMenu(Frame):
    def __init__(self, root, app, **cfg):
        Frame.__init__(self, root, **cfg)

        self.app = app
        self.games = {}

        for game in APP_CFG.get("games", []):
            self.import_game(
                name=game["name"],
                key=game["key"]
            )

    def import_game(self, name, key):
        button = Button(
            self,
            text=name,
            command=lambda: self.app.on_select_party_type(SelectPartyType(key)),
            **STYLE.MAIN_MENU.BTN_CFG
        )
        button.pack(side=TOP, pady=30)
        self.games[key] = button
