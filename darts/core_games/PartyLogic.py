from abc import ABC
from typing import TypeVar, Generic

from darts import base_games as bg
from darts.constants import PartyState
from darts.core_commands import Undo, Redo, AddPlayer, StartParty, AddPlayers, AddScore
from darts.errors import PartyAlreadyStartedError, PartyAlreadyOverError, PartyNotStartedError
from .PartyAnnouncer import PartyAnnouncer

C = TypeVar('C', bound=bg.BaseConfig)
P = TypeVar('P', bound=bg.BasePlayer)
S = TypeVar('S', bound=bg.BaseScore)


class PartyLogic(Generic[C, P, S], PartyAnnouncer[C, P, S], ABC):
    def on_command_undo(self, command: Undo) -> None:
        """Undo actions."""
        self.undo_times(command.times)

        self.do()

    def on_command_redo(self, command: Redo) -> None:
        """Redo actions."""
        self.redo_times(command.times)

        self.do()

    def on_command_add_player(self, command: AddPlayer) -> None:
        """Add a player."""
        if self is PartyState.DURING:
            raise PartyAlreadyStartedError()

        if self is PartyState.AFTER:
            raise PartyAlreadyOverError()

        self.add_player(command.player.name)

        self.do()

    def on_command_start_party(self, _command: StartParty) -> None:
        """Start the party."""
        if self.state is PartyState.DURING:
            raise PartyAlreadyStartedError()

        if self.state is PartyState.AFTER:
            raise PartyAlreadyOverError()

        self.start_party()

        self.announce_start()

        self.do()

    def on_command_add_players(self, command: AddPlayers) -> None:
        """Add players and start the party."""
        if self.state is PartyState.DURING:
            raise PartyAlreadyStartedError()

        if self.state is PartyState.AFTER:
            raise PartyAlreadyOverError()

        self.add_players(player.name for player in command.players)

        self.announce_start()

        self.do()

    def on_command_add_score(self, command: AddScore) -> None:
        """"""
        if self.state is PartyState.BEFORE:
            raise PartyNotStartedError()

        if self.state is PartyState.AFTER:
            raise PartyAlreadyOverError()

        # acquire the targeted player
        if command.player is None:
            player = self.get_next_player()
        else:
            player = self.get_player_by_name(command.player.name)

        # calculate the new score
        new_score = self.update_score(player, command.scores)

        # append the score to the player scores
        self.add_score(player, new_score)

        self.announce_score(player, new_score)

        self.do()

        # check if the game have been won
        is_over = self.check_winner()

        self.do()

        if is_over:
            self.announce_end()
        else:
            self.announce_player(self.get_player_after(player))

        self.do()