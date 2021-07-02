from text_engine import Engine, Identified

from tools import VoiceInterface
from .CommandHandler import CommandHandler
from .CommandListener import CommandListener
from .CommandParser import CommandParser
from .errors import InvalidVocalCommand, InvalidTextCommand, InvalidCommandType


class CommandManager(CommandHandler, CommandParser, CommandListener):
    def __init__(self, vi: VoiceInterface, engine: Engine):
        CommandListener.__init__(self, vi)
        CommandParser.__init__(self, engine)
        CommandHandler.__init__(self)

    def listen(self, identifier: str = Identified.ALL):
        texts = self.listen_command()
        errors = []
        for text in texts:
            try:
                command = self.parse_command(text, identifier)
            except InvalidTextCommand as error:
                errors.append(error)
                continue

            try:
                return self.execute_command(command)
            except InvalidCommandType as error:
                errors.append(error)
                continue


        else:
            raise InvalidVocalCommand(list(zip(texts, errors)))
