from dataclasses import dataclass

from darts.base_commands import Command


@dataclass
class Redo(Command):
    times: int = 1
