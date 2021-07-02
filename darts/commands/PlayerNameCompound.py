from dataclasses import dataclass

from .PlayerName import PlayerName


@dataclass
class PlayerNameCompound(PlayerName):
    def __init__(self, name1: str, name2: str):
        super().__init__(name1 + " " + name2)
