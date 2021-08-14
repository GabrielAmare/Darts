from abc import ABC
from typing import TypeVar, Generic

from .DictInterface import DictInterface
from .FileView import FileView
from .JsonFile import JsonFile

E = TypeVar('E', bound=DictInterface)


class JsonFileView(FileView[E], Generic[E], ABC):
    def load(self) -> None:
        try:
            data = JsonFile.load(self.path)
        except FileNotFoundError:
            data = {}

        self.resource = self.factory.from_dict(data)

    def save(self) -> None:
        if isinstance(self.resource, self.factory):
            data = self.resource.to_dict()
            JsonFile.save(self.path, data)
