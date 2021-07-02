from dataclasses import dataclass

from .base import Command


@dataclass
class Undo(Command):
    times: int = 1
