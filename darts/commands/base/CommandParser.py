from text_engine import Engine, Identified
from text_engine.core.Engine import InvalidASTError
from .errors import InvalidTextCommand


class CommandParser:
    def __init__(self, engine: Engine):
        self.engine: Engine = engine

    def parse_command(self, text: str, identifier: str = Identified.ALL):
        try:
            return self.engine.read(text, identifier=identifier)

        except InvalidASTError:
            raise InvalidTextCommand(text, identifier)
