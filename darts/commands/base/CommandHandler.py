from typing import List, Tuple, Union
from .errors import InvalidCommandType


class CommandMethod:
    def __init__(self, types: Tuple[type], method: callable):
        self.type: Union[type, Tuple[type]] = types[0] if len(types) == 1 else types
        self.method: callable = method

    @classmethod
    def decorator(cls, *types: type):
        def wrapper(method: callable):
            return cls(types, method)

        return wrapper


class CommandHandler:
    """A command manager can bind object types to methods"""
    _handlers: List[CommandMethod]

    def __init_subclass__(cls, **kwargs):
        cls._handlers: List[CommandMethod] = []

        for key, val in cls.__dict__.items():
            if isinstance(val, CommandMethod):
                cls._handlers.append(val)
                setattr(cls, key, val.method)

    def execute_command(self, command: object):
        for handler_ in self._handlers:
            if isinstance(command, handler_.type):
                return handler_.method(self, command)
        else:
            raise InvalidCommandType(command, type(command))


handler = CommandMethod.decorator
