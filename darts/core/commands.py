from dataclasses import dataclass
from typing import List

dc = dataclass


@dc
class Data:
    pass


@dc
class Command:
    pass


@dc
class PlayerData(Data):
    names: List[str]

    @property
    def name(self):
        return "-".join(self.names)


@dc
class ScoreData(Data):
    value: int
    factor: int = 1


@dc
class MainMenu(Command):
    pass


@dc
class OpenSettings(Command):
    pass


@dc
class Quit(Command):
    pass


@dc
class StartParty(Command):
    pass


@dc
class AdjustMic(Command):
    seconds: int = 1


@dc
class Redo(Command):
    times: int = 1


@dc
class SelectPartyType(Command):
    name: str


@dc
class SetLang(Command):
    lang_IETF: str


@dc
class Undo(Command):
    times: int = 1


@dc
class AddPlayer(Command):
    player: PlayerData


@dc
class AddPlayers(Command):
    players: List[PlayerData]


@dc
class AddScore(Command):
    scores: List[ScoreData]
    player: PlayerData = None

    @property
    def total(self):
        return sum(score.factor * score.value for score in self.scores)


__all__ = (
    "Data", "Command",
    "PlayerData", "ScoreData",
    "MainMenu", "OpenSettings", "Quit", "StartParty",
    "AdjustMic", "Redo", "SelectPartyType", "SetLang", "Undo",
    "AddPlayer", "AddPlayers", "AddScore"
)
