from text_engine import *

from darts.commands import *
from darts.constants import KW, CTX


def set_parser_identifiers(parser: Parser):
    parser.add_routine(
        CTX.__GLOBAL__,
        match(Quit.__name__)
        | match(MainMenu.__name__)
        | match(AdjustMic.__name__)
        | match(OpenSettings.__name__)
    )
    parser.add_routine(
        CTX.__SETTINGS__,
        match(SetLang.__name__)
        | match(CTX.__GLOBAL__)
    )
    parser.add_routine(
        CTX.__MAIN_MENU__,
        match(SelectPartyType.__name__)
        | match(CTX.__GLOBAL__)
    )
    parser.add_routine(
        CTX.__GAME__,
        match(Redo.__name__)
        | match(Undo.__name__)
        | match(SaveParty.__name__)
        | match(CTX.__GLOBAL__)
    )
    parser.add_routine(
        CTX.__PRE_GAME__,
        match(AddPlayers.__name__)
        | match(AddPlayer.__name__)
        | match(StartParty.__name__)
        | match(CTX.__GAME__)
    )
    parser.add_routine(
        CTX.__IN_GAME__,
        match(AddScore.__name__)
        | match(CTX.__GAME__)
    )
    parser.add_routine(
        CTX.__POST_GAME__,
        match(CTX.__GAME__)
    )

    parser.add_routine(
        "__scores__",
        match(f"{ScoreValue.__name__} in scores").and_repeat
        & match(KW.AND)
        & match(f"{ScoreValue.__name__} in scores")
    )
    parser.add_routine(
        "__scores__",
        match(f"{ScoreValue.__name__} in scores")
        & (match(KW.PLUS) & match(f"{ScoreValue.__name__} in scores")).and_repeat
    )
    parser.add_routine(
        "__scores__",
        match(f"{ScoreValue.__name__} in scores")
    )
