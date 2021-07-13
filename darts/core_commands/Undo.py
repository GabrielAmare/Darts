from dataclasses import dataclass

from darts.base_commands import Command


@dataclass
class Undo(Command):
    times: int = 1
