from __future__ import annotations

import os
from typing import Iterator, TypeVar, List, Type

from tools37.files import DictInterface, DirView

E = TypeVar('E', bound=DictInterface)


class JsonFilesManager(DirView):
    def __init__(self, path: str, factory: Type[E]):
        super().__init__(path, force_create=True)
        self.factory: Type[E] = factory
        self.uids: List[int] = []

    def file_exists(self, file_name: str) -> bool:
        """Return True if the file exists."""
        file_path = self.sub_path(file_name)
        return os.path.exists(file_path) and os.path.isfile(file_path)

    def get_all_json_file_names(self) -> Iterator[str]:
        """Return all the json file names present in the directory."""
        for file_name in os.listdir(self.path):
            file_path = self.sub_path(file_name)
            if os.path.isfile(file_path):
                base_name, extension = os.path.splitext(file_name)
                if extension == '.json':
                    yield base_name

    def new_uid(self) -> int:
        uid = 1
        while uid in self.uids:
            uid += 1
        self.uids.append(uid)
        return uid

    def load(self) -> None:
        for file_name in os.listdir(self.path):
            file_path = self.sub_path(file_name)
            if os.path.isfile(file_path):
                base_name, extension = os.path.splitext(file_name)
                if extension == '.json':
                    if base_name.isnumeric():
                        uid = int(base_name)
                        self.uids.append(uid)
                        self.load_json_file(file_name, self.factory)

    def load_file(self, name: str) -> E:
        return self.load_json_file(name, self.factory)
