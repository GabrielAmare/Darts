from __future__ import annotations

from tkinter import *
from typing import List, Optional

from darts.Profile import Profile
from darts.app_data import app_data
from darts.base_games import BasePlayer, BaseScore, BaseConfig
from darts.base_games import StringOption
from darts.commands import ScoreValue
from darts.actions import RemovePlayer
from darts.core_games import BaseParty as BaseParty
from darts.core_gui.PlayerButton import PlayerButton
from darts.core_gui.ScoreBoard import ScoreBoard as BaseScoreBoard
from darts.errors import InvalidScoreError, PlayerEliminationException


class Config(BaseConfig):
    killer = StringOption(
        default='killer',
        values=['killer', 'no-killer', 'auto-killer', 'kamikaze']
    )
    drop_down = StringOption(
        default='level-25',
        values=["level-25", "level-0"]
    )
    elimination = StringOption(
        default='elimination',
        values=["no-elimination", "elimination"]
    )


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
    score_cls = Score


class Party(BaseParty[Config, Player, Score]):
    config_cls = Config
    player_cls = Player

    def announce_score(self, player: Player, score: Score) -> None:
        if score.delta == 0:
            return

        self.announce('GLOBAL.PLAYER_MARKED', name=player.name, marks=score.delta)

        if score.delta == 12:
            self.announce('GLOBAL.PLAYER_MARKED_PERFECT')

        elif score.delta == 0:
            self.announce('GLOBAL.PLAYER_MARKED_POORLY', name=player.name, marks=score.delta)

    def create_player(self, profile: Profile) -> Player:
        return Player(profile=profile)

    def initial_score(self, player: Player) -> Score:
        return Score(value=0, delta=0)

    def dropdown(self, value: int) -> Score:
        if self.config.drop_down == 'level-25' and value >= 25:
            return Score(value=25, delta=-1)
        else:
            return Score(value=0, delta=-1)

    def update_score(self, player: Player, marks: List[ScoreValue]) -> Score:
        delta = sum(mark.factor * mark.value for mark in marks)
        if delta > 12 or delta < 0:
            raise InvalidScoreError()

        new_value = player.score.value + delta

        # DROP-DOWN
        if new_value > 50:
            new_score = self.dropdown(new_value)
            self.announce('MOLKKY.ANNOUNCE_DROPDOWN', value=new_score.value)
            return new_score

        # ELIMINATION
        if self.config.elimination == 'elimination':
            if delta == 0 and len(player.scores) >= 2 and player.scores[-2].delta == 0 and player.scores[-1].delta == 0:
                raise PlayerEliminationException()

        # KILLER
        if self.config.killer == 'killer':
            for other in self.players:
                if other is not player and other.scores and other.score.value == new_value:
                    new_score = self.dropdown(other.score.value)
                    self.set_score(other, new_score)
                    self.announce('MOLKKY.ANNOUNCE_KILL', name=other.name, value=new_score.value)

        elif self.config.killer == 'auto-killer':
            for other in self.players:
                if other is not player and other.scores and other.score.value == new_value:
                    new_score = self.dropdown(new_value)
                    self.announce('MOLKKY.ANNOUNCE_DROPDOWN', value=new_score.value)
                    return new_score

        elif self.config.killer == 'kamikaze':
            do_dd = False
            for other in self.players:
                if other is not player and other.scores and other.score.value == new_value:
                    new_score = self.dropdown(other.score.value)
                    self.set_score(other, new_score)
                    self.announce('MOLKKY.ANNOUNCE_KILL', name=other.name, value=new_score.value)
                    do_dd = True

            if do_dd:
                new_score = self.dropdown(new_value)
                self.announce('MOLKKY.ANNOUNCE_DROPDOWN', value=new_score.value)
                return new_score

        return Score(value=new_value, delta=delta)

    def check_winner(self) -> bool:
        if len(self.players) == 1:
            self.set_winners([self.players[0]])
            return True

        for player in self.players:
            if player.scores and player.score.value == 50:
                self.set_winners([player])
                return True

        return False


class PlayerBadge(Frame):
    def __init__(self, root, party: Party, player: Player):
        super().__init__(root)

        self.party: Party = party
        self.player: Player = player

        self.button = PlayerButton(self, party=party, player=player)
        self.score = Label(self, text='')

        self.button.pack(side=TOP, fill=X)
        self.score.pack(side=TOP, fill=X)

        app_data.styles.config(self.button, '301.PlayerBadge.label')
        app_data.styles.config(self.score, '301.PlayerBadge.score')

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
                app_data.styles.config(
                    widget=badge,
                    key='301.PlayerBadge',
                    tag='selected' if player is next_player else ''
                )
                app_data.styles.config(
                    widget=badge.button,
                    key='301.PlayerBadge.label',
                    tag='selected' if player is next_player else ''
                )
            else:
                badge.destroy()

        self.update_idletasks()


app_data.games.register(
    game_uid='molkky',
    config_cls=Config,
    party_cls=Party,
    player_cls=Player,
    score_cls=Score,
    score_board_cls=ScoreBoard
)
