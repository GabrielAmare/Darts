from typing import List
from .Command import Command

from text_engine import Engine, Identified
from text_engine.core.Engine import InvalidASTError

from tools import VoiceInterface

from ..console import console
from ..vocal_errors import ListenError, TextNotFoundError, CommandNotFoundError


class CommandParser:
    def __init__(self, vi: VoiceInterface, engine: Engine):
        self.vi = vi
        self.engine = engine

    def listen(self, identifier: str = Identified.ALL) -> (str, Command):
        try:
            texts = self.vi.listen(show_all=True)
            console.debug("texts : \n" + "\n".join(texts))
        except VoiceInterface.AudioToTextError:
            raise ListenError()

        if not texts:
            raise TextNotFoundError()

        for text in texts:
            try:
                command = self.engine.read(text, identifier=identifier)
            except InvalidASTError:
                continue

            if isinstance(command, Command):
                return text, command
        else:
            raise CommandNotFoundError(texts)
