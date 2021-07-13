from darts.app_logger import app_logger
from darts.base_actions import Action
from darts.base_games import BaseParty
from darts.app_voice import app_voice
from darts.app_settings import app_settings


class PlaySound(Action):
    def __init__(self, party: BaseParty, sound: str):
        self.party: BaseParty = party
        self.sound: str = sound

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.sound!r})"

    def do(self) -> None:
        app_voice.play(app_settings.sounds_fp + self.sound + '.mp3')
        app_logger.do(self)

    def undo(self) -> None:
        app_logger.undo(self)

    def redo(self) -> None:
        app_logger.redo(self)
