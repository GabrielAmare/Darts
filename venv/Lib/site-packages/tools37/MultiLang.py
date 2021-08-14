import os
from typing import Union, List

from .JsonLoader import JsonLoader


class MultiLang:
    @classmethod
    def from_data(cls, data: dict):
        return cls(data=data)

    def __init__(self, data: Union[dict, JsonLoader] = None, lang: str = ""):
        if data is None:
            data = {}

        if isinstance(data, dict):
            data = JsonLoader(data)

        self._callbacks: List[callable] = []
        self.lang: str = lang
        self.data_holder: JsonLoader = data

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value
        for callback in self._callbacks:
            callback()

    def load_lang_file(self, fp: str, lang: str = None):
        if lang is None:
            lang = os.path.splitext(os.path.basename(fp))[0]

        self.data_holder.import_file(fp, lang)

    def save_langs(self, dp: str = os.curdir, category: str = ""):
        if not os.path.exists(dp):
            os.mkdir(dp)
        for lang in self.data_holder.data.keys():
            root = self.data_holder.keys_to_path([lang, category]) if category else lang
            self.data_holder.export_file(os.path.join(dp, lang), root)

    def load_langs(self, dp: str = os.curdir, category: str = ""):
        for fn in os.listdir(dp):
            fp = os.path.join(dp, fn)
            lang = os.path.splitext(fn)[0]
            root = self.data_holder.keys_to_path([lang, category]) if category else lang
            self.data_holder.import_file(fp, root)

    def get(self, path: str, safe: bool = False) -> str:
        try:
            return self.data_holder.get(self.lang, path)
        except JsonLoader.CodeNotFoundError as e:
            if safe:
                return e.code
            else:
                raise e

    __getitem__ = get

    def subscribe(self, callback: callable):
        self._callbacks.append(callback)
        return lambda: (callback in self._callbacks) and self._callbacks.remove(callback)
