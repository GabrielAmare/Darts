from typing import List


class NothingToUndoError(Exception):
    pass


class NothingToRedoError(Exception):
    pass


class InvalidCommandTypeError(Exception):
    pass


class ListenError(Exception):
    pass


class TextNotFoundError(Exception):
    pass


class CommandNotFoundError(Exception):
    def __init__(self, texts: List[str]):
        self.texts: List[str] = texts


class UnhandledCommand(Exception):
    def __init__(self, command: object):
        self.command: object = command


class PartyNotStartedError(Exception):
    pass


class PartyAlreadyStartedError(Exception):
    pass


class PartyAlreadyOverError(Exception):
    pass


class PlayerNotFoundError(Exception):
    def __init__(self, name: str):
        self.name: str = name


class PlayerAlreadyExistsError(Exception):
    def __init__(self, name: str):
        self.name: str = name


class InvalidScoreError(Exception):
    def __init__(self, marks: int = None, code: str = '', **config):
        self.marks: int = marks
        self.code: str = code
        self.config: dict = config


class PartyConfigurationMissingError(Exception):
    pass
