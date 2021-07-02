from dataclasses import dataclass

from .base import Command
from .PlayerName import PlayerName


@dataclass
class AddPlayer(Command):
    player: PlayerName
