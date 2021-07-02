from typing import List, Dict

from .Command import Command


class CommandHandler:
    class UnhandledCommandType(Exception):
        def __init__(self, command_type):
            self.command_type = command_type

    STATES: List[str]
    COMMAND_HANDLERS: Dict[type, callable]

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
