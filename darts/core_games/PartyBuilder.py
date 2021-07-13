from tkinter import Widget
from typing import Optional, Type

from darts.base_games import Game, BaseConfig, BaseParty
from darts.errors import PartyConfigurationMissingError


class PartyBuilder:
    """Class that allow to load/save a party configuration and load parties with it."""

    def __init__(self, game: Game, scoreboard_cls: Type[Widget]):
        self.game: Game = game
        self.scoreboard_cls: Type[Widget] = scoreboard_cls
        self.config: Optional[BaseConfig] = None

    def load_config(self, fp: str) -> None:
        """Load a configuration from a json file."""
        self.config = self.game.config_cls.load(fp)

    def save_config(self, fp: str = '') -> None:
        """Save the configuration to a json file."""
        self.config.save(fp)

    def create_party(self) -> BaseParty:
        """Create a new party using the current configuration."""
        if self.config is None:
            raise PartyConfigurationMissingError()

        return self.game.party_cls(config=self.config)
