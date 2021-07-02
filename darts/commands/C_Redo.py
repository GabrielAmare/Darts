from darts.commands import Command


class C_Redo(Command):
    def __init__(self, times: int = 1):
        self.times = times
