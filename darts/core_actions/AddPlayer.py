from typing import Optional

from darts.app_data import app_data
from darts.base_actions import Action
from darts.base_games import BaseParty, BasePlayer


class AddPlayer(Action):
    def __init__(self, party: BaseParty, name: str):
        self.party: BaseParty = party
        self.name: str = name

        self.player: Optional[BasePlayer] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.name!r})"

    def do(self) -> None:
        self.player = self.party.create_player(self.name)
        self.party.players.append(self.player)
        app_data.logger.do(self)

    def undo(self) -> None:
        self.party.players.remove(self.player)
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.party.players.append(self.player)
        app_data.logger.redo(self)
