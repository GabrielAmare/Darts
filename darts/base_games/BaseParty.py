from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Iterator

from darts import core_commands as cmd
from darts.base import JsonInterface
from darts.base_events import EmitterList, Emitter
from darts.constants import PartyState
from darts.errors import PlayerNotFoundError
from darts.functions import expr_match_ratio, maximums_by
from .BaseConfig import BaseConfig
from .BasePlayer import BasePlayer
from .BaseScore import BaseScore

C = TypeVar('C', bound=BaseConfig)
S = TypeVar('S', bound=BaseScore)
P = TypeVar('P', bound=BasePlayer)


class BaseParty(Generic[C, P, S], Emitter, JsonInterface, ABC):
    def __init__(self, config: C, players: List[P] = None, latest: str = '', state: str = 'BEFORE', winners: List[str] = None):
        Emitter.__init__(self)
        self.config: C = config
        self.players: EmitterList[P] = EmitterList(players)
        self.players.bind_to(emitter=self, prefix='players')

        self.latest: Optional[P] = self.get_player_by_name(latest) if self.players and latest else None
        self.winners: List[P] = [self.get_player_by_name(name) for name in winners or []]

        self.state: PartyState = {
            'BEFORE': PartyState.BEFORE,
            'DURING': PartyState.DURING,
            'AFTER': PartyState.AFTER,
        }[state]

    @property
    def state(self) -> PartyState:
        return self._state

    @state.setter
    def state(self, value: PartyState):
        self._state = value
        self.emit('state.set', value)

    @property
    def latest(self) -> P:
        return self._latest

    @latest.setter
    def latest(self, value: P):
        self._latest = value
        self.emit('latest.set', value)

    def players_to(self, player: P) -> Iterator[P]:
        """Return the list of players that needs to play before it comes to `player`."""
        if len(self.players) and player in self.players:
            next_player = self.get_next_player()

            while next_player is not player:
                yield next_player
                next_player = self.get_player_after(next_player)

    def get_player_by_closest_name(self, name: str, __ratio=0.75) -> P:
        """Return the player with the most corresponding name. (if it has more than 75% match ratio)"""
        max_ratio, players = maximums_by(self.players, lambda player: expr_match_ratio(name, player.name))

        if max_ratio >= __ratio and len(players) == 1:
            return players[0]

        raise PlayerNotFoundError(name=name)

    def get_player_by_name(self, name: str) -> P:
        """Return the player with the corresponding name."""
        for player in self.players:
            if player.name == name:
                return player

        else:
            return self.get_player_by_closest_name(name)

    def get_player_by_index(self, index: int) -> P:
        """Return the player at the corresponding index."""
        return self.players[index % len(self.players)]

    def get_latest_player(self) -> Optional[P]:
        """Get the latest player to play."""
        try:
            return self.get_player_by_index(self.players.index(self.latest))
        except ValueError:
            return None

    def get_player_after(self, player: P) -> Optional[P]:
        """Get the player that plays after the specified one."""
        try:
            return self.get_player_by_index(self.players.index(player) + 1)
        except ValueError:
            return None

    def get_player_before(self, player: P) -> Optional[P]:
        """Get the player that plays after the specified one."""
        try:
            return self.get_player_by_index(self.players.index(player) - 1)
        except ValueError:
            return None

    def get_next_player(self) -> P:
        """Get the next player to play."""
        return self.get_player_after(self.latest)

    def set_next_player(self, player: P) -> None:
        self.latest = self.get_player_before(player)

    @abstractmethod
    def create_player(self, name: str) -> P:
        """Create a Player instance."""

    @abstractmethod
    def initial_score(self, player: P) -> S:
        """Create an initial score for the player."""

    @abstractmethod
    def update_score(self, player: P, marks: List[cmd.ScoreValue]) -> S:
        """Update the score of a player"""

    @abstractmethod
    def check_winner(self) -> bool:
        """Check is the game have been won."""
