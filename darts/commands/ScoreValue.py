from dataclasses import dataclass

from .base import Command


@dataclass
class ScoreValue(Command):
    value: int
    factor: int = 1
