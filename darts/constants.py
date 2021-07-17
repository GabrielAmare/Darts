import os
from enum import Enum, auto


class CTX:
    __GLOBAL__ = "__GLOBAL__"
    __SETTINGS__ = "__SETTINGS__"
    __MAIN_MENU__ = "__MAIN_MENU__"
    __GAME__ = "__GAME__"
    __PRE_GAME__ = "__PRE_GAME__"
    __IN_GAME__ = "__IN_GAME__"
    __POST_GAME__ = "__POST_GAME__"


class KW:
    """Engines Key Words"""

    OK = "KW_OK"
    FOR = "KW_FOR"
    AND = "KW_AND"
    QUIT = "KW_QUIT"
    REDO = "KW_REDO"
    UNDO = "KW_UNDO"
    PLUS = "KW_PLUS"
    LANG = "KW_LANG"
    GAME = "KW_GAME"
    POINT = "KW_POINT"
    TIMES = "KW_TIMES"
    DURING = "KW_DURING"
    PASS_TO = "KW_PASS_TO"
    SECONDS = "KW_SECONDS"
    HAS_DONE = "KW_HAS_DONE"
    MAIN_MENU = "KW_MAIN_MENU"
    SAVE_PARTY = "KW_SAVE_PARTY"
    ADJUST_MIC = "KW_ADJUST_MIC"
    OPEN_SETTINGS = "KW_OPEN_SETTINGS"


class GUI:
    """Graphic User Interface"""

    class TABS:
        GAME_MENU = "game_menu"
        CURRENT_PARTY = "current_party"
        GAME_SETTINGS = "game_settings"
        APP_SETTINGS = "app_settings"

    class EVENTS:
        SELECT = "select"

        class GAME:
            START = "start"
            SETTINGS = "settings"


class VI:
    """Vocal Interface"""

    class EVENTS:
        class LISTEN:
            START = "listen:start"
            END = "listen:end"
            ERROR = "listen:error"

        class SPEAK:
            START = "speak:start"
            END = "speak:end"

        class ADJUST:
            START = "adjust_mic:start"
            END = "adjust_mic:end"


class MainState(Enum):
    GAME_MENU = auto()
    APP_SETTINGS = auto()
    GAME_SETTINGS = auto()
    CURRENT_PARTY = auto()


class PartyState(Enum):
    BEFORE = auto()  # the game have been create but not started
    DURING = auto()  # the game have been started and can be played
    AFTER = auto()  # the game is over


class TextMode(Enum):
    NORMAL = auto()
    RANDOM = auto()
    MULTILINE = auto()


HOME = os.path.expanduser('~')
