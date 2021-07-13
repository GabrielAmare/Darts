from abc import ABC
from typing import List, Iterator

from .Action import Action


class ActionSequence(ABC):
    def __init__(self, *actions: Action):
        self.actions: List[Action] = list(actions)

    def __iter__(self) -> Iterator[Action]:
        return iter(self.actions)

    def __len__(self) -> int:
        return len(self.actions)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(map(repr, self.actions))})"
