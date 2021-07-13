from __future__ import annotations
from typing import List

from darts import core_commands as cmd, base_games as bg, core_games as cg
from darts.errors import InvalidScoreError


class Config(bg.BaseConfig):
    @classmethod
    def from_dict(cls, data: dict) -> Config:
        return cls(**data)

    def to_dict(self) -> dict:
        return self.__dict__

    def __init__(self, killer: str = "killer", drop_down: str = "level-25", elimination: str = "elimination-3"):
        assert killer in ["killer", "no-killer", "auto-killer", "kamikaze"]
        assert drop_down in ["level-25", "level-0"]
        assert elimination in ["no-elimination", "elimination-3", "elimination-dropdown"]
        self.killer: str = killer
        self.drop_down: str = drop_down
        self.elimination: str = elimination


class Score(bg.BaseScore):
    def __init__(self, value: int):
        super().__init__()
        self.value: int = value


class Player(bg.BasePlayer[Score]):
    pass


class Party(cg.BaseParty[Config, Player, Score]):
    def _announce_score(self, player: Player, marks: List[cmd.ScoreValue]) -> None:
        total = sum(mark.factor * mark.value for mark in marks)

        if total == 0:
            return

        self._vocalize("PLAYER_MARKED", name=player.name, marks=total)

        if total <= 10 and player.score.value >= 40:
            self._vocalize("PLAYER_MARKED_POORLY", name=player.name, marks=total)
        elif total == 180:
            self._vocalize("PLAYER_MARKED_PERFECT")
        elif total >= 100:
            self._vocalize("PLAYER_MARKED_GOOD")

    def _announce_player(self, player: Player):
        super()._announce_player(player)

        total = player.score.value

        if total <= 170:  # elligibility
            self._vocalize("ANNOUNCE_REMAINING_SCORE", score=total)

        if total == 42:  # answer to everything
            self._vocalize("ANNOUNCE_42")

        elif total == 50:  # double BULL
            self._vocalize("ANNOUNCE_50")

        elif total <= 40 and total % 2 == 0:  # double to WIN
            self._vocalize("ANNOUNCE_DOUBLE_TO_WIN", half_score=total // 2)

    def create_player(self, name: str) -> Player:
        return Player(name=name)

    def initial_score(self, player: Player) -> Score:
        return Score(value=self.config.default_score)

    def update_score(self, player: Player, marks: List[cmd.ScoreValue]) -> Score:
        total = sum(mark.factor * mark.value for mark in marks)
        new_value = player.score.value - total

        if new_value == 1 and self.config.double_out:
            raise InvalidScoreError()

        if new_value < 0 or new_value > self.config.default_score:
            raise InvalidScoreError()

        return Score(value=new_value)

    def check_winner(self) -> None:
        if len(self.players) == 1:
            return self.set_winners(self.players[0])

        elif len(self.players) == 0:
            return self.set_winners()

        for player in self.players:
            if player.scores and player.score.value == 50:
                return self.set_winner(player)


game = bg.Game(config_cls=Config, party_cls=Party, player_cls=Player, score_cls=Score)

from tkinter import Frame


class ScoreBoard(Frame):
    pass
