from ...actions import Action


class A_AddScore(Action):
    def __init__(self, party, player, score):
        self.party = party
        self.player = player
        self.score = score

    def __repr__(self):
        return f"{self.__class__.__name__}({self.party.uid}, {repr(self.player.name)}, {repr(self.score)})"

    def do(self):
        self.player.scores.append(self.score)

    def undo(self):
        self.player.scores.remove(self.score)

    redo = do
