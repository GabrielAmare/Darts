from __future__ import annotations

from tkinter import *
from typing import Optional, List

from darts.app_styles import app_styles
from darts.base_games import BasePlayer, BaseScore, BaseConfig, Game, StringOption
from darts.core_commands import ScoreValue
from darts.core_games import BaseParty as BaseParty
from darts.core_gui.PlayerButton import PlayerButton
from darts.core_gui.ScoreBoard import ScoreBoard as BaseScoreBoard
from darts.errors import InvalidScoreError

ASCENDING = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25]
DESCENDING = [0, 25, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]


class Config(BaseConfig):
    order = StringOption(default='ascending', values=['ascending', 'descending'])

    @property
    def targets(self) -> List[int]:
        if self.order == 'ascending':
            return ASCENDING
        elif self.order == 'descending':
            return DESCENDING
        else:
            raise ValueError(self.order)


class Score(BaseScore):
    @classmethod
    def from_dict(cls, data: dict) -> Score:
        return cls(value=data['value'], delta=data['delta'])

    def to_dict(self) -> dict:
        return dict(value=self.value, delta=self.delta)

    def __init__(self, value: int = 0, delta: int = 0):
        assert value in ASCENDING, value
        assert delta in [0, 1, 2, 3], delta
        super().__init__()
        self.value: int = value
        self.delta: int = delta

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r}, {self.delta!r})"

    def copy(self) -> Score:
        return Score(value=self.value, delta=self.delta)


class Player(BasePlayer[Score]):
    score_cls = Score


class Party(BaseParty[Config, Player, Score]):
    config_cls = Config
    player_cls = Player
    
    def announce_score(self, player: Player, score: Score) -> None:
        if score.delta == 3:
            self.announce('GLOBAL.PLAYER_MARKED_PERFECT')

    def announce_player(self, player: Player):
        super().announce_player(player)

        target = self.score_target(player.score)

        self.announce('RTC.ANNOUNCE_TARGET', target='BULL' if target == 25 else target)

    def index_to_value(self, index: int) -> int:
        targets = self.config.targets
        if 0 <= index < len(targets):
            return targets[index]
        elif index == len(targets):
            return 0
        else:
            return -1

    def value_to_index(self, target: int) -> int:
        targets = self.config.targets
        if target in targets:
            return targets.index(target)
        else:
            return -1

    def score_target(self, score: Score) -> int:
        """Return the next target of the score, 0 if there's no target, -1 if the origin is wrong."""
        index = self.value_to_index(score.value)
        value = self.index_to_value(index + 1)
        return value

    def create_player(self, name: str) -> Player:
        return Player(name=name, scores=[])

    def initial_score(self, player: Player) -> Score:
        return Score(value=self.config.targets[0], delta=0)

    def update_score(self, player: Player, marks: List[ScoreValue]) -> Score:
        if len(marks) == 0:
            return player.score.copy()  # no update

        if len(marks) > 1:
            raise InvalidScoreError()  # there must always be one mark

        mark = marks[0]

        if mark.factor != 1:
            raise InvalidScoreError()  # the factor must be 1

        if not mark.value:
            return player.score.copy()  # no update

        origin = self.value_to_index(player.score.value)
        target = self.value_to_index(mark.value)

        if target == -1:  # the target area must be a valid one
            raise InvalidScoreError()

        delta = target - origin

        if not 0 <= delta <= 3:  # as we throw 3 darts the max delta must be
            raise InvalidScoreError()

        return Score(value=mark.value, delta=delta)

    def check_winner(self) -> bool:
        for player in self.players:
            if player.score.value == self.config.targets[-1]:
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

        app_styles.config(self.button, 'RTC.PlayerBadge.label')
        app_styles.config(self.score, 'RTC.PlayerBadge.score')

        self.player.on('scores.append', self.update)
        self.player.on('scores.remove', self.update)
        self.player.on('scores.insert', self.update)
        self.player.on('scores.pop', self.update)
        self.player.on('scores.set', self.update)

        self.update()

    def target_text(self, target: int) -> str:
        if target == 0:
            return ''
        elif target == -1:
            return '?'
        elif target == 25:
            return 'BULL'
        else:
            return str(target)

    def update(self, *_, **__):
        """This will update the widget."""

        self.button.update()

        if self.player.scores:
            origin = self.player.score.value
            target = self.party.score_target(self.player.score)
            # ►
            self.score.config(text=f"{self.target_text(origin)}  →  {self.target_text(target)}")

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
                    key='RTC.PlayerBadge',
                    tag='selected' if player is next_player else ''
                )
                app_styles.config(
                    widget=badge.button,
                    key='RTC.PlayerBadge.label',
                    tag='selected' if player is next_player else ''
                )
            else:
                badge.destroy()

        self.update_idletasks()
