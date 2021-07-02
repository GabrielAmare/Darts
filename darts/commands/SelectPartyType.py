from darts.commands import Command


class SelectPartyType(Command):
    def __init__(self, name: str):
        self.name = name
