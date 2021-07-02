from dataclasses import dataclass

from .base import Command


@dataclass
class Redo(Command):
    times: int = 1
