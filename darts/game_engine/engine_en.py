from text_engine import *
from darts import commands as cmd

lexer, parser, astb, engine_en = base(
    # COMMANDS
    [cmd.Quit, match("KW_QUIT")],
    [cmd.MainMenu, match("KW_MAIN_MENU")],
    [cmd.StartParty, match("KW_OK")],
    [cmd.SelectPartyType, match("KW_GAME in *")],
    [
        cmd.AdjustMic,
        match("KW_ADJUST_MIC") & match("KW_DURING") & match("*.value as seconds") & match("KW_SECONDS"),
        match("KW_ADJUST_MIC"),
    ],
    [
        cmd.Redo,
        match("KW_REDO") & match("*.value.mod in *"),
        match("KW_REDO") & (match("*.value in *") & match("KW_FOIS")).optional
    ],
    [
        cmd.Undo,
        match("KW_UNDO") & match("*.value.mod in *"),
        match("KW_UNDO") & (match("*.value in *") & match("KW_FOIS")).optional
    ],
    [cmd.AddPlayers, match("O_Player in players").and_repeat & match("KW_ET") & (match("O_PlayerCP in players") | match("O_Player in players"))],
    [cmd.AddPlayer, match("O_Player as player")],
    [
        cmd.AddScore,
        match("__scores__") & match("KW_POUR") & (match("O_PlayerCP as player") | match("O_Player as player")),
        (match("O_PlayerCP as player") | match("O_Player as player")) & match("KW_HAS_DONE") & match("__scores__"),
        match("__scores__"),
    ],
    # OBJECTS
    [cmd.O_Player, match("VAR as name")],
    [cmd.O_PlayerCP, match("VAR as name1") & match("VAR as name2")],
    [
        cmd.O_Score,
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
    match("O_Score in scores")
)

# KWS
lexer.add_pattern("KW_FOIS", mode="kw", expr="times?|x")
lexer.add_pattern("KW_ET", mode="kw", expr="and")
lexer.add_pattern("KW_OK", mode="kw", expr="ok")

lexer.add_pattern("KW_POUR", mode="kw", expr="for")
lexer.add_pattern("KW_POINT", mode="kw", expr=r"points?|\.")
lexer.add_pattern("KW_HAS_DONE", mode="kw", expr="has done")
lexer.add_pattern("KW_ADJUST_MIC", mode="kw", expr="adjust the mic|adjust the microphone|adjust the noise")
lexer.add_pattern("KW_DURING", mode="kw", expr="for")
lexer.add_pattern("KW_SECONDS", mode="kw", expr="seconds?")
lexer.add_pattern("KW_OPEN_SETTINGS", mode="kw", expr="settings|open (the)? settings|change (the)? settings")
lexer.add_pattern("KW_PASS_TO", mode="kw", expr="(turn|pass) to")

lexer.add_pattern("KW_LANG", mode="kw", expr="french", value="fr-FR")
lexer.add_pattern("KW_LANG", mode="kw", expr="english", value="en-US")

# QUITTER / MENU PRINCIPAL
lexer.add_pattern("KW_QUIT", mode="kw", expr="quit")
lexer.add_pattern("KW_MAIN_MENU", mode="kw", expr="main menu")

# LANCER UNE PARTIE
lexer.add_pattern("KW_GAME", mode="kw", expr="_301")
lexer.add_pattern("KW_GAME", mode="kw", expr="cricket")
lexer.add_pattern("KW_GAME", mode="kw", expr="around the clock")
lexer.add_pattern("KW_GAME", mode="kw", expr="Around the Clock")

# ANNULER REFAIRE
lexer.add_pattern("KW_UNDO", mode="kw", expr="cancel|oops|undo")
lexer.add_pattern("KW_REDO", mode="kw", expr="restore|redo")

# FACTEURS
lexer.add_pattern("KW_1.value.fact", mode="kw", expr="1|one", value=1)
lexer.add_pattern("KW_2.value.fact", mode="kw", expr="2|two", value=2)
lexer.add_pattern("KW_3.value.fact", mode="kw", expr="3|three", value=3)

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
lexer.add_pattern("KW_BULL.value", mode="kw", expr="[bB]ull", value=25)
lexer.add_pattern("KW_0.value", mode="kw", expr="zeros?", value=0)
lexer.add_pattern("KW_2.value", mode="kw", expr="two", value=2)
lexer.add_pattern("KW_2.value.mod", mode="kw", expr="twice", value=2)
lexer.add_pattern("KW_4.value", mode="kw", expr="four", value=4)
lexer.add_pattern("KW_5.value", mode="kw", expr="V|five", value=5)
lexer.add_pattern("KW_6.value", mode="kw", expr="six?", value=6)
lexer.add_pattern("KW_7.value", mode="kw", expr="seven", value=7)
lexer.add_pattern("KW_8.value", mode="kw", expr="eight|oui", value=8)
lexer.add_pattern("KW_9.value", mode="kw", expr="nine", value=9)
lexer.add_pattern("KW_17.value", mode="kw", expr="X 7", value=17)
lexer.add_pattern("KW_18.value", mode="kw", expr="X 8", value=18)
lexer.add_pattern("KW_19.value", mode="kw", expr="X 9", value=19)
lexer.add_pattern("KW_10.value", mode="kw", expr="X|ten", value=10)
lexer.add_pattern("KW_15.value", mode="kw", expr="XV", value=15)
lexer.add_pattern("KW_16.value", mode="kw", expr="XVI", value=16)
lexer.add_pattern("KW_20.value", mode="kw", expr="XX|twenty", value=20)
lexer.add_pattern("KW_70.value", mode="kw", expr="60 X", value=70)
lexer.add_pattern("KW_90.value", mode="kw", expr="80 X", value=90)

lexer.add_pattern("VAR", mode="re", expr="[a-zA-Z-]+", value=lambda content: content.lower().replace('-', ' '))
lexer.add_pattern("INT.value", mode="re", expr="[0-9]+", value=int)

lexer.add_pattern("SPACE", mode="re", expr="[ \t\n]+", flag=16, ignore=True, priority=1000)
lexer.add_pattern("ERROR", mode="re", expr=".+", flag=16, priority=1000)
