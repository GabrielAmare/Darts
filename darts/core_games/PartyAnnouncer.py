from abc import ABC
from typing import TypeVar, Generic

from darts.app_logger import app_logger
from darts.base_games import BaseConfig, BaseScore, BasePlayer
from darts.core_actions import PlaySound
from .PartyActions import PartyActions

C = TypeVar('C', bound=BaseConfig)
P = TypeVar('P', bound=BasePlayer)
S = TypeVar('S', bound=BaseScore)


class PartyAnnouncer(Generic[C, P, S], PartyActions[C, P, S], ABC):
    def announce_start(self) -> None:
        self.announce('GLOBAL.GAME_START')

    def announce_score(self, player: P, score: S) -> None:
        app_logger.warning(f"Unimplemented announce_score method")

    def announce_player(self, player: P) -> None:
        self.announce('GLOBAL.ANNOUNCE_NEXT_PLAYER', name=player.name)

    def announce_end(self) -> None:
        if len(self.winners) == 0:
            self.announce('GLOBAL.GAME_OVER_NO_WINNER')
            self.stack.append(PlaySound(party=self, sound='applause'))
        elif len(self.winners) == 1:
            self.announce('GLOBAL.GAME_WON_BY', name=self.winners[0].name)
            self.stack.append(PlaySound(party=self, sound='applause'))
        else:
            raise NotImplementedError  # TODO : implement end message with multiple winners

    def announce_invalid_score(self) -> None:
        self.announce('GLOBAL.INVALID_SCORE')
