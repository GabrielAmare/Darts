from typing import Optional

from .CommandHandler import CommandHandler
from .Command import Command


class CommandHandlerWrapper(CommandHandler):
    command_handler: Optional[CommandHandler]

    def __init__(self, state: str):
        super().__init__(state)
        self.command_handler = None

    def set_command_handler(self, command_handler: Optional[CommandHandler]):
        self.command_handler = command_handler

    def handle(self, command: Command):
        command_type = type(command)

        if command_type not in self.COMMAND_HANDLERS:
            if self.command_handler is None:
                raise CommandHandler.UnhandledCommandType(type(command))

            return self.command_handler.handle(command)

        method_name = self.COMMAND_HANDLERS[command_type]

        method = getattr(self, method_name)

        return method(command)
