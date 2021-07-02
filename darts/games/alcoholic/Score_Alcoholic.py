from typing import List
from models37 import *

from darts.classes import Score
from darts.game_engine import O_Score


def score_data(value: int, factor: int) -> dict:
    data = {
        "give": {
            "shot": False,
            "sips": 0
        },
        "take": {
            "shot": False,
            "sips": 0
        },
        "elie": {
            "shot": False,
            "sips": False
        },
        "everyone": 0
    }

    if value in [0, 1]:
        data["take"]["shot"] = True
    elif value in [2, 3, 4, 5, 6, 7, 8, 9]:
        data["take"]["sips"] = factor
    elif value in [10]:
        data["everyone"] = factor
    elif value in [11, 12, 13, 14, 15, 16, 17, 18, 19]:
        data["give"]["sips"] = factor
    elif value in [20]:
        data["give"]["shot"] = True
    elif value in [25]:
        if factor == 1:
            data["elie"]["sips"] = True
        elif factor == 2:
            data["elie"]["shot"] = True

    return data


@Field.rpy("!shots_took[int]", default=0)
@Field.rpy("!sips_took[int]", default=0)
@Field.rpy("!shots_given[int]", default=0)
@Field.rpy("!sips_given[int]", default=0)
@Field.rpy("!score[int]", default=0)
class Score_Alcoholic(Score):
    def update(self, scores: List[O_Score]):
        assert len(scores) == 1
        score = scores[0]
        data = score_data(score.value, score.factor)

        return Score_Alcoholic(
            player=self.player,
            index=self.index + 1,
            shots_took=self.shots_took + data["take"]["shot"],
            sips_took=self.sips_took + data["take"]["sips"] + data["everyone"],
            shots_given=self.shots_given + data["give"]["shot"] + data["elie"]["shot"],
            sips_given=self.sips_given + data["give"]["sips"] + data["elie"]["sips"] + data["everyone"] * len(self.party.players),
        )
