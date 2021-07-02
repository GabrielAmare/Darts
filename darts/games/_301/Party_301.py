from darts.classes import *
from .Score_301 import Score_301


@Field.rpy("!total[int]", values=[301, 501, 801], default=301)
class Party_301(Party):
    Score = Score_301
    verbose_prefixes = ["GLOBAL", "_301"]

    def update_winner(self):
        for player in self.players:
            if player.scores and player.scores[-1].score == 0:
                return self.set_winner(player)

    def on_add_score(self, command: C_AddScore):
        marks = command.total
        if marks > 180:
            raise InvalidScoreError(marks)

        player_and_score = self.on_add_score_before(command)
        if not player_and_score:
            return
        player, score = player_and_score

        if marks > 0:
            self.vocal_feedback("PLAYER_MARKED", name=player.name, marks=marks)

            if marks <= 10 and score.score >= 40:
                self.vocal_feedback("PLAYER_MARKED_POORLY", name=player.name, marks=marks)
            elif marks == 180:
                self.vocal_feedback("PLAYER_MARKED_PERFECT")
            elif marks >= 100:
                self.vocal_feedback("PLAYER_MARKED_GOOD")

        self.on_add_score_after(player)

    def on_next_player(self, player):
        score = player.scores[-1].score

        if score <= 170:
            self.vocal_feedback("ANNOUNCE_REMAINING_SCORE", score=score)

            if score == 42:
                self.vocal_feedback("ANNOUNCE_42")
            elif score == 50:
                self.vocal_feedback("ANNOUNCE_50")
            elif score <= 40 and score % 2 == 0:
                self.vocal_feedback("ANNOUNCE_DOUBLE_TO_WIN", half_score=int(score // 2))
