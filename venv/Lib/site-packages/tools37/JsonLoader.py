from typing import List, Union, Iterable

from tools37.files import JsonFile


class JsonLoader:
    DEFAULT_SEPARATOR = "."

    class CodeNotFoundError(Exception):
        def __init__(self, code):
            self.code = code

    def __init__(self, data: dict = None, separator: str = DEFAULT_SEPARATOR):
        if data is None:
            data = {}
        self.data: dict = data
        self.separator: str = separator

    def path_to_keys(self, path: str) -> List[str]:
        return list(filter(len, path.split(self.separator)))

    def keys_to_path(self, keys: Iterable[str]) -> str:
        return self.separator.join(keys)

    def _go_at(self, keys: List[str], force_path: bool = False) -> Union[dict, str]:
        data = self.data
        for index, key in enumerate(keys):
            if force_path:
                data.setdefault(key, {})
            try:
                data = data[key]
            except KeyError:
                raise JsonLoader.CodeNotFoundError(".".join(keys))
        return data

    def export_file(self, fp: str, path: str = "") -> None:
        """Save a part of the data into a single file"""
        keys = self.path_to_keys(path)
        root = self._go_at(keys)
        JsonFile.save(fp, root)

    def import_file(self, fp: str, path: str = "") -> None:
        """Load a single file into the data"""
        data = JsonFile.load(fp)
        keys = self.path_to_keys(path)
        root = self._go_at(keys, force_path=True)

        def include(origin: dict, add: dict):
            for key, val in add.items():
                if isinstance(val, dict):
                    origin.setdefault(key, {})
                    include(origin[key], val)
                else:
                    origin[key] = val

        include(root, data)

    def get(self, *args: str) -> Union[dict, str]:
        path = self.keys_to_path(args)
        keys = self.path_to_keys(path)
        text = self._go_at(keys)
        return text
