from typing import Type
from darts.classes import Party, Player, Score

class GamePack:
    """
        GamePack is used to contain all the classes related to a particular game
    """

    def __init__(self, party_type: Type[Party],
                 player_type: Type[Player],
                 score_type: Type[Score],
                 score_board_type: type):
        self.party_type: Type[Party] = party_type
        self.player_type: Type[Player] = player_type
        self.score_type: Type[Score] = score_type
        self.score_board_type: type = score_board_type
