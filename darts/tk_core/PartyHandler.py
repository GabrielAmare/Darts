from tkinter import *
from darts.classes import Party

from ..app_config import STYLE


class PartyHandler(Frame):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)
        self.board = None
        self.party = None

    @property
    def party(self) -> Party:
        return self._party

    @party.setter
    def party(self, value):
        if self.board is not None:
            self.board.destroy()

        self._party = value
        if self._party is not None:
            self.board = self._party.tk_scoreboard(self, **STYLE.PARTY_HANDLER.SCOREBOARD)
            self.board.pack(side=TOP, fill=BOTH, expand=True)
