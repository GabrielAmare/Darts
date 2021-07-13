from darts.app_logger import app_logger
from darts.base_actions import Action
from darts.base_games import BaseParty
from darts.constants import PartyState


class EndParty(Action):
    def __init__(self, party: BaseParty):
        self.party: BaseParty = party

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r})"

    def do(self) -> None:
        self.party.state = PartyState.AFTER
        app_logger.do(self)

    def undo(self) -> None:
        self.party.state = PartyState.DURING
        app_logger.undo(self)

    def redo(self) -> None:
        self.party.state = PartyState.AFTER
        app_logger.redo(self)
