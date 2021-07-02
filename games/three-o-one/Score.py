from typing import List
from darts.game_materials import *


@Field.rpy("!score[int]",
           default=lambda target, **_: target.player.party.total,
           values=[v for v in range(0, 801 + 1) if v != 1]
           )
class Score(BaseScore):
    def update(self, scores: List[O_Score]):
        delta = sum(score.factor * score.value for score in scores)
        new_score = self.score - delta
        return Score(player=self.player, index=self.index + 1, score=new_score)
