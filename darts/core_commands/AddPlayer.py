from dataclasses import dataclass

from darts.base_commands import Command
from .PlayerName import PlayerName


@dataclass
class AddPlayer(Command):
    player: PlayerName
