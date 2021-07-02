import difflib
import sys

from models37 import *
from tools37 import JsonLoader

from darts.actions import ActionHandler, ActionList
from darts.commands import CommandHandler
from darts.functions import translate

from darts import actions as act, commands as cmd

from darts.vocal_errors import *


@Field.rpy("!party[Party]", show=False)
@Field.rpy("!index[int]", default=lambda target, **_: len(target.party.players))
@Field.rpy("!name[str]")
@Field.rpy("*scores[Score]", show=False)
class Player(Model):
    pass


@Field.rpy("!player[Player]")
@Field.rpy("!score[int]")
@Field.rpy("!index[int]")
class Score(Model):
    @property
    def party(self):
        return self.player.party

    def update(self, scores: List[cmd.O_Score]):
        raise NotImplementedError


class Party_ActionHandler(ActionHandler):
    def __init__(self, party):
        super().__init__()
        self.party = party

    def _start_party(self):
        return act.A_StartParty(party=self.party)

    def _add_score(self, player, score):
        actions = ActionList()

        for skip in self.party.players_to(player):
            empty_score = skip.scores[-1].update([])
            actions.append(act.A_AddScore(party=self.party, player=skip, score=empty_score))
            actions.append(act.A_SetLastPlayer(party=self.party, name=skip.name))

        actions.append(act.A_AddScore(party=self.party, player=player, score=score))
        actions.append(act.A_SetLastPlayer(party=self.party, name=player.name))

        return actions

    def _add_player(self, name):
        # name = parse_player_name(name)
        return ActionList(
            act.A_AddPlayer(party=self.party, name=name),
            act.A_InitScore(party=self.party, name=name, score_cls=self.party.Score),
            act.A_SetLastPlayer(party=self.party, name=name)
        )

    def _add_players(self, names):
        action = ActionList()
        for name in names:
            action.extend(self._add_player(name))
        action.append(self._start_party())

        return action

    def _set_winner(self, winner: Player):
        return ActionList(
            act.A_SetWinner(party=self.party, winner=winner),
            act.A_EndParty(party=self.party)
        )

    def start_party(self):
        self.do(self._start_party())

    def add_score(self, player, score):
        self.do(self._add_score(player, score))

    def add_player(self, name):
        self.do(self._add_player(name))

    def add_players(self, names):
        self.do(self._add_players(names))

    def set_winner(self, winner: Player):
        self.merge_last_do(self._set_winner(winner))


@Field.rpy("*players[Player]", show=False)
@Field.rpy("?last[Player]")
@Field.rpy("!started[bool]", default=False)
@Field.rpy("?winner[Player]")
@Field.rpy("!over[bool]", default=False)
class Party(Model, CommandHandler):
    Score: type
    Player = Player
    tk_scoreboard: callable

    ActionHandler = Party_ActionHandler

    STATES = ["__PRE_GAME__", "__IN_GAME__", "__POST_GAME__"]
    COMMAND_HANDLERS = {
        cmd.C_AddPlayers: "add_players",
        cmd.C_AddPlayer: "add_player",
        cmd.C_StartParty: "start_party",
        cmd.C_AddScore: "on_add_score",
        cmd.C_Undo: "undo",
        cmd.C_Redo: "redo",
        cmd.C_SetWinner: "on_set_winner"
    }

    def __init__(self, vi, **config):
        self.vi = vi
        self.ah = self.ActionHandler(self)

        Model.__init__(self, **config)
        CommandHandler.__init__(self, "__PRE_GAME__")

    def do(self, *actions):
        self.ah.do(*actions)

    def undo(self, command: cmd.C_Undo):
        self.ah.undo(command.times)

    def redo(self, command: cmd.C_Redo):
        self.ah.redo(command.times)

    def players_to(self, player):
        """Return the list of players that needs to play before it comes to `player`"""
        at_index = self.last.index
        to_index = player.index

        delta = to_index - at_index - 1
        if len(self.players):
            number = delta % len(self.players)

            for plus in range(1, number + 1):
                yield self.players[(at_index + plus) % len(self.players)]

    ####################################################################################################################
    # ENGINE METHODS
    ####################################################################################################################

    def add_players(self, command: cmd.C_AddPlayers):
        if self.started:
            raise PartyAlreadyStartedError()

        if self.over:
            raise PartyAlreadyOverError()

        self.ah.add_players([player.name for player in command.players])

        self.vocal_feedback("GAME_START")

    def add_player(self, command: cmd.C_AddPlayer):
        if self.started:
            raise PartyAlreadyStartedError()

        if self.over:
            raise PartyAlreadyOverError()

        self.ah.add_player(command.player.name)

    def start_party(self, _command: cmd.C_StartParty):
        if self.started:
            raise PartyAlreadyStartedError()

        if self.over:
            raise PartyAlreadyOverError()

        self.ah.start_party()

        self.vocal_feedback("GAME_START")

    ####################################################################################################################
    # MISC
    ####################################################################################################################

    def remove_player(self, name):
        for player in self.players:
            if player.name == name:
                for score in player.scores:
                    self.players.scores.remove(score)
                self.players.remove(player)

    def get_player(self, nameOrIndex):
        if nameOrIndex is None:  # get next player
            return self.get_player(self.last.index + 1)
        elif isinstance(nameOrIndex, int):
            return self.players[nameOrIndex % len(self.players)]
        elif isinstance(nameOrIndex, str):
            for player in self.players:
                if player.name == nameOrIndex:
                    return player
            else:
                # partial match
                ratios = {}
                for player in self.players:
                    ratio = difflib.SequenceMatcher(isjunk=None, a=nameOrIndex, b=player.name).ratio()
                    ratios[player] = ratio
                # print(ratios)
                max_ratio = max(ratios.values(), default=0)
                ratios = dict((player, ratio) for player, ratio in ratios.items() if ratio == max_ratio)
                if len(ratios) == 1:
                    player, ratio = list(ratios.items())[0]
                    if ratio >= 0.75:
                        return player
        else:
            raise ValueError(f"Invalid type for Party.get_player(nameOrIndex: {type(nameOrIndex).__name__})"
                             f" expected (str|int)")

    def start(self):
        self.vi.time_limit = 4
        self.ah.start_party()
        self.state = "__IN_GAME__"

    def update_winner(self):
        pass

    def set_winner(self, winner):
        self.ah.set_winner(winner)

    def on_error(self, match):
        self.emit("error", content=match["content"])

    verbose_prefixes = ["GLOBAL"]

    def get_verbose(self, code, config):
        for prefix in self.verbose_prefixes:
            try:
                return translate(
                    code=f"{prefix}.{code}",
                    rand=True,
                    config=config
                )
            except JsonLoader.CodeNotFoundError:
                continue
        else:
            raise JsonLoader.CodeNotFoundError(code=code)

    def vocal_feedback(self, code, **config):
        message = self.get_verbose(code, config)
        if message:
            return self.vi.speak(message)
        else:
            print(f"No message found for : {repr(code)}", file=sys.stderr)

    def on_add_score(self, command: cmd.C_AddScore):
        raise NotImplementedError

    def on_add_score_before(self, command: cmd.C_AddScore):
        if not self.started:
            raise PartyNotStartedError()

        if self.over:
            raise PartyAlreadyOverError()

        if command.player is None:
            player = self.get_player(self.last.index + 1)
        else:
            player = self.get_player(command.player.name)

        if not player:
            raise PlayerNotFoundError(player_name=command.player.name or translate("APP.THIS_PLAYER"))

        try:
            score = player.scores[-1].update(command.scores)

        except FieldCheckError:
            raise InvalidScoreError()

        self.ah.add_score(player, score)

        if len(self.players) == 0:
            self.set_winner(None)
        else:
            self.update_winner()

        return player, score

    def on_add_score_after(self, player):
        if not self.over:
            next_player = self.get_player(player.index + 1)
            self.vocal_feedback("ANNOUNCE_NEXT_PLAYER", name=next_player.name)
            return self.on_next_player(next_player)

        if self.winner:
            self.vocal_feedback("GAME_WON_BY", name=self.winner.name)
        else:
            self.vocal_feedback("GAME_OVER_NO_WINNER")

    def on_next_player(self, player):
        pass
