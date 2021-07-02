from typing import List
from darts.commands import Command
from .O_Player import O_Player


class C_AddPlayers(Command):
    def __init__(self, players: List[O_Player]):
        self.players = players
