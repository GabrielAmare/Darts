from darts.app_data import app_data
from darts.base_actions import Action
from darts.base_games import BaseParty
from darts.constants import PartyState


class StartParty(Action):
    def __init__(self, party: BaseParty):
        self.party: BaseParty = party

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r})"

    def do(self) -> None:
        self.party.state = PartyState.DURING
        app_data.logger.do(self)

    def undo(self) -> None:
        self.party.state = PartyState.BEFORE
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.party.state = PartyState.DURING
        app_data.logger.redo(self)
