from darts.commands import Command


class O_Score(Command):
    def __init__(self, value: int, factor: int = 1):
        self.value = value
        self.factor = factor
