from typing import List
from datetime import datetime

from .functions import vocalize


class VocalError(Exception):
    def __init__(self, command=None):
        self.occured_at: datetime = datetime.now()
        self.command = command

    def vocalize(self):
        raise NotImplementedError

    def __str__(self):
        return f"\nERROR : {self.__class__.__qualname__}\n" + \
               "\n".join(f">>> {key} : {val!r}" for key, val in self.__dict__.items())


########################################################################################################################
# APP ERRORS
########################################################################################################################

class ListenError(VocalError):
    def vocalize(self):
        return vocalize("APP.DID_NOT_HEAR")


class TextNotFoundError(VocalError):
    def vocalize(self):
        return vocalize("APP.DID_NOT_HEAR")


class CommandNotFoundError(VocalError):
    def __init__(self, texts: List[str], command=None):
        super().__init__(command)
        self.texts: List[str] = texts

    def vocalize(self):
        return vocalize("APP.INVALID_COMMAND")


class UnhandledCommandType(VocalError):
    def vocalize(self):
        return vocalize("APP.UNHANDLED_COMMAND")


########################################################################################################################
# PARTY ERRORS
########################################################################################################################

class PartyNotStartedError(VocalError):
    def vocalize(self):
        return vocalize("GLOBAL.PARTY_NOT_STARTED")


class PartyAlreadyStartedError(VocalError):
    def vocalize(self):
        return vocalize("GLOBAL.PARTY_ALREADY_STARTED")


class PartyAlreadyOverError(VocalError):
    def vocalize(self):
        return vocalize("GLOBAL.PARTY_ALREADY_OVER")


class PlayerNotInParty(VocalError):
    def __init__(self, player_name: str, command=None):
        super().__init__(command)
        self.player_name: str = player_name

    def vocalize(self):
        return vocalize("GLOBAL.PLAYER_NOT_IN_PARTY", name=self.player_name)


class PlayerAlreadyInParty(VocalError):
    def __init__(self, player_name: str, command=None):
        super().__init__(command)
        self.player_name: str = player_name

    def vocalize(self):
        return vocalize("GLOBAL.PLAYER_ALREADY_IN_PARTY", name=self.player_name)


class PlayerNotFoundError(VocalError):
    def __init__(self, player_name: str, command=None):
        super().__init__(command)
        self.player_name = player_name

    def vocalize(self):
        return vocalize("GLOBAL.PLAYER_NOT_FOUND", name=self.player_name)


class InvalidScoreError(VocalError):
    def __init__(self, marks: int = None, command=None):
        super().__init__(command)
        self.marks: int = marks

    def vocalize(self):
        return vocalize("GLOBAL.INVALID_SCORE")
