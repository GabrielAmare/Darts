from dataclasses import dataclass

from .base import Command


@dataclass
class SelectPartyType(Command):
    name: str
