from engines.fr import engine
from engines.engine_fr.lexer import lexer

engine.build(allow_overwrite=True)
print('engine rebuilt !')

from engines.engine_fr import *
from item_engine.textbase import make_characters
from engines.engine_fr.materials import *


def get_commands(text: str):
    *lemmas, eof = parse(make_characters(text, eof=True))

    for lemma in lemmas:
        if lemma.at == 0 and lemma.to == eof.at:
            yield build(lemma)


def test(text, expected):
    for token in lexer(make_characters(text, eof=True)):
        print(repr(token))

    for lemma in parse(make_characters(text, eof=True)):
        print(lemma)

    print()

    commands = list(get_commands(text))
    assert commands == expected, f"\ntext = {text!r}\nexpected = {expected}\ncommands = {commands}"


def main():
    test("5 pour michel", [AddScore(Value(5), Player("michel"))])
    test("bull pour michel", [AddScore(Value(25), Player("michel"))])
    test("zéro pour michel", [AddScore(Value(0), Player("michel"))])
    # test("double 5 pour michel", [AddScore(ValueFactor(Factor(2), Value(5)), Player("michel"))])

    while True:
        text = input("command > ")
        if not text:
            break

        for command in get_commands(text):
            print(command)
            print(repr(command))


if __name__ == '__main__':
    main()
