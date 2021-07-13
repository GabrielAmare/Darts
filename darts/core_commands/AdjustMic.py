from dataclasses import dataclass

from darts.base_commands import Command


@dataclass
class AdjustMic(Command):
    seconds: int = 1
