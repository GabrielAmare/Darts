from dataclasses import dataclass
from typing import List

from darts.base_commands import Command
from .PlayerName import PlayerName


@dataclass
class AddPlayers(Command):
    players: List[PlayerName]
