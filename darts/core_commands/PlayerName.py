from dataclasses import dataclass

from darts.base_commands import Command


@dataclass
class PlayerName(Command):
    name: str
