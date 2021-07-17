from abc import ABC
from typing import Generic, List, Type

from tools37.events import EmitterList

from darts.Profile import Profile
from darts.abstracts import AbstractPlayer, SCORE

from darts.app_data import app_data


class BasePlayer(Generic[SCORE], AbstractPlayer, ABC):
    score_cls: Type[SCORE]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            profile=app_data.profiles.find_profile_by_uuid(data['profile_uuid']),
            scores=list(map(cls.score_cls.from_dict, data['scores']))
        )

    def to_dict(self) -> dict:
        return dict(
            profile_uuid=self.profile.uuid,
            scores=[score.to_dict() for score in self.scores]
        )

    def __init__(self, profile: Profile, scores: List[SCORE] = None):
        super().__init__()
        self.profile: Profile = profile
        self.scores: EmitterList[SCORE] = EmitterList(scores)
        self.scores.bind_to(emitter=self, prefix='scores')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self.scores!r})"

    @property
    def score(self) -> SCORE:
        return self.scores[-1]

    @property
    def name(self) -> str:
        return self.profile.name
