"""
    Config objects are just regular objects with implementation of some events
"""
import os
import json


class Config:
    data: dict
    _callbacks: dict
    ALLOW_OVERWRITE: bool = False

    def __init__(self, data: dict = None):
        """
            Create a Config object allowing to load/save from/to json files
            also dynamic, when you change some properties of the config,
            objects can subscribe to these changes
        :param data: optional initial data for the config
        """
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise TypeError(type(data))
        self.data = data
        self._callbacks = {}

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.data)})"

    def load(self, fp: str) -> None:
        """
            Load the config from the given json filepath
        :param fp: json filepath
        :return: None
        """
        if not isinstance(fp, str):
            raise TypeError(type(fp))

        if not fp.endswith(".json"):
            fp = fp + ".json"

        if not os.path.exists(fp):
            raise FileNotFoundError(fp)

        with open(fp, mode="r", encoding="utf-8") as file:
            for key, val in json.load(file).items():
                self.set(key, val)

    def save(self, fp: str, allow_overwrite: bool = None) -> None:
        """
            Save the Config to the json filepath
        :param fp: json filepath
        :param allow_overwrite: True to allow overwrite existing files
        :return: None
        """
        if allow_overwrite is None:
            allow_overwrite = self.ALLOW_OVERWRITE

        if not isinstance(fp, str):
            raise TypeError(type(fp))

        if not fp.endswith(".json"):
            fp = fp + ".json"

        if not allow_overwrite and os.path.exists(fp):
            raise FileExistsError(fp)

        with open(fp, mode="w", encoding="utf-8") as file:
            json.dump(self.data, file)

    def set(self, key: str, val: object) -> None:
        """
            Set a config parameter
            this will call the functions expecting changes on the specified key
        :param key: config key
        :param val: value to set
        :return: None
        """
        self.data[key] = val
        for callback in self._callbacks.get(key, []):
            callback(val)

    def get(self, key: str, default=None) -> object:
        """
            Getter for the config parameter
        :param key: config key
        :return: the associated value
        """
        return self.data.get(key, default)

    def on(self, key: str, callback: callable) -> callable:
        """
            Give a callback function to be called when the key associated value changes
        :param key: the key to react on
        :param callback: the function to call on change
        :return: an unsubscribe function to call to remove the callback function from the list
        """
        self._callbacks.setdefault(key, [])
        self._callbacks[key].append(callback)
        return lambda: callback in self._callbacks[key] and self._callbacks[key].remove(callback)

    __setitem__ = set
    __getitem__ = get
