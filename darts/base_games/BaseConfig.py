from abc import ABC, abstractmethod
from typing import Type, TypeVar, Dict

from tools37 import JsonFile

from darts.base import DictInterface
from .Option import Option
from darts.app_logger import app_logger

C = TypeVar('C')


class BaseConfig(DictInterface, ABC):
    options: Dict[str, Option]

    def __init_subclass__(cls, **kwargs):
        cls.options: Dict[str, Option] = {}

        for key, val in cls.__dict__.copy().items():
            if isinstance(val, Option):
                cls.options[key] = val
                delattr(cls, key)

    def __init__(self, **config):
        for key, option in self.__class__.options.items():
            try:
                self.set(key, config.get(key))

            except ValueError:
                self.set(key, option.default)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{key!s}={self.get(key)!r}' for key in self.options)})"

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def load(cls: Type[C], fp: str) -> C:
        """Load the config from a json file"""
        if JsonFile.exists(fp):
            data = JsonFile.load(fp)
            app_logger.loaded(fp)
        else:
            data = {}
        return cls.from_dict(data)

    def save(self, fp: str) -> None:
        """Save the config to a json file"""
        data = self.to_dict()

        exists = JsonFile.exists(fp)
        JsonFile.save(fp, data)

        if exists:
            app_logger.saved(fp)
        else:
            app_logger.created(fp)

    def set(self, key: str, value):
        """Config parameter setter."""
        option = self.__class__.options[key]

        if not option.confirm(value):
            raise ValueError(value)

        setattr(self, key, value)

    def get(self, key: str):
        """Config parameter getter."""
        if key in self.__class__.options:
            return getattr(self, key)
        else:
            raise KeyError(key)

    def copy(self):
        return self.__class__(**{key: self.get(key) for key in self.options})
