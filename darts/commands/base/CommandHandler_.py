from typing import List, Dict

from .Command import Command


class CommandMethod:
    def __init__(self, command_type: type, command_meth: callable):
        self.command_type: type = command_type
        self.command_meth: callable = command_meth

    @classmethod
    def decorator(cls, command_type: type):
        def wrapper(command_meth: callable):
            return cls(command_type, command_meth)

        return wrapper


execute = CommandMethod.decorator


class CommandHandler:
    _commands: List[CommandMethod]

    class UnhandledCommandType(Exception):
        def __init__(self, command_type):
            self.command_type = command_type

    STATES: List[str]
    COMMAND_HANDLERS: Dict[type, callable]

    def __init_subclass__(cls, **kwargs):
        cls._commands: List[CommandMethod] = []
        for key, val in cls.__dict__.items():
            if isinstance(val, CommandMethod):
                cls._commands.append(val)

    def execute(self, command: object):
        for handler in self._commands:
            if isinstance(command, handler.command_type):
                return handler.command_meth(self, command)
        else:
            raise CommandHandler.UnhandledCommandType(type(command))

    def __init__(self, state: str):
        self.state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value not in self.STATES:
            raise ValueError(value)
        self._state = value

    def handle(self, command: Command):
        command_type = type(command)

        if command_type not in self.COMMAND_HANDLERS:
            raise CommandHandler.UnhandledCommandType(type(command))

        method_name = self.COMMAND_HANDLERS[command_type]

        method = getattr(self, method_name)

        return method(command)
