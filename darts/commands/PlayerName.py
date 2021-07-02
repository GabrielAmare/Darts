from dataclasses import dataclass

from .base import Command


@dataclass
class PlayerName(Command):
    name: str
