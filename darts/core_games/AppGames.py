import importlib
import os
from typing import Iterator, Optional, Dict

from darts.base import PartyFileData
from darts.constants import TextMode
from .BaseParty import BaseParty
from .PartyBuilder import PartyBuilder
from darts.base.AppMessages import AppMessages
from darts.base.AppSettings import AppSettings
from darts.base.AppVoice import AppVoice
from darts.base.AppRepository import AppRepository


class AppGames:
    """This class handle all the game stuff."""

    def __init__(self, root: str, app_repository: AppRepository, app_voice: AppVoice, app_messages: AppMessages,
                 app_settings: AppSettings):
        self.root: str = root
        self.app_repository: AppRepository = app_repository
        self.app_voice: AppVoice = app_voice
        self.app_messages: AppMessages = app_messages
        self.app_settings: AppSettings = app_settings
        self.builders: Dict[str, PartyBuilder] = {}
        self.party: Optional[BaseParty] = None

        # if os.path.exists(self.root):
        #     for name in os.listdir(self.root):
        #         if name.startswith('game_'):
        #             game_uid = name[5:]
        #             path = os.path.join(self.root, name)
        #
        #             module = importlib.import_module(name=f'darts.games.{name}.__init__')
        #
        #             builder = PartyBuilder(
        #                 module.game,
        #                 module.ScoreBoard
        #             )
        #
        #             self.builders[game_uid] = builder
        #
        #             builder.load_config(os.path.join(path, 'config.json'))
        #             builder.save_config(os.path.join(path, 'config.json'))
        #
        #             self.app_messages.load_directory(path=os.path.join(path, 'messages'), category=game_uid)
        #
        #             self.app_repository.load_repo(game_uid)

    def set_party(self, party: BaseParty) -> None:
        self.party = party
        party.on('announce', self.announce)

    def get_party(self) -> BaseParty:
        return self.party

    def del_party(self) -> None:
        self.party = None

    def has_party(self) -> bool:
        return isinstance(self.party, BaseParty)

    def announce(self, code, **config):
        message = self.app_messages.translate(code, TextMode.RANDOM, **config)
        return self.app_voice.speak(message)

    def get_game_uids(self) -> Iterator[str]:
        return iter(self.builders.keys())

    def create_party(self, game_uid: str) -> None:
        """Create a new party."""
        if self.has_party():
            self.save_party()
            self.del_party()

        builder = self.builders[game_uid]
        party = builder.create_party()
        self.set_party(party)

        self.app_settings.pfd = PartyFileData(game_uid=game_uid, party_uid=0)

    def save_party(self) -> None:
        """Save the current party."""
        assert self.has_party()
        assert self.app_settings.pfd.game_uid

        game_uid = self.app_settings.pfd.game_uid

        if self.app_settings.pfd.party_uid:
            party_uid = self.app_settings.pfd.party_uid
            self.app_repository.update(repo=game_uid, uid=party_uid, data=self.party.to_dict())
        else:
            uid = self.app_repository.create(repo=game_uid, data=self.party.to_dict())
            self.app_settings.pfd.party_uid = uid

    def load_party(self, game_uid: str, party_uid: int) -> None:
        """Load an existing party."""

        data = self.app_repository.access(repo=game_uid, uid=party_uid)
        builder = self.builders[game_uid]
        party = builder.game.party_cls.from_dict(data)
        self.set_party(party)

        self.app_settings.pfd = PartyFileData(game_uid, party_uid)
