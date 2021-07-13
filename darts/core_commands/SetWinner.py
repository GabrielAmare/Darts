from dataclasses import dataclass

from darts.base_commands import Command
from .PlayerName import PlayerName


@dataclass
class SetWinner(Command):
    player: PlayerName
