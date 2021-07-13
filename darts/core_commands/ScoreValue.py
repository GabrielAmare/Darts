from dataclasses import dataclass

from darts.base_commands import Command


@dataclass
class ScoreValue(Command):
    value: int
    factor: int = 1
