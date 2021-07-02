from dataclasses import dataclass

from .base import Command


@dataclass
class AdjustMic(Command):
    seconds: int = 1
