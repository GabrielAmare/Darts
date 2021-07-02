from dataclasses import dataclass

from .base import Command


@dataclass
class Quit(Command):
    pass
