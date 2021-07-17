from tkinter import Widget
from typing import Type, Dict, List

from tools37.files import DirView

from darts.abstracts import PARTY, PLAYER, CONFIG, SCORE
from .AppLogger import AppLogger
from .GameManager import GameManager


class GamesManager(DirView):
    def __init__(self, path: str, logger: AppLogger):
        super().__init__(path, force_create=True)
        self.logger: AppLogger = logger
        self._games: Dict[str, GameManager] = {}

    def register(self, game_uid: str,
                 config_cls: Type[CONFIG],
                 party_cls: Type[PARTY],
                 player_cls: Type[PLAYER],
                 score_cls: Type[SCORE],
                 score_board_cls: Type[Widget]
                 ) -> GameManager[CONFIG, PARTY, PLAYER, SCORE]:
        game = self.load_dir(
            game_uid,
            GameManager,
            logger=self.logger,
            config_cls=config_cls,
            party_cls=party_cls,
            player_cls=player_cls,
            score_cls=score_cls,
            score_board_cls=score_board_cls
        )
        self._games[game_uid] = game
        return game

    def get(self, game_uid: str) -> GameManager:
        return self._games[game_uid]

    def load(self) -> None:
        pass

    def all_games_uid(self) -> List[str]:
        return list(self._games.keys())

    def create_party(self, game_uid: str) -> PARTY:
        return self.get(game_uid).create_party()
