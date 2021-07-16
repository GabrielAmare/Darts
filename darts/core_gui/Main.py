from tkinter import *

from darts import core_commands as cmd
from darts import errors
from darts.base_commands import Command
from darts.base_gui import Button
from darts.constants import GUI, MainState
from darts.app_service import app_service

from .Body import Body
from .TextFeedBack import TextFeedBack
from .VoiceInterfaceIcon import VoiceInterfaceIcon
from .GameSettings import GameSettings


class Main(Frame):
    def __init__(self, root, **cfg):
        super().__init__(root, **cfg)
        self.widget = None

        self.voice_interface_icon = VoiceInterfaceIcon(self, app_service.voice.vi)
        self.text_feedback = TextFeedBack(self)
        self.quit_button = Button(self, code='APP.QUIT', command=root.on_quit)
        self.menu = Body(self)

        app_service.styles.config(self.voice_interface_icon, 'VoiceInterfaceIcon')
        app_service.styles.config(self.text_feedback, 'TextFeedBack')
        app_service.styles.config(self.quit_button, 'Main.quit_button')
        app_service.styles.config(self.menu, 'Body')

        self.menu.on('select', self.select_tab)
        self.menu.get_tab(GUI.TABS.GAME_MENU).on(GUI.EVENTS.GAME.START, self.start_game)
        self.menu.get_tab(GUI.TABS.GAME_MENU).on(GUI.EVENTS.GAME.SETTINGS, self.open_game_settings)

        self.voice_interface_icon.grid(row=0, column=0, sticky=NSEW)
        self.text_feedback.grid(row=0, column=1, sticky=NSEW)
        self.quit_button.grid(row=0, column=2, sticky=NSEW)
        self.menu.grid(row=1, column=0, columnspan=3, sticky=NSEW)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.menu.select(GUI.TABS.GAME_MENU)

        self.bind_all('<KeyPress-Control_L>', self.on_control)

        self.state = MainState.GAME_MENU

        if app_service.games.has_party():
            self.create_party_scoreboard()

    @property
    def state(self) -> MainState:
        return self._state

    @state.setter
    def state(self, value: MainState):
        self._state = value

        if value is MainState.GAME_MENU:
            app_service.voice.set_time_limit(2)

        elif value is MainState.GAME_SETTINGS:
            app_service.voice.set_time_limit(2)

        elif value is MainState.APP_SETTINGS:
            app_service.voice.set_time_limit(2)

        elif value is MainState.CURRENT_PARTY:
            app_service.voice.set_time_limit(5)

        else:
            app_service.voice.set_time_limit(2)

    def start_game(self, game_uid: str):
        party = None
        if party is None:
            # create a new party
            self.create_party(game_uid)

    def open_game_settings(self, game_uid: str):
        if game_uid not in app_service.games.builders:
            self.close_game_settings()
            return

        config = app_service.games.builders[game_uid].config

        settings_holder = Frame(self.menu)
        app_service.styles.config(settings_holder, 'Main.holder')

        settings = GameSettings(settings_holder, game_uid, config)
        app_service.styles.build(settings, 'GameSettings')

        self.menu.set_tab(GUI.TABS.GAME_SETTINGS, settings_holder)

        self.menu.enable(GUI.TABS.GAME_SETTINGS)
        self.menu.select(GUI.TABS.GAME_SETTINGS)

    def close_game_settings(self):
        self.menu.set_tab(GUI.TABS.GAME_SETTINGS, Frame(self.menu))
        self.menu.disable(GUI.TABS.GAME_SETTINGS)

    def select_tab(self, key: str):
        if key == GUI.TABS.GAME_MENU:
            self.state = MainState.GAME_MENU

        elif key == GUI.TABS.GAME_SETTINGS:
            self.state = MainState.GAME_SETTINGS

        elif key == GUI.TABS.APP_SETTINGS:
            self.state = MainState.APP_SETTINGS

        elif key == GUI.TABS.CURRENT_PARTY:
            self.state = MainState.CURRENT_PARTY

        else:
            raise ValueError(key)

    def on_control(self, _evt):
        try:
            texts = app_service.voice.listen(show_all=True)

        except errors.ListenError as e:
            app_service.logger.error(repr(e))
            message = app_service.messages.translate('APP.DID_NOT_HEAR')
            app_service.voice.speak(message)
            return

        if not texts:
            app_service.logger.error('text inputs are missing')
            message = app_service.messages.translate('APP.DID_NOT_HEAR')
            app_service.voice.speak(message)
            return

        party_state = None if app_service.games.party is None else app_service.games.party.state
        identifier = app_service.engines.get_identifier(self.state, party_state)

        try:
            text, command = app_service.engines.read(identifier, *texts)

            self.text_feedback.success(text, ms=2500)
            app_service.logger.success(f"identifier: {identifier}\n"
                                       f"text : {text!r}\n"
                                       f"command : {command!r}")

        except errors.CommandNotFoundError as e:
            self.text_feedback.error(texts[0], ms=2500)
            app_service.logger.error(f"identifier : {identifier}\n"
                                     f"texts      : {', '.join(map(repr, texts))}\n"
                                     f"error      : {e!r}")
            app_service.voice.speak(app_service.messages.translate('APP.INVALID_COMMAND'))
            return

        try:
            self.execute(command)

        except errors.UnhandledCommand as e:
            self.text_feedback.error(text, ms=2500)
            app_service.logger.error(repr(e))
            app_service.voice.speak(app_service.messages.translate('APP.UNHANDLED_COMMAND'))
            return

    def execute(self, command: Command) -> None:
        if self.state is MainState.GAME_MENU:
            self._execute_game_menu(command)
        elif self.state is MainState.CURRENT_PARTY:
            try:
                app_service.logger.info('Main.execute -> CurrentParty.execute')
                party = app_service.games.party
                party.execute(command)
            except errors.UnhandledCommand:
                self._execute_always(command)
        else:
            self._execute_always(command)

    def _execute_always(self, command: Command) -> None:
        if isinstance(command, cmd.Quit):
            self.quit()
        elif isinstance(command, cmd.AdjustMic):
            app_service.voice.vi.adjust_mic(seconds=command.seconds)
        else:
            raise errors.UnhandledCommand(command)

    def _execute_game_menu(self, command: Command) -> None:
        if isinstance(command, cmd.SelectPartyType):
            self.create_party(command.name)
        else:
            return self._execute_always(command)

    def create_party_scoreboard(self):
        scoreboard_cls = app_service.games.builders[app_service.settings.pfd.game_uid].scoreboard_cls
        scoreboard = scoreboard_cls(self.menu, app_service.games.party)
        app_service.styles.config(scoreboard, 'ScoreBoard')
        self.menu.set_tab(GUI.TABS.CURRENT_PARTY, scoreboard)
        self.menu.enable(GUI.TABS.CURRENT_PARTY)

    def create_party(self, game_uid: str):
        app_service.games.create_party(game_uid)

        self.create_party_scoreboard()

        self.menu.select(GUI.TABS.CURRENT_PARTY)
