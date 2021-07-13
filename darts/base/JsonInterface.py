from abc import ABC
from typing import TypeVar, Type

from tools37 import JsonFile

from .DictInterface import DictInterface

E = TypeVar('E')


class JsonInterface(DictInterface, ABC):
    @classmethod
    def load(cls: Type[E], fp: str = '') -> E:
        """Load the party from a json file."""
        if JsonFile.exists(fp):
            data = JsonFile.load(fp)
        else:
            data = {}

        if fp:
            data['fp'] = fp

        return cls.from_dict(data)

    def save(self, fp: str = '') -> None:
        """Save the party to a json file."""
        if hasattr(self, 'fp'):
            fp = fp or self.fp
            setattr(self, 'fp', fp)

        data = self.to_dict()
        JsonFile.save(fp, data)
