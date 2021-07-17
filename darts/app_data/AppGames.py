import os
from tkinter import Widget
from typing import Type, List

from tools37 import JsonFile

from darts.base_games import BaseConfig, BaseParty, BasePlayer, BaseScore
from .AppLogger import AppLogger
from ..functions import create_dir_if_not_exists


class AppGames:
    """This class handle all the game stuff."""

    def __init__(self, path: str,
                 logger: AppLogger,
                 config_cls: Type[BaseConfig],
                 party_cls: Type[BaseParty],
                 player_cls: Type[BasePlayer],
                 score_cls: Type[BaseScore],
                 score_board_cls: Type[Widget]
                 ):
        self.path: str = path
        self.logger: AppLogger = logger

        created = create_dir_if_not_exists(self.path)
        if created:
            self.logger.created(self.path)
        else:
            self.logger.loaded(self.path)

        self.config_cls: Type[BaseConfig] = config_cls
        self.party_cls: Type[BaseParty] = party_cls
        self.player_cls: Type[BasePlayer] = player_cls
        self.score_cls: Type[BaseScore] = score_cls
        self.score_board_cls: Type[Widget] = score_board_cls

        self.party_uids: List[int] = self.load_party_uids()
        self.party_config: BaseConfig = self.load_party_config()

    def get_path(self, name: str) -> str:
        return os.path.join(self.path, name)

    def load_party_config(self) -> BaseConfig:
        file_path = self.get_path('settings.json')

        if JsonFile.exists(file_path):
            file_data = JsonFile.load(file_path)
        else:
            file_data = {}

        return self.config_cls.from_dict(file_data)

    def load_party_uids(self) -> List[int]:
        uids = []
        for file_name in os.listdir(self.path):
            file_path = self.get_path(file_name)
            if os.path.isfile(file_path):
                base_name, extension = os.path.splitext(file_path)
                if extension == '.json':
                    if base_name.isnumeric():
                        uids.append(int(base_name))

        return uids

    def new_uid(self) -> int:
        uid = 1
        while uid in self.party_uids:
            uid += 1

        self.party_uids.append(uid)

        return uid

    def create_party(self):
        return self.party_cls(
            uid=self.new_uid(),
            config=self.party_config.copy()
        )

    def load_party(self, uid: int) -> BaseParty:
        fp = self.get_path(str(uid))
        party_data = JsonFile.load(fp)
        party = self.party_cls.from_dict(party_data)
        return party

    def save_party(self, party: BaseParty):
        fp = self.get_path(str(party.uid))
        party_data = party.to_dict()
        JsonFile.save(fp, party_data)

    def load_config(self, name: str) -> BaseConfig:
        fp = self.get_path(name)

        if JsonFile.exists(fp):
            data = JsonFile.load(fp)
            self.logger.loaded(fp)
        else:
            data = {}

        return self.config_cls.from_dict(data)

    def save_config(self, name: str, config: BaseConfig) -> None:
        fp = self.get_path(name)

        data = config.to_dict()

        exists = JsonFile.exists(fp)
        JsonFile.save(fp, data)

        if exists:
            self.logger.saved(fp)
        else:
            self.logger.created(fp)

    def save(self):
        self.save_config('settings.json', self.party_config)
