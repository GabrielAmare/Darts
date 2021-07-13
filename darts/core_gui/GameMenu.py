from tkinter import *
from typing import List

from darts.base_events import Emitter
from darts.constants import GUI
from darts.app_styles import app_styles
from darts.app_games import app_games
from .GameBadge import GameBadge


class GameMenu(Frame, Emitter):
    def __init__(self, root, **cfg):
        Frame.__init__(self, root, **cfg)
        Emitter.__init__(self)

        self.badges: List[GameBadge] = []

        self.holder = Frame(self)

        app_styles.build(self.holder, 'GameMenu.holder')

        for game_uid in app_games.get_game_uids():
            self.add_game(game_uid)

    def add_game(self, game_uid):
        badge = GameBadge(self.holder, game_uid=game_uid)
        app_styles.build(badge, 'GameBadge')

        badge.on(GUI.EVENTS.GAME.START, lambda: self.ask_start(game_uid))
        badge.on(GUI.EVENTS.GAME.SETTINGS, lambda: self.ask_settings(game_uid))

    def ask_start(self, game_uid):
        self.emit(GUI.EVENTS.GAME.START, game_uid)

    def ask_settings(self, game_uid):
        self.emit(GUI.EVENTS.GAME.SETTINGS, game_uid)
