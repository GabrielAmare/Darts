from dataclasses import dataclass

from darts.base_commands import Command


@dataclass
class Quit(Command):
    pass