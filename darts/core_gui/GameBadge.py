from tkinter import *

from tools37.events import Emitter

from darts.app_data import app_data
from darts.base_gui import Label, Button
from darts.constants import GUI


class GameBadge(Frame, Emitter):
    SETTINGS_SIZE = 24
    PLAY_SIZE = 48

    def __init__(self, root, game_uid: str):
        Frame.__init__(self, root)
        Emitter.__init__(self)

        settings_image = app_data.images.get("game-settings", size=self.SETTINGS_SIZE)
        start_image = app_data.images.get("game-start", size=self.PLAY_SIZE)

        self.top = Frame(self)
        self.bot = Frame(self)

        self.name = Label(self.top, code=f"{game_uid.upper()}.INFO.NAME")
        self.settings = Button(self.top, image=settings_image, command=self.ask_settings)

        self.description = Label(self.bot, code=f"{game_uid.upper()}.INFO.DESCRIPTION")
        self.start = Button(self.bot, image=start_image, command=self.ask_start)

        app_data.styles.build(self.top, 'GameBadge.top')
        app_data.styles.build(self.bot, 'GameBadge.bot')
        app_data.styles.build(self.name, 'GameBadge.name')
        app_data.styles.build(self.settings, 'GameBadge.settings')
        app_data.styles.build(self.description, 'GameBadge.description')
        app_data.styles.build(self.start, 'GameBadge.start')

    def ask_start(self):
        self.emit(GUI.EVENTS.GAME.START)

    def ask_settings(self):
        self.emit(GUI.EVENTS.GAME.SETTINGS)
