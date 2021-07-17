from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterator, Type

from tools37.events import EmitterList, Emitter

from darts.Profile import Profile
from darts.abstracts import AbstractParty, CONFIG, PLAYER, SCORE
from darts.commands import *
from darts.constants import PartyState
from darts.errors import PlayerNotFoundError
from darts.functions import expr_match_ratio, maximums_by


class BaseParty(Generic[CONFIG, PLAYER, SCORE], AbstractParty, ABC):
    config_cls: Type[CONFIG]
    player_cls: Type[PLAYER]

    @classmethod
    def from_dict(cls, data: dict) -> BaseParty:
        return cls(
            uid=data['uid'],
            config=cls.config_cls.from_dict(data['config']),
            players=list(map(cls.player_cls.from_dict, data['players'])),
            latest=data['latest'],
            state=data['state'],
            winners=data['winners']
        )

    def to_dict(self) -> dict:
        return dict(
            uid=self.uid,
            config=self.config.to_dict(),
            players=[player.to_dict() for player in self.players],
            latest=self.latest.name if self.latest else '',
            state={
                PartyState.BEFORE: 'BEFORE',
                PartyState.DURING: 'DURING',
                PartyState.AFTER: 'AFTER',
            }[self.state],
            winners=[player.name for player in self.winners]
        )

    def __init__(self,
                 uid: int,
                 config: CONFIG,
                 players: List[PLAYER] = None,
                 latest: str = '',
                 winners: List[str] = None,
                 state: str = 'BEFORE'):
        Emitter.__init__(self)
        self.uid: int = uid
        self.config: CONFIG = config
        self.players: EmitterList[PLAYER] = EmitterList(players)
        self.players.bind_to(emitter=self, prefix='players')

        self.latest: Optional[PLAYER] = self.get_player_by_name(latest) if self.players and latest else None
        self.winners: List[PLAYER] = [self.get_player_by_name(name) for name in winners or []]

        self.state: PartyState = {
            'BEFORE': PartyState.BEFORE,
            'DURING': PartyState.DURING,
            'AFTER': PartyState.AFTER,
        }[state]

    def __repr__(self):
        return f"Party(...)"

    @property
    def state(self) -> PartyState:
        return self._state

    @state.setter
    def state(self, value: PartyState):
        self._state = value
        self.emit('state.set', value)

    @property
    def latest(self) -> PLAYER:
        return self._latest

    @latest.setter
    def latest(self, value: PLAYER):
        self._latest = value
        self.emit('latest.set', value)

    def players_to(self, player: PLAYER) -> Iterator[PLAYER]:
        """Return the list of players that needs to play before it comes to `player`."""
        if len(self.players) and player in self.players:
            next_player = self.get_next_player()

            while next_player is not player:
                yield next_player
                next_player = self.get_player_after(next_player)

    def get_player_by_closest_name(self, name: str, __ratio=0.75) -> PLAYER:
        """Return the player with the most corresponding name. (if it has more than 75% match ratio)"""
        print([player.profile for player in self.players])
        max_ratio, players = maximums_by(self.players, lambda player: expr_match_ratio(name, player.name))

        if max_ratio >= __ratio and len(players) == 1:
            return players[0]

        raise PlayerNotFoundError(name=name)

    def get_player_by_name(self, name: str) -> PLAYER:
        """Return the player with the corresponding name."""
        for player in self.players:
            if player.name == name:
                return player

        else:
            return self.get_player_by_closest_name(name)

    def get_player_by_index(self, index: int) -> PLAYER:
        """Return the player at the corresponding index."""
        return self.players[index % len(self.players)]

    def get_latest_player(self) -> Optional[PLAYER]:
        """Get the latest player to play."""
        try:
            return self.get_player_by_index(self.players.index(self.latest))
        except ValueError:
            return None

    def get_player_after(self, player: PLAYER) -> Optional[PLAYER]:
        """Get the player that plays after the specified one."""
        try:
            return self.get_player_by_index(self.players.index(player) + 1)
        except ValueError:
            return None

    def get_player_before(self, player: PLAYER) -> Optional[PLAYER]:
        """Get the player that plays after the specified one."""
        try:
            return self.get_player_by_index(self.players.index(player) - 1)
        except ValueError:
            return None

    def get_next_player(self) -> PLAYER:
        """Get the next player to play."""
        return self.get_player_after(self.latest)

    def set_next_player(self, player: PLAYER) -> None:
        self.latest = self.get_player_before(player)

    @abstractmethod
    def create_player(self, profile: Profile) -> PLAYER:
        """Create a Player instance."""

    @abstractmethod
    def initial_score(self, player: PLAYER) -> SCORE:
        """Create an initial score for the player."""

    @abstractmethod
    def update_score(self, player: PLAYER, marks: List[ScoreValue]) -> SCORE:
        """Update the score of a player"""

    @abstractmethod
    def check_winner(self) -> bool:
        """Check is the game have been won."""
