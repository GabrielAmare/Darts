from typing import List

from darts.app_data import app_data
from darts.base_actions import Action
from darts.base_games import BaseParty, BasePlayer


class SetWinners(Action):
    def __init__(self, party: BaseParty, players: List[BasePlayer]):
        self.party: BaseParty = party
        self.players: List[BasePlayer] = players

    def __repr__(self) -> str:
        args = [self.party, *self.players]
        return f"{self.__class__.__name__}({self.party!r}, {self.players!r})"

    def do(self) -> None:
        self.party.winners = self.players
        app_data.logger.do(self)

    def undo(self) -> None:
        self.party.winners = []
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.party.winners = self.players
        app_data.logger.redo(self)
