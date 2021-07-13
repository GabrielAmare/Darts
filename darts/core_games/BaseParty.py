from abc import ABC
from typing import TypeVar, Generic

from darts.base_games import BaseConfig, BaseScore, BasePlayer
from .PartyCommands import PartyCommands

C = TypeVar('C', bound=BaseConfig)
P = TypeVar('P', bound=BasePlayer)
S = TypeVar('S', bound=BaseScore)


class BaseParty(Generic[C, P, S], PartyCommands[C, P, S], ABC):
    pass
