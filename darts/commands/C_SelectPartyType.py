from darts.commands import Command


class C_SelectPartyType(Command):
    def __init__(self, name: str):
        self.name = name
