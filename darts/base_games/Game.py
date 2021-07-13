from typing import Type

from .BaseConfig import BaseConfig
from .BaseParty import BaseParty
from .BasePlayer import BasePlayer
from .BaseScore import BaseScore


class Game:
    def __init__(self, config_cls: Type[BaseConfig], party_cls: Type[BaseParty], player_cls: Type[BasePlayer],
                 score_cls: Type[BaseScore]):
        self.config_cls: Type[BaseConfig] = config_cls
        self.party_cls: Type[BaseParty] = party_cls
        self.player_cls: Type[BasePlayer] = player_cls
        self.score_cls: Type[BaseScore] = score_cls
