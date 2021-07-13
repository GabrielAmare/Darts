from typing import Optional

from darts.app_logger import app_logger
from darts.base_actions import Action
from darts.base_games import BaseParty, BasePlayer


class SetLastPlayer(Action):
    def __init__(self, party: BaseParty, name: str):
        self.party: BaseParty = party
        self.name: str = name

        self.player: Optional[BasePlayer] = None
        self.last: Optional[BasePlayer] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.name!r})"

    def do(self) -> None:
        self.last = self.party.latest
        self.player = self.party.get_player_by_name(self.name)
        self.party.latest = self.player
        app_logger.do(self)

    def undo(self) -> None:
        self.party.latest = self.last
        app_logger.undo(self)

    def redo(self) -> None:
        self.party.latest = self.player
        app_logger.redo(self)
