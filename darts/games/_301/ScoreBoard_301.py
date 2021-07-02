from tklib37 import *
from .Party_301 import Party_301
from ...app_config import STYLE


class ScoreBoard_301(KeyTable):
    LABEL_CFG = STYLE.SCOREBOARD.LABEL

    def __init__(self, root, party, **cfg):
        super().__init__(root, **cfg)
        self.party = party
        self.party.on("append", "players", self.on_append_player)
        self.party.on("remove", "players", self.on_remove_player)

        self.party.on("update", "last", self.on_set_last)

    def on_set_last(self, **cfg):
        last = cfg["value"]

        if last is None:
            next_player_index = 0
        else:
            next_player_index = (last.index + 1) % len(self.party.players)

        for player in self.party.players:
            is_next_player = player.index == next_player_index

            widget_cfg = self.LABEL_CFG.copy()
            if is_next_player:
                widget_cfg.update(STYLE.SCOREBOARD.ACTIVE_PLAYER)

            self.upd_widget(row=0, col=player.name, **widget_cfg)

        self.update_idletasks()

    def set_widget(self, row, col, **cfg):
        if self.get_widget(row, col):
            widget = super().upd_widget(row=row, col=col, **cfg)
        else:
            widget = super().set_widget(row=row, col=col, cls=Label, **cfg, **self.LABEL_CFG)

        self.rowconfigure(row, weight=0)
        self.update_idletasks()
        return widget

    def on_append_player(self, **cfg):
        player = cfg["item"]
        player.on("append", "scores", self.on_append_score)
        player.on("remove", "scores", self.on_remove_score)
        self.bind_col(key=player.name, col=player.index + 1)
        self.set_widget(row=0, col=player.name, text=player.name)
        self.update_idletasks()

    def on_remove_player(self, **cfg):
        player = cfg["item"]
        self.del_col(player.name)
        del self.col_map[player.name]
        self.update_idletasks()

    def on_append_score(self, **cfg):
        score = cfg["item"]
        self.set_widget(row=score.index + 1, col=score.player.name, text=score.score)

    def on_remove_score(self, **cfg):
        score = cfg["item"]
        self.del_widget(row=score.index + 1, col=score.player.name)

    def feed(self, ms, action, *actions):
        name, cfg = action
        method = getattr(self.party, name)
        method(**cfg)

        if actions:
            self.after(ms, self.feed, ms, *actions)


Party_301.tk_scoreboard = lambda party, root, **config: ScoreBoard_301(root, party, **config)
