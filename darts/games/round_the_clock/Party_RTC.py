from darts.classes import *
from .Score_RTC import Score_RTC


class Party_RTC(Party):
    Score = Score_RTC
    verbose_prefixes = ["GLOBAL", "RTC"]

    def update_winner(self):
        for player in self.players:
            if player.scores and player.scores[-1].score == 25:
                return self.set_winner(player)

    def on_add_score(self, command: C_AddScore):
        try:
            player_and_score = self.on_add_score_before(command)
        except InvalidScoreError:
            return self.vocal_feedback("INVALID_SCORE")

        if not player_and_score:
            return
        player, score = player_and_score

        marks = command.total
        if marks == 3:
            self.vocal_feedback("PLAYER_MARKED_PERFECT")

        self.on_add_score_after(player)

    def on_next_player(self, player):
        target = player.scores[-1].target

        self.vocal_feedback("ANNOUNCE_TARGET", target="boule" if target == 25 else target)
