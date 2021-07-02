from dataclasses import dataclass
from typing import List, Optional

from .base import Command
from .O_Player import O_Player
from .O_Score import O_Score


@dataclass
class AddScore(Command):
    scores: List[O_Score]
    player: Optional[O_Player] = None

    @property
    def total(self):
        return sum(score.factor * score.value for score in self.scores)
