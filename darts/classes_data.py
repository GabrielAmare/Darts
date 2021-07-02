from __future__ import annotations

from typing import Optional, List, Type
from darts.vocal_errors import PlayerAlreadyInParty, PlayerNotInParty

from darts.utils import CommandHandler, command_method, ActionHandler, action_method


class Player:
    def __init__(self, party: Party, name: str, scores: List[Score] = None):
        self.party: Party = party
        self.name: str = name
        self.scores: List[Score] = scores or []

    @property
    def pack(self):
        return self.party.pack

    @property
    def index(self):
        return self.party.players.index(self)


class Score:
    def __init__(self, player: Player, value: int):
        self.player: Player = player
        self.value: int = value

    @property
    def pack(self):
        return self.player.pack

    @property
    def index(self):
        return self.player.scores.index(self)

    @property
    def party(self):
        return self.player.party


class Party(CommandHandler, ActionHandler):
    def __init__(self,
                 pack: GamePack,
                 players: List[Player] = None,
                 started: bool = False,
                 over: bool = False,
                 last: Player = None,
                 winner: Player = None):
        self.pack: GamePack = pack
        self.players: List[Player] = players or []
        self.started: bool = started
        self.over: bool = over
        self.last: Optional[Player] = last
        self.winner: Optional[Player] = winner

    def index_to_player(self, index: int) -> Player:
        """
            Get the player corresponding to the specified ``index``
            indexes that are not in range are bringed back to range
        """
        return self.players[index % len(self.players)]

    def players_to_skip_to(self, player: Player):
        """
            Iterate over the players that needs to play before it comes to `player`
        """
        if player not in self.players:
            raise PlayerNotInParty(player.name)

        if not self.players:
            return []

        index = self.last.index + 1 if self.last else 0

        c_player = self.index_to_player(index)

        while self.index_to_player(index) is not player:
            yield c_player
            index += 1
            c_player = self.index_to_player(index)

    def append_player(self, player: Player):
        if player in self.players:
            raise PlayerAlreadyInParty(player.name)

        self.players.append(player)

    def remove_player(self, player: Player):
        if player in self.players:
            raise PlayerNotInParty(player.name)

        self.players.append(player)


class GamePack:
    def __init__(self,
                 player_cls: Type[Player],
                 score_cls: Type[Score],
                 party_cls: Type[Party]):
        self.player_cls: Type[Player] = player_cls
        self.score_cls: Type[Score] = score_cls
        self.party_cls: Type[Party] = party_cls

    def new_party(self):
        return self.party_cls(pack=self)
