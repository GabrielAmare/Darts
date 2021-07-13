from abc import ABC
from typing import TypeVar, Generic, List

from darts.base import DictInterface
from darts.base_events import EmitterList, Emitter
from .BaseScore import BaseScore

_Score = TypeVar('_Score', bound=BaseScore)


class BasePlayer(Generic[_Score], DictInterface, Emitter, ABC):
    def __init__(self, name: str, scores: List[_Score] = None):
        super().__init__()
        self.name: str = name
        self.scores: EmitterList[_Score] = EmitterList(scores)
        self.scores.bind_to(emitter=self, prefix='scores')

    @property
    def score(self) -> _Score:
        return self.scores[-1]
