from dataclasses import dataclass
from typing import List

dc = dataclass(frozen=True, order=True)


@dc
class PlayerData:
    names: List[str]

    @property
    def name(self):
        return "-".join(self.names)


@dc
class ScoreData:
    value: int
    factor: int = 1
