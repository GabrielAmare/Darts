from ...actions import Action


class A_EndParty(Action):
    def __init__(self, party):
        self.party = party

    def __repr__(self):
        return f"{self.__class__.__name__}({self.party.uid})"

    def do(self):
        self.party.over = True
        self.party.state = "__POST_GAME__"
        self.party.emit("end")

    def undo(self):
        self.party.emit("end:undo")
        self.party.state = "__IN_GAME__"
        self.party.started = False

    redo = do
