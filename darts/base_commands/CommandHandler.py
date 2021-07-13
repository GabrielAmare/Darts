from typing import List

from darts.errors import InvalidCommandTypeError
from .CommandMethod import CommandMethod


class CommandHandler:
    """A command manager can bind object types to methods"""
    _handlers: List[CommandMethod]

    @classmethod
    def _register_command_method(cls, key: str, val: CommandMethod):
        cls._handlers.append(val)
        setattr(cls, key, val.method)

    @classmethod
    def _register_all_command_methods(cls):
        for key, val in cls.__dict__.items():
            if isinstance(val, CommandMethod):
                cls._register_command_method(key, val)

    def __init_subclass__(cls, **kwargs):
        cls._handlers: List[CommandMethod] = []

        cls._register_all_command_methods()

    def execute_command(self, command: object):
        for handler in self._handlers:
            if isinstance(command, handler.type):
                return handler.method(self, command)

        else:
            raise InvalidCommandTypeError(command, type(command))
