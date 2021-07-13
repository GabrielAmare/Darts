import os

from darts.base import AppSettings, AppLogger, AppImages, AppMessages, AppVoice, AppEngines, AppRepository, AppStyles
from darts.base import PartyFileData
from darts.core_games import AppGames, PartyBuilder
from darts.games import *


class AppService:
    def __init__(self,
                 settings: AppSettings,
                 logger: AppLogger,
                 styles: AppStyles,
                 images: AppImages,
                 messages: AppMessages,
                 voice: AppVoice,
                 repository: AppRepository,
                 games: AppGames,
                 engines: AppEngines
                 ):
        self.settings: AppSettings = settings
        self.logger: AppLogger = logger
        self.styles: AppStyles = styles
        self.images: AppImages = images
        self.messages: AppMessages = messages
        self.voice: AppVoice = voice
        self.repository: AppRepository = repository
        self.games: AppGames = games
        self.engines: AppEngines = engines

        # load the default messages files
        if os.path.exists(self.settings.messages_fp):
            for category in os.listdir(self.settings.messages_fp):
                self.messages.load_directory(
                    path=self.settings.messages_fp + category,
                    category=category.upper()
                )

        # load the games
        games = {
            '301': game_301,
            'cricket': game_cricket,
            'rtc': game_rtc,
        }

        for game_uid, module in games.items():
            builder = PartyBuilder(
                module.game,
                module.ScoreBoard
            )
            self.games.builders[game_uid] = builder

            path = os.path.join(self.games.root, f'game_{game_uid}')

            builder.load_config(os.path.join(path, 'config.json'))
            builder.save_config(os.path.join(path, 'config.json'))

            self.messages.load_directory(path=os.path.join(path, 'messages'), category=game_uid)

            self.repository.load_repo(game_uid)

        pfd = self.settings.pfd
        if pfd.game_uid and pfd.party_uid:
            try:
                self.games.load_party(pfd.game_uid, pfd.party_uid)

            except FileNotFoundError:
                self.settings.pfd = PartyFileData()

    @property
    def lang_IETF(self) -> str:
        return self.settings.lang_IETF

    @lang_IETF.setter
    def lang_IETF(self, value: str):
        self.settings.lang_IETF = value
        self.logger.info(f"lang set to {value!r}")

        self.messages.set_lang(self.settings.lang_ISO_639_1)
        self.voice.set_lang_IETF(self.settings.lang_IETF)
        self.engines.lang_ISO_639_1 = self.settings.lang_ISO_639_1

    @property
    def games_fp(self) -> str:
        return self.settings.games_fp

    @games_fp.setter
    def games_fp(self, value: str):
        self.settings.games_fp = value
        self.logger.info(f"games filepath set to {value!r}")

        self.repository.root = value

    def save(self):
        """Save the App before quitting."""
        if self.games.party:
            self.games.save_party()

        self.settings.save()
