from dataclasses import dataclass
from typing import List, Optional


class Command:
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k!s}={v!r}' for k, v in self.__dict__.items())})"


@dataclass
class PlayerName(Command):
    name: str


@dataclass
class PlayerNameCompound(PlayerName):
    def __init__(self, name1: str, name2: str):
        super().__init__(name1 + " " + name2)


@dataclass
class ScoreValue(Command):
    value: int
    factor: int = 1


@dataclass
class AddPlayer(Command):
    player: PlayerName


@dataclass
class AddPlayers(Command):
    players: List[PlayerName]


@dataclass
class AddScore(Command):
    scores: List[ScoreValue]
    player: Optional[PlayerName] = None

    @property
    def total(self):
        return sum(score.factor * score.value for score in self.scores)


@dataclass
class AdjustMic(Command):
    seconds: int = 1


@dataclass
class MainMenu(Command):
    pass


@dataclass
class OpenSettings(Command):
    pass


@dataclass
class Quit(Command):
    pass


@dataclass
class Redo(Command):
    times: int = 1


@dataclass
class SaveParty(Command):
    pass


@dataclass
class SelectPartyType(Command):
    name: str


@dataclass
class SetLang(Command):
    lang_IETF: str


@dataclass
class SetWinner(Command):
    player: PlayerName


@dataclass
class StartParty(Command):
    pass


@dataclass
class Undo(Command):
    times: int = 1
