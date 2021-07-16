from __future__ import annotations

import random
from tkinter import *
from typing import Optional, List, Tuple

from darts.app_messages import app_messages
from darts.app_styles import app_styles
from darts.base_games import BasePlayer, BaseScore, BaseConfig, Game, BooleanOption, IntegerOption
from darts.constants import PartyState
from darts.core_commands import ScoreValue
from darts.core_games import BaseParty as BaseParty
from darts.core_gui.PlayerButton import PlayerButton
from darts.core_gui.ScoreBoard import ScoreBoard as BaseScoreBoard
from darts.errors import InvalidScoreError
from darts.functions import maximums_by

TARGETS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25]

GAME_CODE = 'TRAINING'


def get_value_factors(value: int) -> List[int]:
    if 1 <= value <= 20:
        return [1, 2, 3]
    elif value == 25:
        return [1, 2]
    else:
        raise ValueError(value)


class Config(BaseConfig):
    precise = BooleanOption(default=False)
    turns = IntegerOption(default=10, values=[5, 10, 20])
    targets = TARGETS


class Score(BaseScore):
    @classmethod
    def from_dict(cls, data: dict) -> Score:
        return cls(
            target_value=data['target_value'],
            target_factor=data['target_factor'],
            marks=list(map(tuple, data['marks'])),
            total=data['total'],
            delta=data['delta'],
        )

    def to_dict(self) -> dict:
        return dict(
            target_value=self.target_value,
            target_factor=self.target_factor,
            marks=list(map(list, self.marks)),
            total=self.total,
            delta=self.delta,
        )

    def __init__(self, target_value: int, target_factor: int, marks: List[Tuple[int, int]] = None, total: int = 0,
                 delta: int = 0):
        assert target_value in TARGETS
        assert target_factor in get_value_factors(target_value) or target_factor == -1
        super().__init__()
        self.target_value: int = target_value
        self.target_factor: int = target_factor
        self.marks: List[Tuple[int, int]] = marks or []
        self.total: int = total
        self.delta: int = delta

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.target_value!r}, {self.target_factor!r}, {self.marks!r}, {self.total!r}, {self.delta!r})"

    def copy(self) -> Score:
        return Score(
            target_value=self.target_value,
            target_factor=self.target_factor,
            marks=self.marks.copy(),
            total=self.total,
            delta=self.delta,
        )


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
        if len(score.marks) > 0:
            if score.delta == len(score.marks):
                self.announce('GLOBAL.PLAYER_MARKED_PERFECT')
            elif score.delta == 0:
                self.announce(f'{GAME_CODE}.PLAYER_IMPROVEMENT_INCENTIVES')

    def announce_player(self, player: Player):
        super().announce_player(player)

        target_value = player.score.target_value
        target_factor = player.score.target_factor

        if target_factor == -1:
            self.announce(
                f'{GAME_CODE}.ANNOUNCE_VALUE',
                value='BULL' if target_value == 25 else target_value,
            )
        else:
            factor_code = {
                1: 'SIMPLE',
                2: 'DOUBLE',
                3: 'TRIPLE'
            }[target_factor]

            self.announce(
                f'{GAME_CODE}.ANNOUNCE_FACTOR_VALUE',
                value='BULL' if target_value == 25 else target_value,
                factor=app_messages.translate(f'APP.FACTORS.{factor_code}')
            )

    def new_target(self) -> Tuple[int, int]:
        value = random.choice(self.config.targets)
        if self.config.precise:
            factor = random.choice(get_value_factors(value))
        else:
            factor = -1

        return value, factor

    def create_player(self, name: str) -> Player:
        return Player(name=name, scores=[])

    def initial_score(self, player: Player) -> Score:
        value, factor = self.new_target()

        return Score(
            target_value=value,
            target_factor=factor,
            marks=[],
        )

    def update_score(self, player: Player, marks: List[ScoreValue]) -> Score:
        if len(marks) == 0:
            return player.score.copy()  # no update

        if len(marks) > 3:
            raise InvalidScoreError()

        score_marks = []

        target_value = player.score.target_value
        target_factor = player.score.target_factor

        delta = 0

        for mark in marks:
            value, factor = mark.value, mark.factor

            if value == 0:
                continue

            if value not in self.config.targets:
                raise InvalidScoreError(
                    code='APP.ERRORS.INVALID_VALUE',
                    value=value
                )

            if factor not in get_value_factors(value):
                raise InvalidScoreError(
                    code='APP.ERRORS.INVALID_FACTOR_VALUE',
                    value=value,
                    factor='BULL' if factor == 25 else factor
                )

            score_marks.append((value, factor))

            if mark.value == target_value:
                if not self.config.precise or mark.factor == target_factor:
                    delta += 1

        if delta:
            target_value, target_factor = self.new_target()

        return Score(
            target_value=target_value,
            target_factor=target_factor,
            total=player.score.total + delta,
            delta=delta,
            marks=score_marks,
        )

    def check_winner(self) -> bool:
        if all(len(player.scores) >= self.config.turns for player in self.players):
            total, winners = maximums_by(self.players, lambda player: player.scores[self.config.turns - 1].total)
            self.set_winners(winners)
            return True

        else:
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

        app_styles.config(self.button, f'{GAME_CODE}.PlayerBadge.label')
        app_styles.config(self.score, f'{GAME_CODE}.PlayerBadge.score')

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
            target_value = self.player.score.target_value
            target_factor = self.player.score.target_factor
            # →
            if target_factor == -1:
                text = str(target_value)
            else:
                factor_code = {
                    1: 'SIMPLE',
                    2: 'DOUBLE',
                    3: 'TRIPLE'
                }[target_factor]
                text = f"{app_messages.translate(f'APP.FACTORS.{factor_code}')} {target_value}"

            self.score.config(text=f"► {text}")

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
                    key=f'{GAME_CODE}.PlayerBadge',
                    tag='selected' if player is next_player else ''
                )
                app_styles.config(
                    widget=badge.button,
                    key=f'{GAME_CODE}.PlayerBadge.label',
                    tag='selected' if player is next_player else ''
                )
            else:
                badge.destroy()

        self.update_idletasks()
