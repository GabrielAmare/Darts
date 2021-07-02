from dataclasses import dataclass

from .base import Command


@dataclass
class O_Score(Command):
    value: int
    factor: int = 1
