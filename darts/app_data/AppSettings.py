from dataclasses import dataclass

from darts.base.DictInterface import DictInterface
from darts.base.PartyFileData import PartyFileData
from darts.constants import HOME


@dataclass
class AppSettings(DictInterface):
    """Representation of the app settings."""

    lang_IETF: str = 'fr-FR'
    user_files: str = HOME

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
