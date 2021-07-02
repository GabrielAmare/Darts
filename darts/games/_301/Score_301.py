from typing import List
from models37 import *

from darts.classes import Score
from darts import commands as cmd


@Field.rpy("!score[int]",
           default=lambda target, **_: target.player.party.total,
           values=[v for v in range(0, 801 + 1) if v != 1]
           )
class Score_301(Score):
    def update(self, scores: List[cmd.ScoreValue]):
        delta = sum(score.factor * score.value for score in scores)
        new_score = self.score - delta
        return Score_301(player=self.player, index=self.index + 1, score=new_score)
