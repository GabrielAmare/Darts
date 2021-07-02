from typing import List
from darts.commands import Command
from .O_Score import O_Score
from .O_Player import O_Player


class AddScore(Command):
    def __init__(self, scores: List[O_Score], player: O_Player = None):
        self.player = player
        self.scores = scores

    @property
    def total(self):
        return sum(score.factor * score.value for score in self.scores)
