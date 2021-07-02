from dataclasses import dataclass
from typing import List

dc = dataclass


class Data:
    pass


@dc
class Command:
    pass


class PlayerData(Data):
    name: str

    def __init__(self, names: List[str]):
        self.name: str = "-".join(name.capitalize() for name in "-".join(names).split("-"))

    def __eq__(self, other):
        return type(self) is type(other) and self.name == other.name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"

    def __str__(self):
        return self.name


class ScoreData(Data):
    def __init__(self, value: int, factor: int = 1):
        self.value: int = value
        self.factor: int = factor

    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value and self.factor == other.factor

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value!r}, factor={self.factor!r})"

    def __str__(self):
        if self.factor == 1:
            f = ""
        elif self.factor == 2:
            f = "double "
        elif self.factor == 3:
            f = "triple "
        else:
            f = f"{self.factor!r} fois "

        if self.value == 0:
            return f"{f}{self.value!r}"
        elif self.value == 1:
            return f"{f}{self.value!r} point"
        else:
            return f"{f}{self.value!r} points"


@dc
class MainMenu(Command):
    def __str__(self):
        return "menu principal"


@dc
class OpenSettings(Command):
    def __str__(self):
        return "ouvrir les paramètres"


@dc
class Quit(Command):
    def __str__(self):
        return "quitter l'application"


@dc
class StartParty(Command):
    def __str__(self):
        return "démarrer la partie"


@dc
class AdjustMic(Command):
    seconds: int = 1

    def __str__(self):
        if self.seconds == 1:
            return f"ajuster le micro pendant {self.seconds} seconde"
        else:
            return f"ajuster le micro pendant {self.seconds} secondes"


@dc
class Redo(Command):
    times: int = 1

    def __str__(self):
        if self.times == 1:
            return "refaire"
        else:
            return f"refaire {self.times} fois"


@dc
class Undo(Command):
    times: int = 1

    def __str__(self):
        if self.times == 1:
            return "annuler"
        else:
            return f"annuler {self.times} fois"


@dc
class SelectPartyType(Command):
    name: str

    def __str__(self):
        return f"nouvelle partie de {self.name!s}"


@dc
class SetLang(Command):
    lang_IETF: str

    def __str__(self):
        return self.lang_IETF.split('-', 1)[0]


@dc
class AddPlayer(Command):
    player: PlayerData

    def __str__(self):
        return f"nouve(au/lle) joueu(r/se) : {self.player!s}"


@dc
class AddPlayers(Command):
    players: List[PlayerData]

    def __str__(self):
        return ", ".join(map(str, self.players[:-1])) + " et " + str(self.players[-1])


@dc
class AddScore(Command):
    scores: List[ScoreData]
    player: PlayerData = None

    @property
    def total(self):
        return sum(score.factor * score.value for score in self.scores)

    def __str__(self):
        if len(self.scores) == 1:
            return str(self.scores[0]) + " pour " + str(self.player)
        elif len(self.scores) > 1:
            return ", ".join(map(str, self.scores[:-1])) + " et " + str(self.scores[-1]) + " pour " + str(self.player)
        else:
            raise Exception


__all__ = (
    "Data", "Command",
    "PlayerData", "ScoreData",
    "MainMenu", "OpenSettings", "Quit", "StartParty",
    "AdjustMic", "Redo", "SelectPartyType", "SetLang", "Undo",
    "AddPlayer", "AddPlayers", "AddScore"
)
