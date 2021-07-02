from tklib37 import *
from .Party_Cricket import Party_Cricket
from ...app_config import STYLE


class ScoreBoard_Cricket(KeyTable):
    LABEL_CFG = STYLE.SCOREBOARD.LABEL_LG

    DOOR_OPEN = STYLE.SCOREBOARD.CRICKET.DOOR_OPEN
    DOOR_CLOSED = STYLE.SCOREBOARD.CRICKET.DOOR_CLOSED

    DISABLED = STYLE.SCOREBOARD.CRICKET.DISABLED

    DOORS_LABELS = ["15", "16", "17", "18", "19", "20", "BULL"]
    DOORS_VALUES = [15, 16, 17, 18, 19, 20, 25]
    DOORS_ROWS = [1, 2, 3, 4, 5, 6, 7]

    SCORE_COLUMN_LABEL = "_doors"

    def __init__(self, root, party, **cfg):
        super().__init__(root, **cfg)
        self.party = party
        self.party.on("append", "players", self.on_append_player)
        self.party.on("remove", "players", self.on_remove_player)
        self.party.on("update", "last", self.on_set_last)
        self.party.on("start", callback=self.on_start)
        self.party.on("start:undo", callback=self.on_start_undo)

        self.score_column_index = 0
        self.bind_col(key=self.SCORE_COLUMN_LABEL, col=self.score_column_index)

        self.set_widget(row=0, col=self.SCORE_COLUMN_LABEL, text="")

        for row, door, label in zip(self.DOORS_ROWS, self.DOORS_VALUES, self.DOORS_LABELS):
            self.set_widget(row=row, col=self.SCORE_COLUMN_LABEL, text=label)
        self.rowconfigure(8, minsize=10)

        self.set_widget(row=9, col=self.SCORE_COLUMN_LABEL, text="score")

    def on_start(self, **_):
        if len(self.party.players) == 2:
            self.invert_cols(old_col=self.SCORE_COLUMN_LABEL, new_col=self.party.players[0].name)
            self.update_idletasks()

    def on_start_undo(self, **_):
        if len(self.party.players) == 2:
            self.invert_cols(old_col=self.SCORE_COLUMN_LABEL, new_col=self.party.players[0].name)
            self.update_idletasks()

    def set_widget(self, row, col, **cfg):
        if self.get_widget(row, col):
            widget = super().upd_widget(row=row, col=col, **cfg)
        else:
            cnf = self.LABEL_CFG.copy()
            cnf.update(**cfg)
            widget = super().set_widget(row=row, col=col, cls=Label, **cnf)
        return widget

    def on_append_player(self, **cfg):
        player = cfg["item"]
        player.on("append", "scores", self.update_table)
        player.on("remove", "scores", self.update_table)
        self.bind_col(key=player.name, col=player.index + 1)
        self.set_widget(row=0, col=player.name, text=player.name)
        self.update_idletasks()

    def on_remove_player(self, **cfg):
        player = cfg["item"]
        self.del_col(player.name)
        del self.col_map[player.name]
        self.update_idletasks()

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

    def open_door(self, door):
        row = self.DOORS_ROWS[self.DOORS_VALUES.index(door)]
        self.set_widget(row=row, col=self.SCORE_COLUMN_LABEL, **self.DOOR_OPEN)

    def close_door(self, door):
        row = self.DOORS_ROWS[self.DOORS_VALUES.index(door)]
        self.set_widget(row=row, col=self.SCORE_COLUMN_LABEL, **self.DOOR_CLOSED)
        for player in self.party.players:
            self.set_widget(row=row, col=player.name, **self.DISABLED)

    def update_table(self, **_):
        for door, row in zip(self.DOORS_VALUES, self.DOORS_ROWS):
            opener = self.party.opener(door)
            closer = self.party.closer(door)
            for player in self.party.players:
                if len(player.scores):
                    score = player.scores[-1]
                    widget_cfg = self.LABEL_CFG.copy()
                    if player is opener:
                        widget_cfg.update(**self.DOOR_OPEN)
                        widget_cfg["text"] = str(score.get_score(door))
                    else:
                        widget_cfg["text"] = score.get_marks(door) * " I "
                        if player is closer:
                            widget_cfg.update(**self.DOOR_CLOSED)

                    if closer:
                        widget_cfg.update(**self.DISABLED)
                else:
                    widget_cfg = dict(text="")

                self.set_widget(row=row, col=player.name, **widget_cfg)

        for player in self.party.players:
            text = player.scores[-1].score if len(player.scores) else "0"
            self.set_widget(row=9, col=player.name, text=text)

        for row, door in zip(self.DOORS_ROWS, self.DOORS_VALUES):
            if self.party.is_opened(door):
                door_config = self.DOOR_OPEN
            elif self.party.is_closed(door):
                door_config = self.DOOR_CLOSED
            else:
                door_config = self.LABEL_CFG

            self.set_widget(row=row, col=self.SCORE_COLUMN_LABEL, **door_config)

    def feed(self, ms, action, *actions):
        name, cfg = action
        method = getattr(self.party, name)
        method(**cfg)

        if actions:
            self.after(ms, self.feed, ms, *actions)

    def parse_text(self, text):
        return self.party.parse_text(text)


Party_Cricket.tk_scoreboard = lambda party, root, **config: ScoreBoard_Cricket(root, party, **config)
