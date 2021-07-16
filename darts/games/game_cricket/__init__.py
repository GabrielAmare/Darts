from __future__ import annotations

from tkinter import *
from typing import Optional, List, Dict, Tuple

from darts.app_messages import app_messages
from darts.app_styles import app_styles
from darts.base_games import BasePlayer, BaseScore, BaseConfig, Game, IntegerOption, StringOption
from darts.base_gui.Label import Label
from darts.constants import PartyState
from darts.core_commands import ScoreValue
from darts.core_games import BaseParty as BaseParty
from darts.core_gui.PlayerButton import PlayerButton
from darts.core_gui.ScoreBoard import ScoreBoard as BaseScoreBoard
from darts.errors import InvalidScoreError

CLASSIC_DOORS: List[int] = [15, 16, 17, 18, 19, 20, 25]
MINIMAL_DOORS: List[int] = [1, 2, 3, 4, 5, 6, 7, 8]


class Config(BaseConfig):
    marks_to_open = IntegerOption(default=3, values=[1, 2, 3, 4, 5, 6])
    marks_to_close = IntegerOption(default=3, values=[1, 2, 3, 4, 5, 6])
    doors_type = StringOption(default='classic', values=['classic', 'minimal'])

    @property
    def doors(self) -> List[int]:
        if self.doors_type == 'classic':
            return CLASSIC_DOORS
        elif self.doors_type == 'minimal':
            return MINIMAL_DOORS
        else:
            raise ValueError(self.doors_type)


class Score(BaseScore):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            value=data['value'],
            doors={int(key): int(val) for key, val in data['doors'].items()},
            has_opened=data['has_opened'],
            has_closed=data['has_closed'],
            delta=data['delta'],
        )

    def to_dict(self) -> dict:
        return dict(
            value=self.value,
            doors=self.doors,
            has_opened=self.has_opened,
            has_closed=self.has_closed,
            delta=self.delta,
        )

    def __init__(self,
                 value: int,
                 doors: Dict[int, int],
                 has_opened: List[int],
                 has_closed: List[int],
                 delta: int = 0
                 ):
        super().__init__()
        self.value = value
        self.doors = doors
        self.has_opened = has_opened or []
        self.has_closed = has_closed or []
        self.delta = delta

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r}, {self.doors!r}, {self.has_opened!r}, {self.has_closed!r}, {self.delta!r})"


class Player(BasePlayer[Score]):
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data['name'],
            scores=list(map(Score.from_dict, data['scores']))
        )

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            scores=list(map(Score.to_dict, self.scores))
        )

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

    def opener(self, door: int) -> Optional[Player]:
        for player in self.players:
            for score in player.scores:
                if door in score.has_opened:
                    return player

    def closer(self, door: int) -> Optional[Player]:
        for player in self.players:
            for score in player.scores:
                if door in score.has_closed:
                    return player

    @staticmethod
    def door_to_text(door: int) -> str:
        if door == 25:
            return "BULL"
        else:
            return str(door)

    @classmethod
    def doors_to_text(cls, doors: List[int]) -> Tuple[str, str]:
        *doors, last = doors
        return ", ".join(map(cls.door_to_text, doors)), cls.door_to_text(last)

    def announce_score(self, player: Player, score: Score) -> None:
        if score.delta > 0:
            self.announce("GLOBAL.PLAYER_MARKED", name=player.name, marks=score.delta)

        if score.has_opened:
            if len(score.has_opened) == 1:
                self.announce("CRICKET.DOOR_OPENED", door=self.door_to_text(score.has_opened[0]))
            else:
                doors, last = self.doors_to_text(score.has_opened)
                text = app_messages.translate('APP.UTILS.AND', left=doors, right=last)
                self.announce("CRICKET.DOORS_OPENED", doors=text)

        if score.has_closed:
            if len(score.has_closed) == 1:
                self.announce("CRICKET.DOOR_CLOSED", door=self.door_to_text(score.has_closed[0]))
            else:
                doors, last = self.doors_to_text(score.has_closed)
                text = app_messages.translate('APP.UTILS.AND', left=doors, right=last)
                self.announce("CRICKET.DOORS_CLOSED", doors=text)

    def create_player(self, name: str) -> Player:
        return Player(name=name)

    def initial_score(self, player: Player) -> Score:
        return Score(
            value=0,
            doors={door: 0 for door in self.config.doors},
            has_opened=[],
            has_closed=[],
            delta=0
        )

    def update_score(self, player: Player, marks: List[ScoreValue]) -> Score:
        score = player.score

        doors: Dict[int, int] = score.doors.copy()
        has_opened: List[int] = []
        has_closed: List[int] = []

        delta = 0

        for mark in marks:
            door, count = mark.value, mark.factor

            if door not in self.config.doors:
                raise InvalidScoreError()

            closer = self.closer(door)

            # DOOR ALREADY CLOSED
            if closer:
                continue

            opener = self.opener(door)

            # ADD POINTS
            if player is opener:
                doors[door] += count
                delta += door * count
                continue

            old_marks = doors[door]
            new_marks = old_marks + count

            # TRY TO CLOSE THE DOOR
            if opener:
                if new_marks >= self.config.marks_to_close:
                    doors[door] = self.config.marks_to_close
                    has_closed.append(door)
                else:
                    doors[door] += count

                continue

            # TRY TO OPEN THE DOOR
            if new_marks >= self.config.marks_to_open:
                has_opened.append(door)
                delta += door * (new_marks - self.config.marks_to_open)
                doors[door] += count
                continue

            # ADD MARKS
            doors[door] += count

        return Score(
            value=score.value + delta,
            doors=doors,
            has_opened=has_opened,
            has_closed=has_closed,
            delta=delta
        )

    def check_winner(self) -> bool:
        greater_score = max(player.score.value for player in self.players)
        players = [player for player in self.players if player.score.value == greater_score]

        if len(players) == 1:
            if all(self.opener(door) is players[0] or self.closer(door) for door in self.config.doors):
                self.set_winners(players)
                return True

        elif all(self.closer(door) for door in self.config.doors):
            self.set_winners(players)
            return True

        else:
            return False


game = Game(config_cls=Config, party_cls=Party, player_cls=Player, score_cls=Score)


class ScoreBoard(BaseScoreBoard[Config, Party, Player, Score]):
    def __init__(self, root, party: Party):
        super().__init__(root, party)

        self.door_column = [
            Label(self, code="CRICKET.SCOREBOARD.DOORS"),
            *[
                Label(self, text='BULL' if door == 25 else str(door))
                for door in self.party.config.doors
            ],
            Label(self, code="CRICKET.SCOREBOARD.TOTAL")
        ]
        self.player_columns = []

        for player in self.party.players:
            self.on_players_append(player)

        self.update()

    def new_player_column(self, player: Player) -> List[Widget]:
        player.on('scores.append', self.update)
        player.on('scores.remove', self.update)
        player.on('scores.insert', self.update)
        player.on('scores.pop', self.update)
        player.on('scores.set', self.update)

        return [
            PlayerButton(self, party=self.party, player=player),
            *[
                Label(self, text='')
                for _ in self.party.config.doors
            ],
            Label(self, text='')
        ]

    def on_players_append(self, player: Player):
        widgets = self.new_player_column(player)
        self.player_columns.append(widgets)
        self.update()

    def on_players_remove(self, player: Player):
        self.update()

    def on_players_insert(self, index: int, player: Player):
        widgets = self.new_player_column(player)
        self.player_columns.insert(index, widgets)
        self.update()

    def on_players_pop(self, index: int, player: Player):
        widgets = self.player_columns.pop(index)
        self.update()

    def on_players_set(self, index: int, player: Player):
        widgets = self.new_player_column(player)
        self.player_columns[index] = widgets
        self.update()

    def update_style(self):
        opener = {door: self.party.opener(door) for door in self.party.config.doors}
        closer = {door: self.party.closer(door) for door in self.party.config.doors}

        app_styles.config(self.door_column[0], 'Cricket.ScoreBoard.DoorLabel', '')

        for door, widget in zip(self.party.config.doors, self.door_column[1:-1]):
            if closer[door]:
                app_styles.config(widget, 'Cricket.ScoreBoard.DoorLabel', 'closed')
            elif opener[door]:
                app_styles.config(widget, 'Cricket.ScoreBoard.DoorLabel', 'opened')
            else:
                app_styles.config(widget, 'Cricket.ScoreBoard.DoorLabel', '')

        app_styles.config(self.door_column[-1], 'Cricket.ScoreBoard.DoorLabel', '')

        for player, widgets in zip(self.party.players, self.player_columns):
            app_styles.config(widgets[0], 'Cricket.ScoreBoard.PlayerName')
            widgets[0].update()

            for door, widget in zip(self.party.config.doors, widgets[1:-1]):
                if closer[door]:
                    if player is opener[door]:
                        app_styles.config(widget, 'Cricket.ScoreBoard.Player', 'opener-closed')
                    else:
                        app_styles.config(widget, 'Cricket.ScoreBoard.Player', 'closed')
                elif player is opener[door]:
                    app_styles.config(widget, 'Cricket.ScoreBoard.Player', 'opener')
                else:
                    app_styles.config(widget, 'Cricket.ScoreBoard.Player', '')

            app_styles.config(widgets[-1], 'Cricket.ScoreBoard.PlayerTotal')

    def update(self, *_, **__):
        for column in range(len(self.party.players) + 1):
            self.grid_columnconfigure(column, weight=1)

        for row in range(len(self.party.config.doors) + 2):
            self.grid_rowconfigure(row, weight=1)

        self.update_style()

        opener = {door: self.party.opener(door) for door in self.party.config.doors}
        closer = {door: self.party.closer(door) for door in self.party.config.doors}

        if len(self.player_columns) == 2:
            data = [self.player_columns[0], self.door_column, self.player_columns[1]]
        else:
            data = [self.door_column, *self.player_columns]

        for column, widgets in enumerate(data):
            for row, label in enumerate(widgets):
                self.grid_at(label, row=row, column=column)

        for player, widgets in zip(self.party.players, self.player_columns):
            for door, widget in zip(self.party.config.doors, widgets[1:-1]):
                if player.scores:
                    if player is closer[door]:
                        widget.config(text=self.party.config.marks_to_close * 'I')
                    elif player is opener[door]:
                        value = door * (player.score.doors[door] - self.party.config.marks_to_open)
                        widget.config(text=str(value))
                    else:
                        widget.config(text=player.score.doors[door] * 'I')

                    widgets[-1].config(text=str(player.score.value))
                else:
                    widgets[-1].config(text='0')

        self.update_idletasks()
