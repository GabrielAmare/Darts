from dataclasses import dataclass
from typing import List

from .base import Command
from .O_Player import O_Player


@dataclass
class AddPlayers(Command):
    players: List[O_Player]
