from abc import ABC
from typing import TypeVar, Generic, List, Type

from darts.base import DictInterface
from darts.base_events import EmitterList, Emitter
from .BaseScore import BaseScore

S = TypeVar('S', bound=BaseScore)


class BasePlayer(Generic[S], DictInterface, Emitter, ABC):
    score_cls: Type[S]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data['name'],
            scores=list(map(cls.score_cls.from_dict, data['scores']))
        )

    def to_dict(self) -> dict:
        return dict(name=self.name, scores=[score.to_dict() for score in self.scores])

    def __init__(self, name: str, scores: List[S] = None):
        super().__init__()
        self.name: str = name
        self.scores: EmitterList[S] = EmitterList(scores)
        self.scores.bind_to(emitter=self, prefix='scores')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self.scores!r})"

    @property
    def score(self) -> S:
        return self.scores[-1]
