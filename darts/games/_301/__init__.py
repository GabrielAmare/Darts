from .Party_301 import Party_301
from .Score_301 import Score_301
from .ScoreBoard_301 import ScoreBoard_301

from darts.GamePack import GamePack
from darts.classes import Player

_301 = GamePack(
    party_type=Party_301,
    player_type=Player,
    score_type=Score_301,
    score_board_type=ScoreBoard_301
)
