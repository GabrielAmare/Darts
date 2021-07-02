from darts.commands import Command


class C_Undo(Command):
    def __init__(self, times: int = 1):
        self.times = times
