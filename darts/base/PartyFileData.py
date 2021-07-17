from dataclasses import dataclass

from .DictInterface import DictInterface


@dataclass
class PartyFileData(DictInterface):
    game_uid: str = ''
    party_uid: int = 0

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            game_uid=data['game_uid'],
            party_uid=data['party_uid']
        )

    def to_dict(self) -> dict:
        return dict(
            game_uid=self.game_uid,
            party_uid=self.party_uid
        )

    def __str__(self):
        return f"{self.game_uid}:{self.party_uid}"

    def __bool__(self):
        return bool(self.game_uid) and bool(self.party_uid)
