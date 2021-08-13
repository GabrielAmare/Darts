import os
from typing import Optional

from tools37.files import DirView

from darts.abstracts import AbstractParty
from darts.base_engines import fr, en
from darts.constants import HOME
from darts.style_data import STYLES, PACK_STYLES
from .AppEngines import AppEngines
from .AppImages import AppImages
from .AppLogger import AppLogger
from .AppMessages import AppMessages
from .AppSettings import AppSettings
from .AppStyles import AppStyles
from .AppVoice import AppVoice
from .GameManager import GameManager
from .GamesManager import GamesManager
from .ProfilesManager import ProfilesManager


class AppData(DirView):
    """Handle every part of the application which doesn't required Games to be loaded."""

    def get_path(self, name: str) -> str:
        return os.path.join(self.path, name)

    def __init__(self, root: str = HOME, name: str = 'Darts'):
        super().__init__(os.path.join(root, name), force_create=True)

        self.settings: AppSettings = self.load_json_file('settings.json', AppSettings)

        log_fp = self.get_path('log.csv')
        self.logger: AppLogger = AppLogger(fp=log_fp)

        self.voice: AppVoice = AppVoice(
            lang_IETF=self.lang_IETF
        )
        self.messages: AppMessages = AppMessages(
            lang_ISO_639_1=self.lang_ISO_639_1,
            logger=self.logger
        )
        self.images: AppImages = AppImages(
            root='assets/images/',
            logger=self.logger
        )
        self.styles: AppStyles = AppStyles(
            config_styles=STYLES,
            pack_styles=PACK_STYLES,
            logger=self.logger
        )
        self.engines: AppEngines = AppEngines(
            engines=dict(fr=fr.engine, en=en.engine),
            lang_ISO_639_1=self.lang_ISO_639_1,
            logger=self.logger
        )

        self.games: GamesManager = self.load_dir('games', GamesManager, logger=self.logger)
        self.profiles: ProfilesManager = self.load_dir('profiles', ProfilesManager)

        self.party: Optional[AbstractParty] = None

    @property
    def lang_ISO_639_1(self):
        return self.settings.lang_ISO_639_1

    @property
    def lang_IETF(self) -> str:
        return self.settings.lang_IETF

    @lang_IETF.setter
    def lang_IETF(self, value: str):
        self.settings.lang_IETF = value

        self.logger.info(f"lang set to {value!r}")

        self.voice.lang_IETF = self.settings.lang_IETF
        self.messages.lang_ISO_639_1 = self.lang_ISO_639_1
        self.engines.lang_ISO_639_1 = self.settings.lang_ISO_639_1

    def load_current_party(self):
        if self.settings.loaded_game:
            try:
                game = self.games.get(self.settings.loaded_game)
            except KeyError:
                return

            try:
                self.party = game.load_party(self.settings.loaded_party)

            except FileNotFoundError:
                return

    def save_current_party(self):
        """This will save the current party and the settings pfd."""

        if self.party and self.settings.loaded_game and self.settings.loaded_party:
            try:
                game: GameManager = self.games.get(self.settings.loaded_game)

            except KeyError:
                return

            game.save_json_file(str(self.party.uid), self.party)

    def has_party(self) -> bool:
        return self.party is not None

    def create_party(self, game_uid: str):
        self.party = self.games.create_party(game_uid)
        self.settings.loaded_game = game_uid
        self.settings.loaded_party = self.party.uid

    def load(self):
        pass

    def save(self):
        super().save()

        self.save_current_party()

    def get_current_game(self):
        """Return the currently selected game."""
        game_uid = self.settings.loaded_game
        game = self.games.get(game_uid)
        return game
