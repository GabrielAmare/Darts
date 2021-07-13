from dataclasses import dataclass

from darts.base_commands import Command


@dataclass
class SelectPartyType(Command):
    name: str
