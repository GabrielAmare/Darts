from darts.commands import Command


class SetWinner(Command):
    def __init__(self, player):
        self.player = player
