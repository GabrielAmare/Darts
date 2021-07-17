import os

from darts.app_data import AppData
from darts.base import AppRepository
from darts.base import PartyFileData
from darts.games import *


class AppService:
    def __init__(self,
                 data: AppData,
                 repository: AppRepository,
                 ):
        self.data: AppData = data
        self.repository: AppRepository = repository

        # load the default messages files
        if os.path.exists('assets/messages/'):
            for category in os.listdir('assets/messages/'):
                self.data.messages.load_directory(
                    path='assets/messages/' + category,
                    category=category.upper()
                )

        # load the games messages
        for game_uid in self.data.games:
            self.data.messages.load_directory(
                path=os.path.join('darts', 'games', f'game_{game_uid}', 'messages'),
                category=game_uid
            )

        pfd = self.data.settings.pfd
        if pfd.game_uid and pfd.party_uid:
            try:
                self.data.games[pfd.game_uid].load_party(pfd.party_uid)

            except FileNotFoundError:
                self.data.settings.pfd = PartyFileData()

    def save(self):
        """Save the App before quitting."""
        self.data.save()

