from abc import ABC, abstractmethod
from typing import TypeVar

from tools37 import EmitterList
from tools37.events import Emitter
from tools37.files import DictInterface


class AbstractProfile(DictInterface, ABC):
    pass


class AbstractConfig(DictInterface, ABC):
    @abstractmethod
    def copy(self):
        """Return a copy of the configuration."""


class AbstractParty(Emitter, DictInterface, ABC):
    pass


class AbstractPlayer(Emitter, DictInterface, ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the player."""

    scores: EmitterList
    profile: AbstractProfile


class AbstractScore(Emitter, DictInterface, ABC):
    pass


CONFIG = TypeVar('CONFIG', bound=AbstractConfig)
PARTY = TypeVar('PARTY', bound=AbstractParty)
SCORE = TypeVar('SCORE', bound=AbstractScore)
PLAYER = TypeVar('PLAYER', bound=AbstractPlayer)
