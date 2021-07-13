from abc import ABC
from typing import Type, TypeVar

from tools37 import JsonFile

from darts.base import DictInterface

C = TypeVar('C')


class BaseConfig(DictInterface, ABC):
    @classmethod
    def load(cls: Type[C], fp: str) -> C:
        """Load the config from a json file"""
        if JsonFile.exists(fp):
            data = JsonFile.load(fp)
        else:
            data = {}
        return cls.from_dict(data)

    def save(self, fp: str) -> None:
        """Save the config to a json file"""
        data = self.to_dict()
        JsonFile.save(fp, data)
