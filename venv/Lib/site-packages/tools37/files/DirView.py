from __future__ import annotations

import os
from abc import ABC
from typing import List, Type, TypeVar

from .DictInterface import DictInterface
from .FileView import FileView
from .JsonFileView import JsonFileView
from .PathView import PathView


class BaseDirView(PathView, ABC):
    def __init__(self, path: str):
        super().__init__(path)

        self.file_views: List[FileView] = []
        self.dir_views: List[DirView] = []

    def save(self) -> None:
        for file_view in self.file_views:
            file_view.save()

        for dir_view in self.dir_views:
            dir_view.save()

    def sub_path(self, name: str) -> str:
        return os.path.join(self.path, name)


J = TypeVar('J', bound=DictInterface)
D = TypeVar('D', bound=BaseDirView)


class DirView(BaseDirView, ABC):
    def __init__(self, path: str, force_create: bool = False):
        super().__init__(path)
        if force_create and not self.exists():
            os.mkdir(self.path)

    def load_json_file(self, name: str, factory: Type[J]) -> J:
        path = self.sub_path(name)
        file_view = JsonFileView(path, factory)
        file_view.load()
        self.file_views.append(file_view)
        return file_view.resource

    def load_dir(self, __name: str, __factory: Type[D], *args, **kwargs) -> D:
        path = self.sub_path(__name)
        dir_view = __factory(path, *args, **kwargs)
        dir_view.load()
        self.dir_views.append(dir_view)
        return dir_view

    def save_json_file(self, name: str, resource: J) -> None:
        path = self.sub_path(name)
        file_view = JsonFileView(path, resource.__class__, resource)
        file_view.save()
        self.file_views.append(file_view)
