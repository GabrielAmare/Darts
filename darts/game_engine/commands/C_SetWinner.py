from darts.commands import Command


class C_SetWinner(Command):
    def __init__(self, player):
        self.player = player
