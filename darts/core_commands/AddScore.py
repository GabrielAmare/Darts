from dataclasses import dataclass
from typing import List, Optional

from darts.base_commands import Command
from .PlayerName import PlayerName
from .ScoreValue import ScoreValue


@dataclass
class AddScore(Command):
    scores: List[ScoreValue]
    player: Optional[PlayerName] = None

    @property
    def total(self):
        return sum(score.factor * score.value for score in self.scores)
