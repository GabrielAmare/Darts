from __future__ import annotations

from tkinter import *
from typing import List, Optional

from darts.app_styles import app_styles
from darts.base_games import BasePlayer, BaseScore, BaseConfig, Game
from darts.constants import PartyState
from darts.core_commands import ScoreValue
from darts.core_games import BaseParty as BaseParty
from darts.core_gui.PlayerButton import PlayerButton
from darts.core_gui.ScoreBoard import ScoreBoard as BaseScoreBoard
from darts.errors import InvalidScoreError


class Config(BaseConfig):
    @classmethod
    def from_dict(cls, data: dict) -> Config:
        return cls(**data)

    def to_dict(self) -> dict:
        return self.__dict__

    def copy(self):
        return Config(
            default_score=self.default_score,
            double_in=self.double_in,
            double_out=self.double_out
        )

    def __init__(self, default_score: int = 301, double_in: bool = False, double_out: bool = True):
        assert default_score in [301, 501, 801]
        assert double_in in [True, False]
        assert double_out in [True, False]
        self.default_score: int = default_score
        self.double_in: bool = double_in
        self.double_out: bool = double_out

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default_score!r}, {self.double_in!r}, {self.double_out!r})"


class Score(BaseScore):
    @classmethod
    def from_dict(cls, data: dict) -> Score:
        return cls(value=data['value'], delta=data['delta'])

    def to_dict(self) -> dict:
        return dict(value=self.value, delta=self.delta)

    def __init__(self, value: int, delta: int):
        super().__init__()
        self.value: int = value
        self.delta: int = delta

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r}, {self.delta!r})"


class Player(BasePlayer[Score]):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data['name'],
            scores=list(map(Score.from_dict, data['scores']))
        )

    def to_dict(self) -> dict:
        return dict(name=self.name, scores=list(map(Score.to_dict, self.scores)))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self.scores!r})"


class Party(BaseParty[Config, Player, Score]):
    @classmethod
    def from_dict(cls, data: dict) -> Party:
        return cls(
            config=Config.from_dict(data['config']),
            players=list(map(Player.from_dict, data['players'])),
            latest=data['latest'],
            state=data['state'],
            winners=data['winners']
        )

    def to_dict(self) -> dict:
        return dict(
            config=self.config.to_dict(),
            players=list(map(Player.to_dict, self.players)),
            latest=self.latest.name if self.latest else '',
            state={
                PartyState.BEFORE: 'BEFORE',
                PartyState.DURING: 'DURING',
                PartyState.AFTER: 'AFTER',
            }[self.state],
            winners=[player.name for player in self.winners]
        )

    def __repr__(self):
        return f"Party(...)"

    def announce_score(self, player: Player, score: Score) -> None:
        if score.delta == 0:
            return

        self.announce('GLOBAL.PLAYER_MARKED', name=player.name, marks=score.delta)

        if score.delta == 180:
            self.announce('GLOBAL.PLAYER_MARKED_PERFECT')
        elif 100 <= score.delta < 180:
            self.announce('GLOBAL.PLAYER_MARKED_GOOD')
        elif 0 < score.delta <= 10 and player.score.value >= 40:
            self.announce('GLOBAL.PLAYER_MARKED_POORLY', name=player.name, marks=score.delta)

    def announce_player(self, player: Player):
        super().announce_player(player)

        total = player.score.value

        if total <= 170:  # elligibility
            self.announce('301.ANNOUNCE_REMAINING_SCORE', score=total)

        if total == 42:  # answer to everything
            self.announce('301.ANNOUNCE_42')

        elif total == 50:  # double BULL
            self.announce('301.ANNOUNCE_50')

        elif total <= 40 and total % 2 == 0:  # double to WIN
            self.announce('301.ANNOUNCE_DOUBLE_TO_WIN', half_score=total // 2)

    def create_player(self, name: str) -> Player:
        return Player(name=name)

    def initial_score(self, player: Player) -> Score:
        return Score(value=self.config.default_score, delta=0)

    def update_score(self, player: Player, marks: List[ScoreValue]) -> Score:
        delta = sum(mark.factor * mark.value for mark in marks)
        new_value = player.score.value - delta

        if new_value == 1 and self.config.double_out:
            raise InvalidScoreError()

        if new_value < 0 or new_value > self.config.default_score:
            raise InvalidScoreError()

        return Score(value=new_value, delta=delta)

    def check_winner(self) -> bool:
        for player in self.players:
            if player.scores and player.score.value == 0:
                self.set_winners([player])
                return True

        return False


game = Game(config_cls=Config, party_cls=Party, player_cls=Player, score_cls=Score)


class PlayerBadge(Frame):
    def __init__(self, root, party: Party, player: Player):
        super().__init__(root)

        self.party: Party = party
        self.player: Player = player

        self.button = PlayerButton(self, party=party, player=player)
        self.score = Label(self, text='')

        self.button.pack(side=TOP, fill=X)
        self.score.pack(side=TOP, fill=X)

        app_styles.config(self.button, '301.PlayerBadge.label')
        app_styles.config(self.score, '301.PlayerBadge.score')

        self.player.on('scores.append', self.update)
        self.player.on('scores.remove', self.update)
        self.player.on('scores.insert', self.update)
        self.player.on('scores.pop', self.update)
        self.player.on('scores.set', self.update)

        self.update()

    def update(self, *_, **__):
        """This will update the widget."""

        self.button.update()

        if self.player.scores:
            self.score.config(text=str(self.player.score.value))

        self.button.update_idletasks()
        self.score.update_idletasks()
        self.update_idletasks()


class ScoreBoard(BaseScoreBoard[Config, Party, Player, Score]):
    def __init__(self, root, party: Party):
        super().__init__(root, party)

        self.widgets: List[PlayerBadge] = []

        for player in self.party.players:
            self.on_players_append(player)

    def new_badge_player(self, player: Player) -> PlayerBadge:
        return PlayerBadge(self, self.party, player)

    def get_player_badge(self, player: Player) -> Optional[PlayerBadge]:
        for badge in self.widgets:
            if badge.player is player:
                return badge

    def on_players_append(self, player: Player):
        badge = self.new_badge_player(player)
        self.widgets.append(badge)
        self.update()

    def on_players_remove(self, player: Player):
        badge = self.get_player_badge(player)
        self.widgets.remove(badge)
        self.update()

    def on_players_insert(self, index: int, player: Player):
        badge = self.new_badge_player(player)
        self.widgets.insert(index, badge)
        self.update()

    def on_players_pop(self, index: int, player: Player):
        self.widgets.pop(index)
        self.update()

    def on_players_set(self, index: int, player: Player):
        badge = self.get_player_badge(player) or self.new_badge_player(player)
        self.widgets[index] = badge
        self.update()

    def update(self, *_, **__):
        for index in range(len(self.party.players)):
            self.columnconfigure(index, weight=1)

        next_player = self.party.get_next_player()

        for badge in self.widgets:
            player = badge.player
            if player in self.party.players:
                index = self.party.players.index(player)
                self.grid_at(badge, row=0, column=index, padx=40, pady=40)
                app_styles.config(
                    widget=badge,
                    key='301.PlayerBadge',
                    tag='selected' if player is next_player else ''
                )
                app_styles.config(
                    widget=badge.button,
                    key='301.PlayerBadge.label',
                    tag='selected' if player is next_player else ''
                )
            else:
                badge.destroy()

        self.update_idletasks()
