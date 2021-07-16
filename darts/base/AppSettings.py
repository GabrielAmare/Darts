from dataclasses import dataclass
from pathlib import Path

from .JsonInterface import JsonInterface
from .PartyFileData import PartyFileData


@dataclass
class AppSettings(JsonInterface):
    """Representation of the app settings."""

    fp: str = 'app_settings.json'
    messages_fp: str = 'assets/messages/'
    images_fp: str = 'assets/images/'
    exes_fp: str = 'assets/exes/'
    sounds_fp: str = 'assets/sounds/'
    engines_fp: str = 'darts/base_engines/'
    games_fp: str = f'{Path.home()}/Darts/games/'
    log_fp: str = 'darts_log'
    lang_IETF: str = 'fr-FR'

    pfd: PartyFileData = PartyFileData()

    @classmethod
    def from_dict(cls, data: dict):
        if 'pfd' in data:
            data['pfd'] = PartyFileData.from_dict(data['pfd'])

        return cls(**data)

    def to_dict(self) -> dict:
        data = self.__dict__.copy()
        data['pfd'] = data['pfd'].to_dict()
        return data

    @property
    def lang_ISO_639_1(self) -> str:
        return self.lang_IETF.split('-', 1)[0]
