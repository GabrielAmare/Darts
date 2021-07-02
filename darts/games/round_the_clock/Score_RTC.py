from typing import List

from models37 import *

from darts.classes import Score, InvalidScoreError
from darts import commands as cmd


@Field.rpy("!score[int]", default=0, values=[*range(0, 21), 25])
class Score_RTC(Score):
    def update(self, scores: List[cmd.O_Score]):
        assert len(scores) == 1, scores
        score = scores[0]
        new_goal = score.value

        if new_goal is None:
            new_goal = self.score
        diff = min(new_goal, 21) - min(self.score, 21)  # resume 25 to 21 so the diff is valid

        if not 0 <= diff <= 3:
            raise InvalidScoreError

        return Score_RTC(player=self.player, index=self.index + 1, score=new_goal)

    @property
    def target(self):
        if self.score == 20:
            return 25
        else:
            return self.score + 1
