from dataclasses import dataclass

from .base import Command


@dataclass
class StartParty(Command):
    pass
