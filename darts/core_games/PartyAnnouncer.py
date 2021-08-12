from abc import ABC
from typing import TypeVar, Generic

from darts.actions import PlaySound
from darts.app_data import app_data
from darts.base_games import BaseConfig, BaseScore, BasePlayer
from .PartyActions import PartyActions

C = TypeVar('C', bound=BaseConfig)
P = TypeVar('P', bound=BasePlayer)
S = TypeVar('S', bound=BaseScore)


class PartyAnnouncer(Generic[C, P, S], PartyActions[C, P, S], ABC):
    def announce_start(self) -> None:
        if len(self.players) == 1:
            self.announce('APP.ANNOUNCES.GAME_START.ONE_PLAYER')
        else:
            self.announce('APP.ANNOUNCES.GAME_START.MANY_PLAYERS')

    def announce_score(self, player: P, score: S) -> None:
        app_data.logger.warning(f"Unimplemented announce_score method")

    def announce_player(self, player: P) -> None:
        self.announce('GLOBAL.ANNOUNCE_NEXT_PLAYER', name=player.name)

    def announce_end(self) -> None:
        if len(self.winners) == 0:
            self.announce('APP.ANNOUNCES.NO_WINNER')
        elif len(self.winners) == 1:
            self.announce('APP.ANNOUNCES.WINNER', name=self.winners[0].name)
            self.stack.append(PlaySound(party=self, sound='applause'))
        else:
            names = app_data.messages.translate(
                'APP.UTILS.AND',
                left=', '.join(player.name for player in self.winners[:-1]),
                right=self.winners[-1].name
            )
            self.announce('APP.ANNOUNCES.WINNERS', names=names)
            self.stack.append(PlaySound(party=self, sound='applause'))

    def announce_invalid_score(self, code: str = '', **config) -> None:
        self.announce(code or 'GLOBAL.INVALID_SCORE', **config)
