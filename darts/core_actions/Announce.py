from darts.app_logger import app_logger
from darts.base_actions import Action
from darts.base_games import BaseParty


class Announce(Action):
    def __init__(self, party: BaseParty, code: str, config: dict):
        self.party: BaseParty = party
        self.code: str = code
        self.config: dict = config

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.code!r}, {self.config!r})"

    def do(self) -> None:
        self.party.emit('announce', self.code, **self.config)
        app_logger.do(self)

    def undo(self) -> None:
        app_logger.undo(self)

    def redo(self) -> None:
        app_logger.redo(self)
