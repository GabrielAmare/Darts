from darts.game_engine import ENGINES
from tools import Config
from .constants import *

APP_CFG = {
    "lang_IETF": "fr-FR",
    "lang": "fr",
    "engine": ENGINES["fr"],
    "vi": VI,
    "games": []
}

APP_CONFIG = Config(APP_CFG)
APP_CONFIG.on("lang_IETF", lambda lang_IETF: APP_CONFIG.set("lang", lang_IETF.split("-", 1)[0]))
APP_CONFIG.on("lang_IETF", lambda lang_IETF: APP_CONFIG["vi"].set_lang(lang_IETF))
APP_CONFIG.on("lang", lambda lang: APP_CONFIG.set("engine", ENGINES[lang]))
APP_CONFIG.on("lang", lambda lang: print("changing to " + lang) or setattr(MESSAGES, "lang", lang))

APP_CFG = APP_CONFIG


def set_lang(lang_IETF: str):
    APP_CFG["lang_IETF"] = lang_IETF
    APP_CFG["lang"] = lang_IETF.split("-", 1)[0]
    APP_CFG["engine"] = ENGINES[APP_CFG["lang"]]
    APP_CFG["vi"].set_lang(lang_IETF)
    print(APP_CFG)


def import_game(name, key):
    APP_CFG["games"].append(dict(name=name, key=key))


# set_lang("en-US")

import_game(name="301", key="301")
import_game(name="Cricket", key="cricket")
import_game(name="Round the clock", key="around the clock")
import_game(name="Molkky", key="molkky")
