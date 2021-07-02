from dataclasses import dataclass

from .PlayerName import PlayerName
from .base import Command


@dataclass
class SetWinner(Command):
    player: PlayerName
