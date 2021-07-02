from .base import Action


class SetWinner(Action):
    def __init__(self, party, winner):
        self.party = party
        self.winner = winner

    def __repr__(self):
        return f"{self.__class__.__name__}({self.party.uid!r}, {self.winner!r})"

    def do(self):
        self.party.winner = self.winner

    def undo(self):
        self.party.winner = None

    def redo(self):
        self.party.winner = self.winner
