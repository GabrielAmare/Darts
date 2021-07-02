from __future__ import annotations

from typing import List, Tuple

__all__ = ["CommandHandler", "command_method"]


class command_method:
    __cache__: List[command_method] = []

    @classmethod
    def pop_cache(cls) -> List[Tuple[type, callable]]:
        cache = [(cm.command_type, cm.method) for cm in cls.__cache__]
        cls.__cache__ = []
        return cache

    def __init__(self, method: callable):
        assert 'command' in method.__annotations__, "command_method method must have a 'command' argument"
        self.method: callable = method
        self.command_type: type = method.__annotations__['command']


class CommandHandler:
    def __init_subclass__(cls, **kwargs):
        cls.__commands: List[Tuple[type, callable]] = command_method.pop_cache()

    def execute(self, command):
        """
            Will call the method binded to the specified command type
        """
        for command_type, method in self.__commands:
            if isinstance(command, command_type):
                return method(self, command)
        else:
            raise Exception(f"command method not found for command type {command.__class__.__name__!r}")
