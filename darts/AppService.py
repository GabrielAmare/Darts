import os

from darts.app_data import AppData

import darts.games


class AppService:
    def __init__(self,
                 data: AppData,
                 ):
        self.data: AppData = data

        # load the default messages files
        if os.path.exists('assets/messages/'):
            for category in os.listdir('assets/messages/'):
                self.data.messages.load_directory(
                    path='assets/messages/' + category,
                    category=category.upper()
                )

        # load the games messages
        for game_uid in self.data.games.all_games_uid():
            self.data.messages.load_directory(
                path=os.path.join('darts', 'games', f'game_{game_uid}', 'messages'),
                category=game_uid
            )

        if self.data.settings.loaded_game:
            try:
                game = self.data.games.get(self.data.settings.loaded_game)

            except KeyError:
                self.data.settings.loaded_game = ''

            else:
                try:
                    game.load_party(self.data.settings.loaded_party)

                except FileNotFoundError:
                    self.data.settings.loaded_party = 0

    def save(self):
        """Save the App before quitting."""
        self.data.save()
