from darts.app_data import app_data
from darts.base_actions import Action
from darts.base_games import BaseParty


class PlaySound(Action):
    def __init__(self, party: BaseParty, sound: str):
        self.party: BaseParty = party
        self.sound: str = sound

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.sound!r})"

    def do(self) -> None:
        app_data.voice.play(f"assets/sounds/{self.sound}.mp3")
        app_data.logger.do(self)

    def undo(self) -> None:
        app_data.logger.undo(self)

    def redo(self) -> None:
        app_data.logger.redo(self)
