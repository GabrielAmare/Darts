from typing import Iterator

from darts.actions import ActionHandler, ActionList, Action
from darts.classes_data import Party, Player, Score
from darts.game_engine import StartParty, AddScore, SetLastPlayer, AddPlayer, InitScore, EndParty, \
    SetWinner

from darts.utils import ActionHandler, action_method


class Party_ActionHandler(ActionHandler):
    def __init__(self, party: Party):
        super().__init__()
        self.party: Party = party

    def _start_party(self) -> Iterator[Action]:
        yield StartParty(party=self.party)

    def _new_empty_score(self, player: Player):
        empty_score = player.scores[-1].update([])
        yield AddScore(party=self.party, player=player, score=empty_score)

    def _skip_to(self, player: Player):
        for player_to_skip in self.party.players_to_skip_to(player):
            yield from self._new_empty_score(player_to_skip)
            yield SetLastPlayer(party=self.party, name=player_to_skip.name)

    def _add_score(self, player: Player, score: Score) -> Iterator[Action]:
        yield from self._skip_to(player)
        yield AddScore(party=self.party, player=player, score=score)
        yield SetLastPlayer(party=self.party, name=player.name)

    def _add_player(self, name: str) -> Iterator[Action]:
        yield AddPlayer(party=self.party, name=name)
        yield InitScore(party=self.party, name=name)
        yield SetLastPlayer(party=self.party, name=name)

    def _add_players(self, names: Iterator[str]) -> Iterator[Action]:
        for name in names:
            yield from self._add_player(name)
        yield from self._start_party()

    def _set_winner(self, winner: Player) -> Iterator[Action]:
        yield SetWinner(party=self.party, winner=winner)
        yield EndParty(party=self.party)

    @action_method
    def start_party(self):
        self.do(ActionList(*self._start_party()))

    @action_method
    def add_score(self, player, score):
        self.do(ActionList(*self._add_score(player, score)))

    @action_method
    def add_player(self, name):
        self.do(ActionList(*self._add_player(name)))

    @action_method
    def add_players(self, names):
        self.do(ActionList(*self._add_players(names)))

    @action_method
    def set_winner(self, winner: Player):
        self.merge_last_do(ActionList(*self._set_winner(winner)))
