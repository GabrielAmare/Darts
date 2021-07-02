from typing import List

from models37 import *

from darts.classes import Score, InvalidScoreError
from darts import commands as cmd


@Field.rpy("!score[int]", default=0)
@Field.rpy("!door_15[int]", default=0)
@Field.rpy("!door_16[int]", default=0)
@Field.rpy("!door_17[int]", default=0)
@Field.rpy("!door_18[int]", default=0)
@Field.rpy("!door_19[int]", default=0)
@Field.rpy("!door_20[int]", default=0)
@Field.rpy("!door_25[int]", default=0)
@Field.rpy("*has_opened[int]")
@Field.rpy("*has_closed[int]")
@Field.rpy("!delta[int]", default=0)
class Score_Cricket(Score):
    OPEN_DOOR = 3

    def get_marks(self, door):
        return getattr(self, f"door_{door}")

    def get_score(self, door):
        assert door in self.party.DOORS
        return door * (self.get_marks(door) - self.OPEN_DOOR)

    def update(self, scores: List[cmd.ScoreValue]):
        items = [(score.value, score.factor) for score in scores]

        data = dict(
            player=self.player,
            index=self.index + 1,
            score=self.score,
            door_15=self.door_15,
            door_16=self.door_16,
            door_17=self.door_17,
            door_18=self.door_18,
            door_19=self.door_19,
            door_20=self.door_20,
            door_25=self.door_25,
            has_opened=[],
            has_closed=[],
            delta=0
        )

        for door, count in items:
            if door not in self.party.DOORS:
                raise InvalidScoreError

            key = f"door_{door}"
            marks = data[key]
            new_marks = marks + count

            opener = self.party.opener(door)
            closer = self.party.closer(door)

            closed = closer is not None
            opened = opener is not None

            neutral = not opened
            opened_by_player = self.player is opener
            opened_by_other = opened and not opened_by_player

            if opened_by_other:
                new_marks = min(new_marks, self.OPEN_DOOR)

            if not closed and marks < new_marks:
                data[key] = new_marks

                if new_marks >= self.OPEN_DOOR:
                    if opened_by_player:
                        data["delta"] += count * door
                    elif neutral:
                        data["has_opened"].append(door)
                        data["delta"] += (new_marks - self.OPEN_DOOR) * door
                    elif opened_by_other:
                        data["has_closed"].append(door)

        data["score"] = data["score"] + data["delta"]

        return Score_Cricket(**data)
