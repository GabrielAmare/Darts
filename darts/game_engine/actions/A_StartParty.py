from ...actions import Action


class A_StartParty(Action):
    def __init__(self, party):
        self.party = party

    def __repr__(self):
        return f"{self.__class__.__name__}({self.party.uid})"

    def do(self):
        self.party.started = True
        self.party.state = "__IN_GAME__"
        self.party.emit("start")

    def undo(self):
        self.party.emit("start:undo")
        self.party.state = "__PRE_GAME__"
        self.party.started = False

    redo = do
