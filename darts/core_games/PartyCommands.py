from abc import ABC
from typing import TypeVar, Generic

from darts.base_commands import Command
from darts.base_games import BaseConfig, BaseScore, BasePlayer
from darts.constants import PartyState
from darts.core_commands import Undo, Redo, AddPlayer, AddPlayers, StartParty, AddScore
from darts.errors import InvalidScoreError
from .PartyLogic import PartyLogic

C = TypeVar('C', bound=BaseConfig)
P = TypeVar('P', bound=BasePlayer)
S = TypeVar('S', bound=BaseScore)


class PartyCommands(Generic[C, P, S], PartyLogic[C, P, S], ABC):
    def execute(self, command: Command) -> None:
        try:
            if self.state is PartyState.BEFORE:
                self.execute_before(command)
            elif self.state is PartyState.DURING:
                self.execute_during(command)
            elif self.state is PartyState.AFTER:
                self.execute_after(command)
            else:
                self.execute_always(command)

        except InvalidScoreError as e:
            self.stack.clear()
            self.announce_invalid_score()
            self.do()

    def execute_always(self, command: Command) -> None:
        if isinstance(command, Undo):
            self.on_command_undo(command)
        elif isinstance(command, Redo):
            self.on_command_redo(command)
        else:
            raise Exception

    def execute_before(self, command: Command) -> None:
        if isinstance(command, AddPlayer):
            self.on_command_add_player(command)
        elif isinstance(command, AddPlayers):
            self.on_command_add_players(command)
        elif isinstance(command, StartParty):
            self.on_command_start_party(command)
        else:
            return self.execute_always(command)

    def execute_during(self, command: Command) -> None:
        if isinstance(command, AddScore):
            self.on_command_add_score(command)
        else:
            return self.execute_always(command)

    def execute_after(self, command: Command) -> None:
        return self.execute_always(command)
