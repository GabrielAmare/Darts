from darts.classes import *
from .Score_Molkky import Score_Molkky


@Field.rpy("!rule_killer[str]", default="killer", values=["no-killer", "killer", "auto-killer", "kamikaze"])
@Field.rpy("!rule_dropdown[str]", default="level-25", values=["level-0", "level-25"])
@Field.rpy("!rule_elimination[str]", default="elimination-3",
           values=["no-elimination", "elimination-3", "elimination-dropdown"])
class Party_Molkky(Party):
    Score = Score_Molkky
    verbose_prefixes = ["GLOBAL", "MOLKKY"]

    def update_winner(self):
        if len(self.players) == 1:
            return self.set_winner(self.players[0])
        elif len(self.players) == 0:
            return self.set_winner(None)

        for player in self.players:
            if player.scores and player.scores[-1].score == 50:
                return self.set_winner(player)

    def on_add_score(self, command: C_AddScore):
        marks = command.total

        player_and_score = self.on_add_score_before(command)
        if not player_and_score:
            return
        player, score = player_and_score

        if marks >= 0:
            self.vocal_feedback("PLAYER_MARKED", name=player.name, marks=marks)

        self.on_add_score_after(player)

    def on_next_player(self, player):
        score = player.scores[-1]

        if score.dropdown:
            self.vocal_feedback("ANNOUNCE_DROPDOWN", score=score.score)

        if score.kills:
            for player in score.kills:
                self.vocal_feedback("ANNOUNCE_KILL", score=player.scores[-1].score, name=player.name)
