from darts.commands import Command


class O_Player(Command):
    def __init__(self, name: str):
        self.name = name
