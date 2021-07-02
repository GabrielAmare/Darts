from dataclasses import dataclass
from typing import List

from .base import Command
from .PlayerName import PlayerName


@dataclass
class AddPlayers(Command):
    players: List[PlayerName]
