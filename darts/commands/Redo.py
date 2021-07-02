from darts.commands import Command


class Redo(Command):
    def __init__(self, times: int = 1):
        self.times = times
