from text_engine import *
from .commands import *

lexer, parser, astb, engine_fr = base(
    # COMMANDS
    [C_Quit, match("KW_QUIT")],
    [C_SaveParty, match("KW_SAVE_PARTY")],
    [C_MainMenu, match("KW_MAIN_MENU")],
    [C_StartParty, match("KW_OK")],
    [C_SelectPartyType, match("KW_GAME in *")],
    [C_SetLang, match("KW_PASS_TO") & match("KW_LANG as lang_IETF")],
    [
        C_AdjustMic,
        match("KW_ADJUST_MIC") & match("KW_DURING") & match("*.value as seconds") & match("KW_SECONDS"),
        match("KW_ADJUST_MIC"),
    ],
    [C_OpenSettings, match("KW_OPEN_SETTINGS")],
    [C_Redo, match("KW_REDO") & (match("*.value in *") & match("KW_FOIS")).optional],
    [C_Undo, match("KW_UNDO") & (match("*.value in *") & match("KW_FOIS")).optional],
    [C_AddPlayers, match("O_Player in players").and_repeat & match("KW_ET") & (
            match("O_PlayerCP in players") | match("O_Player in players"))],
    [C_AddPlayer, match("O_Player as player")],
    [
        C_AddScore,
        match("__scores__") & match("KW_POUR") & (match("O_PlayerCP as player") | match("O_Player as player")),
        (match("O_PlayerCP as player") | match("O_Player as player")) & match("KW_HAS_DONE") & match("__scores__"),
        match("__scores__"),
    ],
    # OBJECTS
    [O_Player, match("VAR as name")],
    [O_PlayerCP, match("VAR as name1") & match("VAR as name2")],
    [
        O_Score,
        match("*.value as factor") & match("KW_FOIS") & match("*.value as value") & match("KW_POINT").optional,
        match("*.value as value") & match("KW_POINT").optional,
        match("*.fact as factor") & match("*.value as value") & match("KW_POINT").optional,
    ],
    pattern_libs=[]
)
parser.add_routine(
    "__GLOBAL__",
    match("C_Quit")
    | match("C_MainMenu")
    | match("C_AdjustMic")
    | match("C_OpenSettings")
)
parser.add_routine(
    "__SETTINGS__",
    match("C_SetLang")
    | match("__GLOBAL__")
)
parser.add_routine(
    "__MAIN_MENU__",
    match("C_SelectPartyType")
    | match("__GLOBAL__")
)
parser.add_routine(
    "__GAME__",
    match("C_Redo")
    | match("C_Undo")
    | match("C_SaveParty")
    | match("__GLOBAL__")
)
parser.add_routine(
    "__PRE_GAME__",
    match("C_AddPlayers")
    | match("C_AddPlayer")
    | match("C_StartParty")
    | match("__GAME__")
)
parser.add_routine(
    "__IN_GAME__",
    match("C_AddScore")
    | match("__GAME__")
)
parser.add_routine(
    "__POST_GAME__",
    match("__GAME__")
)

parser.add_routine(
    "__scores__",
    match("O_Score in scores").and_repeat & match("KW_ET") & match("O_Score in scores")
)
parser.add_routine(
    "__scores__",
    match("O_Score in scores") & (match("KW_PLUS") & match("O_Score in scores")).and_repeat
)
parser.add_routine(
    "__scores__",
    match("O_Score in scores")
)

# KWS
lexer.add_pattern("KW_ET", mode="kw", expr="et")
lexer.add_pattern("KW_OK", mode="kw", expr="ok")
lexer.add_pattern("KW_POUR", mode="kw", expr="pour")

lexer.add_pattern("KW_POINT", mode="kw", expr=r"points?|"
                                              r"\.")
lexer.add_pattern("KW_FOIS", mode="kw", expr="fois|"
                                             "x")
lexer.add_pattern("KW_PLUS", mode="kw", expr=r"plus|"
                                             r"\+")

lexer.add_pattern("KW_HAS_DONE", mode="kw", expr="a fait|marques?")
lexer.add_pattern("KW_ADJUST_MIC", mode="kw", expr="ajuster? le micro|"
                                                   "ajuster? le microphone|"
                                                   "ajuster? le bruit|"
                                                   "ajuster")
lexer.add_pattern("KW_DURING", mode="kw", expr="pendant|"
                                               "durant")
lexer.add_pattern("KW_SECONDS", mode="kw", expr="secondes?")
lexer.add_pattern("KW_OPEN_SETTINGS", mode="kw", expr="paramètres|"
                                                      "ouvrir les paramètres|"
                                                      "changer les paramètres")
lexer.add_pattern("KW_PASS_TO", mode="kw", expr="passe[rs]? en")

lexer.add_pattern("KW_SAVE_PARTY", mode="kw", expr="sauvegarder la partie|"
                                                   "enregistrer la partie|"
                                                   "sauvegarder|"
                                                   "enregistrer")

lexer.add_pattern("KW_LANG", mode="kw", expr="français", value="fr-FR")
lexer.add_pattern("KW_LANG", mode="kw", expr="anglais", value="en-US")

# QUITTER / MENU PRINCIPAL
lexer.add_pattern("KW_QUIT", mode="kw", expr="quitter")
lexer.add_pattern("KW_MAIN_MENU", mode="kw", expr="menu principal")

# LANCER UNE PARTIE
lexer.add_pattern("KW_GAME", mode="kw", expr="301")
lexer.add_pattern("KW_GAME", mode="kw", expr="501")  # _301 variant
lexer.add_pattern("KW_GAME", mode="kw", expr="801")  # _301 variant
lexer.add_pattern("KW_GAME", mode="kw", expr="cricket")
lexer.add_pattern("KW_GAME", mode="kw", expr="around the clock")
lexer.add_pattern("KW_GAME", mode="kw", expr="alcooliques?")
lexer.add_pattern("KW_GAME", mode="kw", expr="[mM]olkky")

# ANNULER REFAIRE
lexer.add_pattern("KW_UNDO", mode="kw", expr="annuler|"
                                             "oups|"
                                             "oops")
lexer.add_pattern("KW_REDO", mode="kw", expr="restaurer|"
                                             "refaire")

# FACTEURS
lexer.add_pattern("KW_1.value.fact", mode="kw", expr="1|"
                                                     "une?", value=1)
lexer.add_pattern("KW_2.value.fact", mode="kw", expr="2|"
                                                     "de|"
                                                     "deux", value=2)
lexer.add_pattern("KW_3.value.fact", mode="kw", expr="3|"
                                                     "trois", value=3)

lexer.add_pattern("KW_SIMPLE.fact", mode="kw", expr="[Ss]imples?", value=1)
lexer.add_pattern("KW_DOUBLE.fact", mode="kw", expr="[Dd]oubles?", value=2)
lexer.add_pattern("KW_TRIPLE.fact", mode="kw", expr="[Tt]riples?", value=3)
lexer.add_pattern("KW_QUADRUPLE.fact", mode="kw", expr="quadruples?", value=4)
lexer.add_pattern("KW_QUINTUPLE.fact", mode="kw", expr="quintuples?", value=5)
lexer.add_pattern("KW_SEXTUPLE.fact", mode="kw", expr="sextuples?", value=6)
lexer.add_pattern("KW_HEPTUPLE.fact", mode="kw", expr="septuples?", value=7)
lexer.add_pattern("KW_OCTUPLE.fact", mode="kw", expr="octuples?", value=8)
lexer.add_pattern("KW_NINETUPLE.fact", mode="kw", expr="nonuples?", value=9)

# NOMBRES
lexer.add_pattern("KW_BULL.value", mode="kw", expr="[bB]ulle?s?|"
                                                   "[bB]oules?", value=25)
lexer.add_pattern("KW_0.value", mode="kw", expr="zéros?", value=0)
lexer.add_pattern("KW_2.value", mode="kw", expr="deux", value=2)
lexer.add_pattern("KW_4.value", mode="kw", expr="quatre", value=4)
lexer.add_pattern("KW_5.value", mode="kw", expr="V|"
                                                "cinq", value=5)
lexer.add_pattern("KW_6.value", mode="kw", expr="six?", value=6)
lexer.add_pattern("KW_7.value", mode="kw", expr="sept", value=7)
lexer.add_pattern("KW_8.value", mode="kw", expr="huit|"
                                                "oui", value=8)
lexer.add_pattern("KW_9.value", mode="kw", expr="neuf", value=9)
lexer.add_pattern("KW_17.value", mode="kw", expr="X 7", value=17)
lexer.add_pattern("KW_18.value", mode="kw", expr="X 8", value=18)
lexer.add_pattern("KW_19.value", mode="kw", expr="X 9", value=19)
lexer.add_pattern("KW_10.value", mode="kw", expr="X|"
                                                 "dix|"
                                                 "dis", value=10)
lexer.add_pattern("KW_15.value", mode="kw", expr="XV", value=15)
lexer.add_pattern("KW_16.value", mode="kw", expr="XVI", value=16)
lexer.add_pattern("KW_20.value", mode="kw", expr="XX|"
                                                 "vins?|"
                                                 "Vins?|"
                                                 "vent|"
                                                 "vans", value=20)
lexer.add_pattern("KW_30.value", mode="kw", expr="trans|"
                                                 "France", value=30)
lexer.add_pattern("KW_70.value", mode="kw", expr="60 X", value=70)
lexer.add_pattern("KW_90.value", mode="kw", expr="80 X", value=90)
lexer.add_pattern("KW_300.value", mode="kw", expr="croissant", value=300)

lexer.add_pattern("VAR", mode="re", expr="[A-Za-zÀ-ÖØ-öø-ÿ-]+", value=lambda content: content.lower().replace('-', ' '))
lexer.add_pattern("INT.value", mode="re", expr="[0-9]+", value=int)
