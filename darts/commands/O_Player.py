from dataclasses import dataclass

from .base import Command


@dataclass
class O_Player(Command):
    name: str
