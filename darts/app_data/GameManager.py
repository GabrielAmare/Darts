from tkinter import Widget
from typing import Type, Generic

from darts.abstracts import PARTY, PLAYER, CONFIG, SCORE
from .AppLogger import AppLogger
from .JsonFilesManager import JsonFilesManager


class GameManager(Generic[CONFIG, PARTY, PLAYER, SCORE], JsonFilesManager):
    """This class handle all the game stuff."""

    def __init__(self, path: str, logger: AppLogger,
                 config_cls: Type[CONFIG],
                 party_cls: Type[PARTY],
                 player_cls: Type[PLAYER],
                 score_cls: Type[SCORE],
                 score_board_cls: Type[Widget]
                 ):
        super().__init__(path, factory=party_cls)
        self.logger: AppLogger = logger

        self.config_cls: Type[CONFIG] = config_cls
        self.party_cls: Type[PARTY] = party_cls
        self.player_cls: Type[PLAYER] = player_cls
        self.score_cls: Type[SCORE] = score_cls
        self.score_board_cls: Type[Widget] = score_board_cls

        self.config: CONFIG = self.load_json_file('settings.json', self.config_cls)

    def create_party(self) -> PARTY:
        uid = self.new_uid()
        party = self.party_cls(uid=uid, config=self.config.copy())
        self.save_json_file(str(uid), party)
        return party

    def load_party(self, party_uid: int) -> PARTY:
        return self.load_json_file(str(party_uid), self.party_cls)

    def save_party(self, party: PARTY):
        self.save_json_file(str(party.uid), party)
