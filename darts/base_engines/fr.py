from text_engine import *

from darts.commands import *
from darts.constants import KW, CTX
from .utils import set_parser_identifiers

PNC = PlayerNameCompound.__name__
PN = PlayerName.__name__

lexer, parser, astb, engine_fr = base(
    # COMMANDS
    [Quit, match(KW.QUIT)],
    [SaveParty, match(KW.SAVE_PARTY)],
    [MainMenu, match(KW.MAIN_MENU)],
    [StartParty, match(KW.OK)],
    [SelectPartyType, match(f"{KW.GAME} in *")],
    [SetLang, match(KW.PASS_TO) & match(f"{KW.LANG} as lang_IETF")],
    [
        AdjustMic,
        match(KW.ADJUST_MIC) & match(KW.DURING) & match("*.value as seconds") & match(KW.SECONDS),
        match(KW.ADJUST_MIC),
    ],
    [OpenSettings, match(KW.OPEN_SETTINGS)],
    [Redo, match(KW.REDO) & (match("*.value in *") & match(KW.TIMES)).optional],
    [Undo, match(KW.UNDO) & (match("*.value in *") & match(KW.TIMES)).optional],
    [AddPlayers, match(f"{PN} in players").and_repeat & match(KW.AND) & (
            match(f"{PNC} in players") | match(f"{PN} in players"))],
    [AddPlayer, match(f"{PN} as player")],
    [
        AddScore,
        match("__scores__") & match(KW.FOR) & (match(f"{PNC} as player") | match(f"{PN} as player")),
        (match(f"{PNC} as player") | match(f"{PN} as player")) & match(KW.HAS_DONE) & match("__scores__"),
        match("__scores__"),
    ],
    # OBJECTS
    [PlayerName, match("VAR as name")],
    [PlayerNameCompound, match("VAR as name1") & match("VAR as name2")],
    [
        ScoreValue,
        match("*.value as factor") & match(KW.TIMES) & match("*.value as value") & match(KW.POINT).optional,
        match("*.value as value") & match(KW.POINT).optional,
        match("*.fact as factor") & match("*.value as value") & match(KW.POINT).optional,
    ],
    pattern_libs=[]
)

set_parser_identifiers(parser)

# KWS
lexer.add_pattern(KW.AND, mode="kw", expr="et")
lexer.add_pattern(KW.OK, mode="kw", expr="ok")
lexer.add_pattern(KW.FOR, mode="kw", expr="pour")

lexer.add_pattern(KW.POINT, mode="kw", expr=r"points?|"
                                            r"\.")
lexer.add_pattern(KW.TIMES, mode="kw", expr="fois|"
                                            "x")
lexer.add_pattern(KW.PLUS, mode="kw", expr=r"plus|"
                                           r"\+")

lexer.add_pattern(KW.HAS_DONE, mode="kw", expr="a fait|marques?")
lexer.add_pattern(KW.ADJUST_MIC, mode="kw", expr="ajuster? le micro|"
                                                 "ajuster? le microphone|"
                                                 "ajuster? le bruit|"
                                                 "ajuster")
lexer.add_pattern(KW.DURING, mode="kw", expr="pendant|"
                                             "durant")
lexer.add_pattern(KW.SECONDS, mode="kw", expr="secondes?")
lexer.add_pattern(KW.OPEN_SETTINGS, mode="kw", expr="paramètres|"
                                                    "ouvrir les paramètres|"
                                                    "changer les paramètres")
lexer.add_pattern(KW.PASS_TO, mode="kw", expr="passe[rs]? en")

lexer.add_pattern(KW.SAVE_PARTY, mode="kw", expr="sauvegarder la partie|"
                                                 "enregistrer la partie|"
                                                 "sauvegarder|"
                                                 "enregistrer")

lexer.add_pattern(KW.LANG, mode="kw", expr="français", value="fr-FR")
lexer.add_pattern(KW.LANG, mode="kw", expr="anglais", value="en-US")

# QUITTER / MENU PRINCIPAL
lexer.add_pattern(KW.QUIT, mode="kw", expr="quitter")
lexer.add_pattern(KW.MAIN_MENU, mode="kw", expr="menu principal")

# LANCER UNE PARTIE
lexer.add_pattern(KW.GAME, mode="kw", expr="301", value="301")
lexer.add_pattern(KW.GAME, mode="kw", expr="cricket", value="cricket")
lexer.add_pattern(KW.GAME, mode="kw", expr="around the clock", value="rtc")
lexer.add_pattern(KW.GAME, mode="kw", expr="alcooliques?")
lexer.add_pattern(KW.GAME, mode="kw", expr="[mM]olkky", value="molkky")

# ANNULER REFAIRE
lexer.add_pattern(KW.UNDO, mode="kw", expr="annuler|"
                                           "oups|"
                                           "oops")
lexer.add_pattern(KW.REDO, mode="kw", expr="restaurer|"
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

engine = engine_fr
