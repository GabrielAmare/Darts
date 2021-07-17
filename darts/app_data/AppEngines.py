from typing import Dict, Tuple, Optional

from text_engine import Engine

from darts.base_commands import Command
from darts.constants import CTX, MainState, PartyState
from darts.errors import CommandNotFoundError
from darts.app_data.AppLogger import AppLogger
import importlib


class AppEngines:
    def __init__(self, engines: Dict[str, Engine], lang_ISO_639_1: str, logger: AppLogger):
        self.engines: Dict[str, Engine] = engines
        self.lang_ISO_639_1: str = lang_ISO_639_1
        self.logger: AppLogger = logger

    def load_engine(self, path: str, lang: str):
        path = path.replace('/', '.')
        module = importlib.import_module(name=path)
        self.engines[lang] = module.engine

    def get_identifier(self, main_state: MainState, party_state: Optional[PartyState]) -> str:
        if main_state is MainState.GAME_MENU:
            return CTX.__MAIN_MENU__

        elif main_state is MainState.GAME_SETTINGS:
            return CTX.__SETTINGS__

        elif main_state is MainState.APP_SETTINGS:
            return CTX.__SETTINGS__

        elif main_state is MainState.CURRENT_PARTY:
            if party_state is PartyState.BEFORE:
                return CTX.__PRE_GAME__

            elif party_state is PartyState.DURING:
                return CTX.__IN_GAME__

            elif party_state is PartyState.AFTER:
                return CTX.__POST_GAME__

            else:
                self.logger.warning(f"location : AppEngines.get_identifier(...)\n"
                                    f"reason   : party_state invalid : {party_state!r}")
                return CTX.__GAME__

        else:
            return CTX.__GLOBAL__

    def read(self, identifier: str, *texts: str) -> Tuple[str, Command]:
        engine = self.engines[self.lang_ISO_639_1]

        for text in texts:
            command = engine.read(text=text, identifier=identifier)

            if isinstance(command, Command):
                return text, command

        raise CommandNotFoundError(texts=list(texts))
