from dataclasses import dataclass

from .O_Player import O_Player
from .base import Command


@dataclass
class SetWinner(Command):
    player: O_Player
