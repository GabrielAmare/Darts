import json
from .DictSerializable import DictSerializable


class JsonSerializable(DictSerializable):
    @classmethod
    def from_dict(cls, data: dict):
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_json(cls, fp: str) -> None:
        with open(fp, mode='r', encoding='utf-8') as file:
            data = json.load(file)
        return cls.from_dict(data)

    def to_json(self, fp: str) -> None:
        data = self.to_dict()
        with open(fp, mode='r', encoding='utf-8') as file:
            json.dump(data, file)
