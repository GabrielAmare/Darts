from tkinter import *

from darts.app_config import APP_CFG, set_lang
from darts import commands as cmd
from darts.constants import STYLE
from darts.functions import translate, auto_translate, log

from darts.games import *
from darts.vocal_errors import *
from tools import VoiceInterface
from .AppHeader import AppHeader
from .MainMenu import MainMenu
from .PartyHandler import PartyHandler
from .SettingsMenu import SettingsMenu
from .base import Interface, NoteBook


class AppInterface(Interface, cmd.CommandManager):
    DEBUG = False

    vi: VoiceInterface
    command_parser: cmd.CommandParser
    STATES = ["__GLOBAL__", "__MAIN_MENU__", "__SETTINGS__"]

    def __init__(self, root, **cfg):
        Interface.__init__(self, root, **cfg)
        cmd.CommandManager.__init__(self, vi=APP_CFG['vi'], engine=APP_CFG['engine'])
        self.identifier: str = "__GLOBAL__"

        self.PARTY_TYPES = {
            "301": (Party_301, 3),
            "501": (lambda vi, **cfg: Party_301(vi, **cfg, total=501), 3),
            "801": (lambda vi, **cfg: Party_301(vi, **cfg, total=801), 3),
            "cricket": (Party_Cricket, 5),
            "around the clock": (Party_RTC, 3),
            "Around the Clock": (Party_RTC, 3),
            "alcoolique": (Party_Alcoholic, 3),
            "molkky": (Party_Molkky, 3),
            "Molkky": (Party_Molkky, 3),
        }

        self.vi = APP_CFG["vi"]

        # self.command_parser = cmd.CommandParser(vi=self.vi, engine=APP_CFG["engine"])

        self.header = AppHeader(self, **STYLE.APP_HEADER.CFG)
        self.header.pack(side=TOP, fill=X)

        self.init_notebook()
        self.init_voice_interface()

        # REGISTER KEYBOARD EVENTS
        self.bind_all("<KeyPress-Control_L>", self.on_control)

        self.nb.disable("party")
        self.nb.active("main_menu")

    def init_notebook(self):
        # NOTE BOOK CONFIGURATION
        self.nb = NoteBook(self)
        self.nb.pack(side=TOP, fill=BOTH, expand=True)

        self.nb.config(**STYLE.APP_INTERFACE.FRAME)
        self.nb.head.config(**STYLE.APP_INTERFACE.FRAME)
        self.nb.body.config(**STYLE.APP_INTERFACE.FRAME)

        self.nb.styles["active"] = STYLE.APP_INTERFACE.TAB_ACTIVE
        self.nb.styles["enabled"] = STYLE.APP_INTERFACE.TAB_ENABLED
        self.nb.styles["disabled"] = STYLE.APP_INTERFACE.TAB_DISABLED

        # MAIN MENU
        button, widget = self.nb.append(
            key="main_menu",
            text=translate("APP.MAIN_MENU"),
            cls=MainMenu,
            cfg=dict(app=self, **STYLE.APP_INTERFACE.TAB_BODY)
        )
        auto_translate("APP.MAIN_MENU", lambda text, button=button: button.configure(text=text))
        # SETTINGS
        button, widget = self.nb.append(
            key="settings",
            text=translate("APP.SETTINGS"),
            cls=SettingsMenu,
            cfg=STYLE.APP_INTERFACE.TAB_BODY
        )
        auto_translate("APP.SETTINGS", lambda text, button=button: button.configure(text=text))
        # PARTY HOLDER
        button, widget = self.nb.append(
            key="party",
            text=translate("APP.NO_PARTY"),
            cls=PartyHandler,
            cfg=STYLE.APP_INTERFACE.TAB_BODY
        )
        auto_translate("APP.NO_PARTY", lambda text, button=button: button.configure(text=text))

        # REGISTER NB EVENTS
        self.nb.on("active", self.on_active)

    def init_voice_interface(self):
        # REGISTER VI EVENTS
        self.vi.on("listen:start", lambda: self.header.set_icon("listening"))
        self.vi.on("listen:end", lambda: self.header.set_icon("neutral"))
        self.vi.on("listen:error", lambda: self.header.set_icon("error"))

        self.vi.on("speak:start", lambda: self.header.set_icon("speaking"))
        self.vi.on("speak:end", lambda: self.header.set_icon("neutral"))

        self.vi.on("adjust_mic:start", lambda: self.header.set_icon("adjusting"))
        self.vi.on("adjust_mic:end", lambda: self.header.set_icon("neutral"))

    @property
    def party_handler(self) -> PartyHandler:
        return self.nb.get("party")

    @property
    def party(self):
        return self.party_handler.party

    def on_active(self, key: str):
        if key == "main_menu":
            self.vi.time_limit = 2
            self.identifier = "__MAIN_MENU__"
            # self.set_command_handler(None)
        elif key == "settings":
            self.vi.time_limit = 2
            self.identifier = "__SETTINGS__"
            # self.set_command_handler(None)
        elif key == "party":
            self.vi.time_limit = 5
            self.identifier = "__GLOBAL__"
            # self.set_command_handler(self.party)
            # self.nb.disable("main_menu")
        else:
            raise ValueError(key)

    def say(self, code: str):
        self.vi.speak(translate(code))

    def handle_error(self, error: Exception, command):
        if isinstance(error, CommandNotFoundError):
            self.display_error_for(error.texts[0], 1000)

        if isinstance(error, VocalError):
            error.command = command
            error.vocalize()

        log(error)

    def on_control(self, _=None):
        self.listen(self.identifier)

        # if self.command_handler is None:
        #     identifier = self.state
        # else:
        #     identifier = self.command_handler.state
        #
        # command = None
        # try:
        #     text, command = self.command_parser.listen(identifier=identifier)
        #     self.display_success_for(text, 1000)
        #     self.execute_command(command)
        #
        # except Exception as error:
        #     self.handle_error(error, command)

    def _display_text(self, text: str, ms: int, **cfg):
        key = self.header.append_text(text, **cfg)
        self.after(ms, self.header.remove_text, key)

    def display_text(self, text: str, ms: int):
        self._display_text(text, ms, **STYLE.APP_INTERFACE.TEXT.NORMAL)

    def display_error_for(self, text: str, ms: int):
        self._display_text(text, ms, **STYLE.APP_INTERFACE.TEXT.ERROR)

    def display_warning_for(self, text: str, ms: int):
        self._display_text(text, ms, **STYLE.APP_INTERFACE.TEXT.WARNING)

    def display_success_for(self, text: str, ms: int):
        self._display_text(text, ms, **STYLE.APP_INTERFACE.TEXT.SUCCESS)

    display_text_for = display_text

    # COMMANDS METHODS

    @cmd.handler(cmd.MainMenu)
    def on_main_menu(self, _command: cmd.MainMenu = None):
        self.nb.active("main_menu")

    @cmd.handler(cmd.OpenSettings)
    def on_open_settings(self, _command: cmd.OpenSettings = None):
        self.nb.active("settings")

    @cmd.handler(cmd.SelectPartyType)
    def on_select_party_type(self, command: cmd.SelectPartyType):
        if command.name not in self.PARTY_TYPES:
            self.display_error_for(command.name, 1000)
            self.say("APP.UNRECOGNIZED_GAME")

        party_cls, time_limit = self.PARTY_TYPES[command.name]

        self.party_handler.party = party_cls(self.vi)

        self.nb.tabs["party"]["button"].config(text=translate("APP.PARTY_OF", config=dict(game=command.name)))

        self.nb.enable("party")
        self.nb.active("party")

    @cmd.handler(cmd.SetLang)
    def on_set_lang(self, command: cmd.SetLang):
        set_lang(command.lang_IETF)
        self.command_parser.engine = APP_CFG["engine"]

    @cmd.handler(cmd.Quit)
    def on_quit(self, _command: cmd.Quit = None):
        self.master.on_quit()

    @cmd.handler(cmd.AdjustMic)
    def on_adjust_mic(self, command: cmd.AdjustMic):
        self.vi.adjust_mic(command.seconds)
