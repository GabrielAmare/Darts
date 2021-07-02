from darts.classes import *
from .Score_Cricket import Score_Cricket


class Party_Cricket(Party):
    DOORS = (15, 16, 17, 18, 19, 20, 25)
    Score = Score_Cricket
    verbose_prefixes = ["GLOBAL", "CRICKET"]

    @property
    def scores_in_order(self):
        return sorted(
            [score for player in self.players for score in player.scores],
            key=lambda score: (score.index, score.player.index)
        )

    def opener(self, door):
        for score in self.scores_in_order:
            if score.get_marks(door) >= Score_Cricket.OPEN_DOOR:
                return score.player

    def closer(self, door):
        opener = None
        for score in self.scores_in_order:
            if score.get_marks(door) >= Score_Cricket.OPEN_DOOR:
                if opener:
                    if opener is not score.player:
                        return score.player
                else:
                    opener = score.player

    def is_opener(self, door, player):
        return self.opener(door) is player

    def is_closer(self, door, player):
        return self.closer(door) is player

    def is_opened(self, door):
        return self.opener(door) is not None and self.closer(door) is None

    def is_closed(self, door):
        return self.closer(door) is not None

    def on_add_score(self, command: C_AddScore):
        player_and_score = self.on_add_score_before(command)
        if not player_and_score:
            return
        player, score = player_and_score

        if score.delta > 0:
            self.vocal_feedback("PLAYER_MARKED", name=player.name, marks=score.delta)

        to_str_door = lambda door: "boule" if door == 25 else str(door)

        if score.has_opened:
            if len(score.has_opened) == 1:
                self.vocal_feedback("DOOR_OPENED", door=to_str_door(score.has_opened[0]))
            else:
                *ds, d = score.has_opened
                self.vocal_feedback("DOORS_OPENED", doors=", ".join(map(to_str_door, ds)) + " et " + to_str_door(d))

        if score.has_closed:
            if len(score.has_closed) == 1:
                self.vocal_feedback("DOOR_CLOSED", door=to_str_door(score.has_closed[0]))
            else:
                *ds, d = score.has_closed
                self.vocal_feedback("DOORS_CLOSED", doors=", ".join(map(to_str_door, ds)) + " et " + to_str_door(d))

        self.on_add_score_after(player)

    def player_with_greater_score(self):
        get_score = lambda player: player.scores[-1].score if player.scores else 0
        max_score = max(map(get_score, self.players), default=0)
        players = []
        for player in self.players:
            if get_score(player) == max_score:
                players.append(player)

        if len(players) == 1:
            return players[0]

    def all_doors_closed_or_opened_by(self, player):
        return all(
            self.is_closed(door) or self.is_opener(door, player)
            for door in self.DOORS
        )

    def all_doors_closed(self):
        return all(
            self.is_closed(door)
            for door in self.DOORS
        )

    def update_winner(self):
        player = self.player_with_greater_score()
        if player:
            if self.all_doors_closed_or_opened_by(player):
                self.set_winner(player)
        elif self.all_doors_closed():
            self.set_winner(None)
