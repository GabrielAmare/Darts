from ...actions import Action


class A_SetLastPlayer(Action):
    def __init__(self, party, name):
        self.party = party
        self.name = name

        self.player = None
        self.last = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.party.uid}, {repr(self.name)})"

    def do(self):
        self.last = self.party.last
        self.player = self.party.get_player(self.name)
        self.party.last = self.player

    def undo(self):
        self.party.last = self.last

    def redo(self):
        self.party.last = self.player
