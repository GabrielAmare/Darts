import json
import random


def merge_in(d1: dict, d2: dict):
    """
        This will merge d2 into d1
        only handle dict|list|str typed values
    :param d1: the dict which will receive the update
    :param d2: the dict which will be merged
    :return: None
    """
    for key, val in d2.items():
        if key in d1:
            sub = d1[key]
            if isinstance(sub, dict):
                if isinstance(val, dict):
                    merge_in(sub, val)
                else:
                    raise Exception
            elif isinstance(sub, list):
                if isinstance(val, list):
                    sub.extend(val)
                elif isinstance(val, str):
                    sub.append(val)
                else:
                    raise Exception
            elif isinstance(sub, str):
                if isinstance(val, list):
                    d1[key] = [sub, *val]
                elif isinstance(val, str):
                    d1[key] = [sub, val]
                else:
                    raise Exception
        else:
            d1[key] = val


class MultiLang:
    def __init__(self, sep="."):
        self.data = {}

        self._callbacks = []

        self.sep = sep

    def load(self, fp, lang, add=False):
        with open(fp, mode="r", encoding="utf-8") as file:
            data = json.load(file)

        if add:
            merge_in(self.data, {lang: data})
        else:
            self.data = data

    def get(self, code, lang, rand=False, config=None):
        keys = code.split(self.sep)

        data = self.data.get(lang, {})

        for key in keys:
            data = data.get(key, {})

        if rand and isinstance(data, list):
            data = random.choice(data)

        if config and isinstance(data, str):
            for key, val in config.items():
                data = data.replace("<" + key + ">", str(val))

        return data

    def subscribe(self, callback: callable):
        self._callbacks.append(callback)

    def _on_change(self):
        for callback in self._callbacks:
            callback()
