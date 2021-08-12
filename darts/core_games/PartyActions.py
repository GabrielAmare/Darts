from abc import ABC
from typing import TypeVar, Generic, Iterator, List

from darts.actions import StartParty, AddScore, SetLastPlayer, AddPlayer, InitScore, SetWinners, EndParty, Announce
from darts.base_actions import ActionHandler
from darts.base_games import BaseConfig, BaseScore, BasePlayer, BaseParty
from darts.constants import TextMode

C = TypeVar('C', bound=BaseConfig)
P = TypeVar('P', bound=BasePlayer)
S = TypeVar('S', bound=BaseScore)


class PartyActions(Generic[C, P, S], BaseParty[C, P, S], ActionHandler, ABC):
    def __init__(self, *args, **kwargs):
        BaseParty.__init__(self, *args, **kwargs)
        ActionHandler.__init__(self)

    def announce(self, code: str, **config) -> None:
        """Set up the actions to announce something."""
        self.stack.append(Announce(party=self, code=code, mode=TextMode.RANDOM, config=config))

    def start_party(self) -> None:
        """Set up the actions to start a party."""
        self.stack.append(StartParty(party=self))

    def set_score(self, player: P, score: S) -> None:
        """Set up the actions to set the score of a player."""
        self.stack.append(AddScore(party=self, player=player, score=score))
        self.stack.append(SetLastPlayer(party=self, name=player.name))

    def skip_player(self, player: P) -> None:
        """Set up the action to skip the player."""
        self.set_score(player, self.update_score(player, []))

    def add_score(self, player: P, score: S) -> None:
        """Set up the actions to set the score of a player (skipping the other)."""
        for skip in self.players_to(player):
            self.skip_player(skip)
        self.set_score(player, score)

    def set_latest_player(self, name: str) -> None:
        """Set up the actions to set the latest player."""
        self.stack.append(SetLastPlayer(party=self, name=name))

    def add_player(self, name: str) -> None:
        """Set up the actions to add a new player."""
        self.stack.append(AddPlayer(party=self, name=name))
        self.stack.append(InitScore(party=self, name=name))
        self.set_latest_player(name)

    def add_players(self, names: Iterator[str]) -> None:
        """Set up the actions to add multiple players and start the party."""
        for name in names:
            self.add_player(name)
        self.start_party()

    def set_winners(self, players: List[P]) -> None:
        """Set up the actions to defined the winners of the party."""
        self.stack.append(SetWinners(party=self, players=players))
        self.stack.append(EndParty(party=self))
