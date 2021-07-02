from darts.commands import Command


class Undo(Command):
    def __init__(self, times: int = 1):
        self.times = times
