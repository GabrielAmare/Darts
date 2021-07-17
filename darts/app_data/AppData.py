import os
from tkinter import Widget
from typing import Type, Dict, Optional

from darts.base_engines import fr, en
from darts.base_games import BaseConfig, BaseParty, BasePlayer, BaseScore
from darts.style_data import STYLES, PACK_STYLES
from .AppEngines import AppEngines
from .AppGames import AppGames
from .AppImages import AppImages
from .AppLogger import AppLogger
from .AppMessages import AppMessages
from .AppSettings import AppSettings
from .AppStyles import AppStyles
from .AppVoice import AppVoice
from ..base import PartyFileData
from darts.functions import create_dir_if_not_exists
from darts.constants import HOME
from tools37 import JsonFile


class AppData:
    """Handle every part of the application which doesn't required Games to be loaded."""

    def get_path(self, name: str) -> str:
        return os.path.join(self.path, name)

    def __init__(self, root: str = HOME):
        self.path = os.path.join(root, 'Darts')

        create_dir_if_not_exists(self.path)

        self.settings_path = self.get_path('settings.json')
        try:
            settings_data = JsonFile.load(self.settings_path)
        except FileNotFoundError:
            settings_data = {}

        self.settings: AppSettings = AppSettings.from_dict(settings_data)

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
        self.games: Dict[str, AppGames] = {}
        self.party: Optional[BaseParty] = None

        self.games_fp = self.get_path('games')
        created = create_dir_if_not_exists(self.games_fp)
        if created:
            self.logger.created(self.games_fp)
        else:
            self.logger.loaded(self.games_fp)

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

    def register_game(self, game_uid: str,
                      config_cls: Type[BaseConfig],
                      party_cls: Type[BaseParty],
                      player_cls: Type[BasePlayer],
                      score_cls: Type[BaseScore],
                      score_board_cls: Type[Widget]
                      ):
        self.games[game_uid] = AppGames(
            path=os.path.join(self.games_fp, game_uid),
            logger=self.logger,
            config_cls=config_cls,
            party_cls=party_cls,
            player_cls=player_cls,
            score_cls=score_cls,
            score_board_cls=score_board_cls
        )

    def load_current_party(self):
        """This will load the current party from the settings pfd."""
        pfd = self.settings.pfd
        if pfd:
            try:
                game = self.games[pfd.game_uid]
            except KeyError:
                return

            try:
                self.party = game.load_party(pfd.party_uid)

            except FileNotFoundError:
                return

    def save_current_party(self):
        """This will save the current party and the settings pfd."""
        pfd = self.settings.pfd

        if self.party and pfd:
            try:
                game = self.games[pfd.game_uid]
            except KeyError:
                return

            game.save_party(self.party)

    def has_party(self) -> bool:
        return self.party is not None

    def create_party(self, game_uid: str):
        self.party = self.games[game_uid].create_party()
        self.settings.pfd = PartyFileData(game_uid=game_uid, party_uid=self.party.uid)

    def save(self):
        settings_data = self.settings.to_dict()
        JsonFile.save(self.settings_path, settings_data)

        for app_game in self.games.values():
            app_game.save()

        self.save_current_party()
