from typing import List
from darts.game_materials import *

KILLER_RULES = ["no-killer", "killer", "auto-killer", "kamikaze"]
DROP_DOWN_RULES = ["level-0", "level-25"]
ELIMINATION_RULES = ["no-elimination", "elimination-3", "elimination-dropdown"]


@Field.rpy("!score[int]",
           default=lambda target, **_: 0,
           values=[v for v in range(0, 50 + 1)]
           )
@Field.rpy("!delta[int]", default=1)
@Field.rpy("!errors[int]", default=0, values=[0, 1, 2, 3])
@Field.rpy("!dropdown[bool]", default=False)
@Field.rpy("!eliminate[bool]", default=False)
@Field.rpy("*kills[Player]")
class Score(BaseScore):
    def drop_down_value(self):
        rule_dropdown = self.party.rule_dropdown
        if rule_dropdown == "level-25":
            return 25 if self.score >= 25 else 0
        elif rule_dropdown == "level-0":
            return 0
        else:
            raise ValueError(rule_dropdown, DROP_DOWN_RULES)

    def drop_down(self, kills=None, errors=None):
        if kills is None:
            kills = []
        if errors is None:
            errors = self.errors
        new = Score(
            player=self.player,
            index=self.index + 1,
            score=self.drop_down_value(),
            delta=-1,
            dropdown=True,
            kills=kills,
            errors=errors
        )
        return new

    def elimination(self, errors=None):
        if errors is None:
            errors = self.errors
        return Score(
            player=self.player,
            index=self.index + 1,
            score=0,
            delta=-1,
            eliminate=True,
            errors=errors
        )

    def update(self, scores: List[O_Score]):
        delta = sum(score.factor * score.value for score in scores)
        new_score = self.score + delta

        rule_killer = self.party.rule_killer
        rule_elimination = self.party.rule_elimination

        if rule_killer not in KILLER_RULES:
            raise ValueError(rule_killer, KILLER_RULES)

        if rule_elimination == "elimination-3":
            if delta == 0:
                errors = self.errors + 1
            else:
                errors = 0

            if errors == 3:
                if rule_elimination == "elimination-3":
                    self.party.players.remove(self.player)
                    return self.elimination(errors=errors)
                elif rule_elimination == "elimination-dropdown":
                    return self.drop_down(errors=errors)
        else:
            errors = self.errors

        if rule_killer != "no-killer":
            kills = [
                player
                for player in self.party.players
                if player is not self.player and len(player.scores) and player.scores[-1].score == new_score
            ]

            if kills:
                if rule_killer in ("killer", "kamikaze"):
                    for player in kills:
                        new = player.scores[-1].drop_down()
                        player.scores.append(new)

                if rule_killer in ("auto-killer", "kamikaze"):
                    return self.drop_down(kills=kills, errors=errors)

        return Score(
            player=self.player,
            index=self.index + 1,
            score=new_score,
            delta=delta,
            errors=errors
        )
