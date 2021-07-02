from darts.commands import Command
from .O_Player import O_Player


class AddPlayer(Command):
    def __init__(self, player: O_Player):
        self.player = player
