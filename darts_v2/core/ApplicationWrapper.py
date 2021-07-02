from typing import Dict, List
import re

from .Application import Application
from .VocalUserInterface import VocalUserInterface
from .GraphicUserInterface import GraphicUserInterface

from .engine import __GAME__, __GLOBAL__, __IN_GAME__, __PRE_GAME__, __POST_GAME__, __MAIN_MENU__, __SETTINGS__
from .commands import Command


class PreProcessor:
    aliases: Dict[str, str]

    def __init_subclass__(cls, **kwargs):
        cls.__functions = []

        for name, meth in cls.__dict__.items():
            if hasattr(meth, "__call__"):
                cls.__functions.append(meth)

    def __call__(self, text: str):
        for old, new in self.aliases.items():
            text = text.replace(old, new)

        for function in self.__functions:
            text = function(self, text)

        return text


class FrenchPreProcessor(PreProcessor):
    aliases = {
        "zéro": "0",
        "un": "1",
        "une": "1",
        "deux": "2",
        "trois": "3",
        "quatre": "4",
        "cinq": "5",
        "six": "6",
        "sept": "7",
        "huit": "8",
        "neuf": "9",

        "triplement": "triple 20",
        "chaise": "16",
        "x 7": "17",
        "x 8": "18",
        "x 9": "19",
        "boules": "bull",
        "boule": "bull",
        ".": "points",
    }

    def consecutive_four_digits(self, text: str) -> str:
        while True:
            match = re.match(r".*(?P<expr>[0-9]{4}).*", text)
            if match:
                expr = match.group("expr")
                l, r = expr[:2], expr[2:]
                text = text.replace(expr, l + " " + r)
            else:
                return text

    def multiple_spaces(self, text: str) -> str:
        while "  " in text:
            text = text.replace("  ", " ")
        return text


class FrenchProcessor:
    patterns = {
        "<int>": re.compile("[0-9]+"),
        "<quit>": "quitter",
        "<redo>": "refaire",
        "<undo>": "annuler",
        "<kw_game>": ["_301", "round the clock", "molkky", "cricket"],
        "<players>": ["<player*players> <players>", "<player*players>"],
        "[new_game_with]": "nouvelle partie de <game> avec <players>"
    }

    def __call__(self, text: str) -> object:
        words = text.split(" ")
        print(words)
        return words


fr_pp = FrenchPreProcessor()
fr_p = FrenchProcessor()


class ApplicationWrapper:
    app: Application
    vui: VocalUserInterface
    gui: GraphicUserInterface

    def __init__(self, config_fp: str):
        self.app = Application(self, config_fp)
        self.vui = VocalUserInterface(self.app)
        self.gui = GraphicUserInterface(self.app)

        self.gui.bind("<Control_L>", self.on_control)

        # self.app.on("feedback_icon", lambda value: self.app.console.log(f"feedback_icon set to {value!r}"))

    def run(self):
        """mainloop of the program"""
        self.gui.mainloop()

    def text_to_command(self, text: str):
        raise NotImplementedError

    def command_to_action(self, command):
        raise NotImplementedError

    def apply_action(self, action):
        raise NotImplementedError

    def listen(self, save_audio: str = "") -> List[str]:
        return self.vui.listen(show_all=True, save_audio=save_audio)

    def speak(self, text: str):
        duration = self.vui.speak(text)
        self.gui.after(int(1000 * duration), lambda: setattr(self.app, "feedback_icon", "neutral"))

    def show_message(self, text: str):
        self.app.feedback_text = ""
        if text != "":
            self.app.feedback_text = text

    def _make_commands(self, texts: List[str]) -> Dict[str, Command]:
        commands: Dict[str, Command] = {}
        for text in texts:
            if text not in commands:
                command = self.app.engine.read(text.lower(), identifier=__MAIN_MENU__)
                if command is not None:
                    if command not in commands.values():
                        commands[text] = command

        return commands

    def on_control(self, _):
        # listen to the user
        # extract all the possible text representations of the user speech
        import os
        from datetime import datetime
        now = datetime.now()
        log_fp = self.app.logs_fp + f"{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}_{now.microsecond}/"
        os.mkdir(log_fp)

        try:
            texts: List[str] = self.listen(save_audio=log_fp + "speech.mp3")
        except TypeError:
            self.show_message("")
            self.speak("je n'ai pas entendu")
            return

        # for each possible text, try to find an associated command
        commands: Dict[str, Command] = self._make_commands(texts)

        if not commands:
            self.show_message("")
            self.speak("je n'ai pas compris")
            return

        output_text = "\n".join(
            f"{text!r}\n{command!s}" for text, command in commands.items()
        )

        self.show_message(output_text)

        # duration = self.vui.speak(text)
        # self.gui.after(int(1000 * duration), lambda: setattr(self.app, "feedback_icon", "neutral"))
