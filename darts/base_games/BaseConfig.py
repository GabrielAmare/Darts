from abc import ABC
from typing import Dict

from darts.abstracts import AbstractConfig
from .Option import Option


class BaseConfig(AbstractConfig, ABC):
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
