from .base import Action


class A_InitScore(Action):
    def __init__(self, party, name, score_cls=None):
        self.party = party
        self.name = name

        if score_cls is None:
            self.score_cls = self.party.pack.score_cls
        else:
            self.score_cls = score_cls

        self.player = None
        self.score = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.party.uid}, {repr(self.name)}, {self.score_cls.__name__})"

    def do(self):
        self.player = self.party.get_player(self.name)

        self.score = self.score_cls(player=self.player, index=0)
        self.player.scores.append(self.score)

    def undo(self):
        self.player.scores.remove(self.score)

    def redo(self):
        self.player.scores.append(self.score)
