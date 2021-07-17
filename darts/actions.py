from typing import Optional, List

from darts.Profile import Profile
from darts.app_data import app_data
from darts.base_actions import Action
from darts.base_games import BaseParty, BasePlayer, BaseScore
from darts.constants import PartyState
from darts.errors import ProfileNotFoundError


class AddPlayer(Action):
    def __init__(self, party: BaseParty, name: str):
        self.party: BaseParty = party
        self.name: str = name

        self.player: Optional[BasePlayer] = None
        self.profile: Optional[Profile] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.name!r})"

    def do(self) -> None:
        try:
            self.profile = app_data.profiles.find_profile_by_name(self.name)

        except ProfileNotFoundError:
            self.profile = app_data.profiles.create_profile(self.name)

        self.player = self.party.create_player(self.profile)
        self.party.players.append(self.player)
        app_data.logger.do(self)

    def undo(self) -> None:
        self.party.players.remove(self.player)
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.party.players.append(self.player)
        app_data.logger.redo(self)


class AddScore(Action):
    def __init__(self, party: BaseParty, player: BasePlayer, score: BaseScore):
        self.party: BaseParty = party
        self.player: BasePlayer = player
        self.score: BaseScore = score

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.player!r}, {self.score!r})"

    def do(self) -> None:
        self.player.scores.append(self.score)
        app_data.logger.do(self)

    def undo(self) -> None:
        self.player.scores.remove(self.score)
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.player.scores.append(self.score)
        app_data.logger.redo(self)


class Announce(Action):
    def __init__(self, party: BaseParty, code: str, config: dict):
        self.party: BaseParty = party
        self.code: str = code
        self.config: dict = config

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.code!r}, {self.config!r})"

    def do(self) -> None:
        self.party.emit('announce', self.code, **self.config)
        app_data.logger.do(self)

    def undo(self) -> None:
        app_data.logger.undo(self)

    def redo(self) -> None:
        app_data.logger.redo(self)


class EndParty(Action):
    def __init__(self, party: BaseParty):
        self.party: BaseParty = party

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r})"

    def do(self) -> None:
        self.party.state = PartyState.AFTER
        app_data.logger.do(self)

    def undo(self) -> None:
        self.party.state = PartyState.DURING
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.party.state = PartyState.AFTER
        app_data.logger.redo(self)


class InitScore(Action):
    def __init__(self, party: BaseParty, name: str):
        self.party: BaseParty = party
        self.name: str = name

        self.player: Optional[BasePlayer] = None
        self.score: Optional[BaseScore] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.name!r})"

    def do(self) -> None:
        self.player = self.party.get_player_by_name(self.name)
        self.score = self.party.initial_score(self.player)
        self.player.scores.append(self.score)
        app_data.logger.do(self)

    def undo(self) -> None:
        self.player.scores.remove(self.score)
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.player.scores.append(self.score)
        app_data.logger.redo(self)


class PlaySound(Action):
    def __init__(self, party: BaseParty, sound: str):
        self.party: BaseParty = party
        self.sound: str = sound

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.sound!r})"

    def do(self) -> None:
        app_data.voice.play(f"assets/sounds/{self.sound}.mp3")
        app_data.logger.do(self)

    def undo(self) -> None:
        app_data.logger.undo(self)

    def redo(self) -> None:
        app_data.logger.redo(self)


class SetLastPlayer(Action):
    def __init__(self, party: BaseParty, name: str):
        self.party: BaseParty = party
        self.name: str = name

        self.player: Optional[BasePlayer] = None
        self.last: Optional[BasePlayer] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r}, {self.name!r})"

    def do(self) -> None:
        self.last = self.party.latest
        self.player = self.party.get_player_by_name(self.name)
        self.party.latest = self.player
        app_data.logger.do(self)

    def undo(self) -> None:
        self.party.latest = self.last
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.party.latest = self.player
        app_data.logger.redo(self)


class SetWinners(Action):
    def __init__(self, party: BaseParty, players: List[BasePlayer]):
        self.party: BaseParty = party
        self.players: List[BasePlayer] = players

    def __repr__(self) -> str:
        args = [self.party, *self.players]
        return f"{self.__class__.__name__}({self.party!r}, {self.players!r})"

    def do(self) -> None:
        self.party.winners = self.players
        app_data.logger.do(self)

    def undo(self) -> None:
        self.party.winners = []
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.party.winners = self.players
        app_data.logger.redo(self)


class StartParty(Action):
    def __init__(self, party: BaseParty):
        self.party: BaseParty = party

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.party!r})"

    def do(self) -> None:
        self.party.state = PartyState.DURING
        app_data.logger.do(self)

    def undo(self) -> None:
        self.party.state = PartyState.BEFORE
        app_data.logger.undo(self)

    def redo(self) -> None:
        self.party.state = PartyState.DURING
        app_data.logger.redo(self)
