from tkinter import *

from darts.ScoreTextInput import ScoreTextInput
from darts.app_data import app_data


class ScoreBoardHandler(Frame):
    """This widget will contains a scoreboard and the text entry."""

    def __init__(self, root, command_callback, **cfg):
        super().__init__(root, **cfg)
        self.command_callback = command_callback

        game = app_data.get_current_game()
        self.scoreboard = game.score_board_cls(self, app_data.party)
        app_data.styles.build(self.scoreboard, 'ScoreBoard')

        self.text: ScoreTextInput = ScoreTextInput()
        self.entry = Label(self, text=self.text)
        app_data.styles.build(self.entry, 'ScoreBoardHandler.entry')

    def handle_keypress(self, evt):
        """Handle the keys pressed."""
        if evt.char in '0123456789':
            self.text.add_digit(evt.char)
        elif evt.char == '+':
            self.text.add_score()
        elif evt.char == '*':
            self.text.mul_score()
        elif evt.char == '\x08':
            self.text.del_last()
        elif evt.char == '\r':
            self.confirm_text_input()
        # additional characters.
        elif evt.char == 'b':  # BULL shortcut.
            self.text.add_digit('2')
            self.text.add_digit('5')

        self.update()

    def confirm_text_input(self):
        """This will use the current value of self.text as an AddScore command."""
        command = self.text.as_command()
        self.text.reset()
        self.update()
        self.command_callback(command)

    def update(self):
        self.entry.config(text=str(self.text))
