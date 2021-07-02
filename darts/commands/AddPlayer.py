from dataclasses import dataclass

from .base import Command
from .O_Player import O_Player


@dataclass
class AddPlayer(Command):
    player: O_Player
