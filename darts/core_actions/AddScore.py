from darts.app_data import app_data
from darts.base_actions import Action
from darts.base_games import BaseParty, BasePlayer, BaseScore


class AddScore(Action):
    def __init__(self, party: BaseParty, player: BasePlayer, score: BaseScore):
        self.party: BaseParty = party
        self.player: BasePlayer = player
        self.score: BaseScore = score

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.player!r}, {self.score!r})"

    def do(self) -> None:
        self.player.scores.append(self.score)
        app_data.logger.do(self)

    def undo(self) -> None:
        self.player.scores.remove(self.score)
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.player.scores.append(self.score)
        app_data.logger.redo(self)
