from dataclasses import dataclass

from tools37.files import DictInterface

from darts.constants import HOME


@dataclass
class AppSettings(DictInterface):
    """Representation of the app settings."""

    lang_IETF: str = 'fr-FR'
    user_files: str = HOME

    loaded_game: str = ''
    loaded_party: int = 0

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self) -> dict:
        return self.__dict__

    @property
    def lang_ISO_639_1(self) -> str:
        return self.lang_IETF.split('-', 1)[0]
