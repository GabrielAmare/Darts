from darts.classes import *
from .Score_Alcoholic import Score_Alcoholic, score_data

VALUES = list(range(0, 21)) + [25]


@Field.rpy("!total[int]", values=[301, 501, 801], default=301)
class Party_Alcoholic(Party):
    Score = Score_Alcoholic
    verbose_prefixes = ["ALCOHOLIC", "GLOBAL"]

    def update_winner(self):
        pass

    def on_add_score(self, command: cmd.AddScore):
        if len(command.scores) != 1:
            return self.vocal_feedback("INVALID_SCORE")

        score = command.scores[0]

        if score.value not in VALUES:
            return self.vocal_feedback("INVALID_SCORE")

        if score.factor not in [1, 2, 3]:
            return self.vocal_feedback("INVALID_SCORE")

        player_and_score = self.on_add_score_before(command)
        if not player_and_score:
            return
        player, player_score = player_and_score

        data = score_data(score.value, score.factor)

        if data["take"]["shot"]:
            self.vocal_feedback("PLAYER_TAKE_SHOT", name=player.name)
        if data["give"]["shot"]:
            self.vocal_feedback("PLAYER_GIVE_SHOT", name=player.name)
        if data["elie"]["shot"]:
            self.vocal_feedback("ELIE_TAKE_SHOT")

        if data["take"]["sips"]:
            self.vocal_feedback("PLAYER_TAKE_SIPS", name=player.name, number=data["take"]["sips"])
        if data["give"]["sips"]:
            self.vocal_feedback("PLAYER_GIVE_SIPS", name=player.name, number=data["give"]["sips"])
        if data["elie"]["sips"]:
            self.vocal_feedback("ELIE_TAKE_SIP")

        if data["everyone"]:
            self.vocal_feedback("EVERYBODY_DRINKS", number=data["everyone"])

        self.on_add_score_after(player)

    def on_next_player(self, player):
        self.vocal_feedback("PLAY_AS")
