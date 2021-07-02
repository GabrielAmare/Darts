from .base import Action


class A_AddPlayer(Action):
    def __init__(self, party, name):
        self.party = party
        self.name = name

        self.player = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.party.uid}, {repr(self.name)})"

    def do(self):
        self.player = self.party.Player(party=self.party, name=self.name)
        self.party.players.append(self.player)

    def undo(self):
        self.party.players.remove(self.player)

    def redo(self):
        self.party.players.append(self.player)
