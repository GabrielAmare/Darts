from item_engine.textbase import *


def pluralize(text: str):
    """Return the singular & plural form by adding an optional 's' at the end"""
    return string(text)  # & charset("s").inc().optional


letters = charset(
    'abcdefghijklmnopqrstuvwxyz' +
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
    '-' +
    'àéèâêûîôäëüïöÿÂÊÛÎÔÄËÜÏÖ'
).inc()

lexer, kws, sym = MakeLexer(
    keywords=[
        " et ", " pour ", "ok"
    ],
    symbols=[],
    branches=dict(
        POINT=pluralize("point") | string("."),
        FOIS=string("fois") | string("x"),
        PLUS=string("plus") | string("+"),
        A_FAIT=string("a fait"),
        MARQUE=pluralize("marque"),
        PENDANT=string("pendant"),
        DURANT=string("durant"),
        SECONDE=pluralize("seconde"),

        # SINGLE WORD COMMANDS
        QUITTER=string("quitter"),
        MENU_PRINCIPAL=string("menu principal"),
        PARAMETRES=pluralize("paramètre"),
        ANNULER=string("annuler") | string("oups") | string("oops"),
        REFAIRE=string("refaire") | string("restaurer"),

        # GAMES
        GAME=string("301") | string("501") | string("801")
             | string("cricket")
             | string("around the clock")
             | pluralize("alcoolique")
             | string("molkky"),

        # VALUES & FACTORS
        FACTOR=pluralize("simple")
               | pluralize("double")
               | pluralize("triple")
               | pluralize("quadruple")
               | pluralize("quintuple")
               | pluralize("sextuple")
               | pluralize("septuple")
               | pluralize("octuple")
               | pluralize("nonuple"),

        VALUE=pluralize("zéro")
            | pluralize("bull")
            | pluralize("bulle")
            | pluralize("boule"),

        WHITESPACE=charset(" ").inc().repeat(1, INF),
    ),
    raw_branches=[
        Branch("NAME", letters.repeat(1, INF), priority=-1),
        Branch("VALUE", digits.repeat(1, INF), priority=-1)
    ]
)

# PARSE FUNCTION FOR POWER INTEGERS
import python_generator as pg

VALUE_DICT = {
    "zéro": 0,
    "bull": 25,
    "bulle": 25,
    "boule": 25
}
FACTOR_DICT = {
    "simple": 1,
    "double": 2,
    "triple": 3,
    "quadruple": 4,
    "quintuple": 5,
    "sextuple": 6,
    "septuple": 7,
    "octuple": 8,
    "nonuple": 9,
}


def make_replace(old: pg.OBJECT) -> pg.CALL:
    return old.METH("replace", )


CONTENT = pg.VAR("content")
DATA = pg.VAR("data")

PARSE_VALUE = pg.DEF(
    "parse",
    args=CONTENT,
    block=pg.BLOCK(
        DATA.ASSIGN(pg.DICT({k: v for k, v in VALUE_DICT.items()})),
        pg.BLOCK(
            DATA.GETITEM(CONTENT).RETURN()
        ).IF(CONTENT.IN(DATA)).ELSE(
            pg.VAR("int").CALL(CONTENT).RETURN()
        )

    )
)
PARSE_FACTOR = pg.LAMBDA(
    args=CONTENT,
    expr=pg.DICT({k: v for k, v in FACTOR_DICT.items()}).GETITEM(CONTENT)
)

grp = GroupMaker({
    "score": ["VALUE"],
    "player": ["PLAYER"]
})

parser, operators = MakeParser(
    operators=dict(
        Value=UNIT(n="VALUE", k="value", t=int, f=PARSE_VALUE),
        Factor=UNIT(n="FACTOR", k="value", t=int, f=PARSE_FACTOR),
        Player=UNIT(n="NAME", k="name", t=str),
        Game=UNIT(n="GAME", k="name", t=str),

        # ValueFactor=OP(grp["factor"], grp["value"]),

        AddPlayer=OP(grp["NAME"]),

        AddScore=OP(grp["VALUE"], kws["POUR"], grp["PLAYER"]),

        StartParty=OP(kws["OK"]),
        NewParty=OP(grp["GAME"]),
        AddPlayers=ENUM(grp["NAME"], kws["ET"]),
    ),
    branches=dict(
        __ADDPLAYERS__=grp["NAME"].in_("cs").repeat(2, INF) & kws["ET"].tokenG.inc() & grp["NAME"].in_("cs")
    )
)

engine = Engine(
    name='engine_fr',
    parsers=[
        Parser(
            name='lexer',
            branch_set=lexer,
            input_cls=Char,
            output_cls=Token,
            skips=["WHITESPACE"],
            formal_inputs=True,
            formal_outputs=True,
            reflexive=False,
        ),
        Parser(
            name='parser',
            branch_set=parser,
            input_cls=Token,
            output_cls=Lemma,
            skips=[],
            formal_inputs=True,
            formal_outputs=False,
            reflexive=True,
        )
    ],
    operators=operators
)


def main():
    engine.build(allow_overwrite=True)


if __name__ == '__main__':
    main()
