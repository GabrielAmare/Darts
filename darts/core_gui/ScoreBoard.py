from abc import ABC, abstractmethod
from tkinter import *
from typing import Generic, TypeVar

from darts.base_games import BasePlayer, BaseConfig, BaseScore
from darts.constants import PartyState
from darts.core_games import BaseParty

PA = TypeVar('PA', bound=BaseParty)
PL = TypeVar('PL', bound=BasePlayer)
CO = TypeVar('CO', bound=BaseConfig)
SC = TypeVar('SC', bound=BaseScore)


class ScoreBoard(Generic[CO, PA, PL, SC], Frame, ABC):
    def __init__(self, root, party: PA):
        super().__init__(root)

        self.party: PA = party

        self.party.on('players.append', self.on_players_append)
        self.party.on('players.remove', self.on_players_remove)
        self.party.on('players.insert', self.on_players_insert)
        self.party.on('players.pop', self.on_players_pop)
        self.party.on('players.set', self.on_players_set)

        self.bind_all('<KeyPress-Right>', self.on_right_keypress)
        self.bind_all('<KeyPress-Left>', self.on_left_keypress)

    def on_right_keypress(self, _evt):
        """Handle the keyboard RIGHT arrow press, which select the next player."""
        if self.party.state is PartyState.DURING:
            prev_player = self.party.get_player_after(self.party.latest)
            self.party.set_latest_player(prev_player.name)
            self.party.do()

    def on_left_keypress(self, _evt):
        """Handle the keyboard LEFT arrow press, which select the previous player."""
        if self.party.state is PartyState.DURING:
            prev_player = self.party.get_player_before(self.party.latest)
            self.party.set_latest_player(prev_player.name)
            self.party.do()

    @abstractmethod
    def on_players_append(self, player: PL) -> None:
        """Event handler of self.party.players.append"""

    @abstractmethod
    def on_players_remove(self, player: PL) -> None:
        """Event handler of self.party.players.remove"""

    @abstractmethod
    def on_players_insert(self, index: int, player: PL) -> None:
        """Event handler of self.party.players.insert"""

    @abstractmethod
    def on_players_pop(self, index: int, player: PL) -> None:
        """Event handler of self.party.players.pop"""

    @abstractmethod
    def on_players_set(self, index: int, player: PL) -> None:
        """Event handler of self.party.players.set"""

    def grid_at(self, widget: Widget, row: int, column: int, sticky=NSEW, **config):
        """Force the widget to the specified grid row-column if it's not grided there."""
        if widget not in self.grid_slaves(row, column):
            widget.grid(row=row, column=column, sticky=sticky, **config)
