from dataclasses import replace
from item_engine import ACTION, STATE
from item_engine.textbase.elements import Char, Token
from typing import Iterator, Tuple


__all__ = ['lexer']


def _lexer(current: Token, item: Char) -> Tuple[ACTION, STATE]:
    if current.value == 0:
        if item.value == ' ':
            return '∈', 1
        elif item.value == '+':
            return '∈', 'PLUS'
        elif item.value == '.':
            return '∈', 'POINT'
        elif item.value == 'a':
            return '∈', 5
        elif item.value == 'b':
            return '∈', 6
        elif item.value == 'c':
            return '∈', 7
        elif item.value == 'd':
            return '∈', 8
        elif item.value == 'e':
            return '∈', 9
        elif item.value == 'f':
            return '∈', 10
        elif item.value == 'm':
            return '∈', 11
        elif item.value == 'n':
            return '∈', 12
        elif item.value == 'o':
            return '∈', 13
        elif item.value == 'p':
            return '∈', 14
        elif item.value == 'q':
            return '∈', 15
        elif item.value == 'r':
            return '∈', 16
        elif item.value == 's':
            return '∈', 17
        elif item.value == 't':
            return '∈', 18
        elif item.value == 'x':
            return '∈', 19
        elif item.value == 'z':
            return '∈', 20
        elif item.value in '358':
            return '∈', 4
        elif item.value in '0124679':
            return '∈', 3
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZghijkluvwyÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', '!KW_POUR'
    elif current.value == 1:
        if item.value == ' ':
            return '∈', 1
        else:
            return '∉', 'WHITESPACE'
    elif current.value == 2:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 3:
        if item.value in '0123456789':
            return '∈', 3
        else:
            return '∉', 'VALUE'
    elif current.value == 4:
        if item.value == '0':
            return '∈', 21
        elif item.value in '123456789':
            return '∈', 3
        else:
            return '∉', 'VALUE'
    elif current.value == 5:
        if item.value == ' ':
            return '∈', 22
        elif item.value == 'l':
            return '∈', 23
        elif item.value == 'n':
            return '∈', 24
        elif item.value == 'r':
            return '∈', 25
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 6:
        if item.value == 'o':
            return '∈', 26
        elif item.value == 'u':
            return '∈', 27
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnpqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 7:
        if item.value == 'r':
            return '∈', 28
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 8:
        if item.value == 'o':
            return '∈', 29
        elif item.value == 'u':
            return '∈', 30
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnpqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 9:
        if item.value == 't':
            return '∈', 31
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrsuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 10:
        if item.value == 'o':
            return '∈', 32
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnpqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 11:
        if item.value == 'a':
            return '∈', 33
        elif item.value == 'e':
            return '∈', 34
        elif item.value == 'o':
            return '∈', 35
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZbcdfghijklmnpqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 12:
        if item.value == 'o':
            return '∈', 36
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnpqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 13:
        if item.value == 'c':
            return '∈', 37
        elif item.value == 'k':
            return '∈', 38
        elif item.value in 'ou':
            return '∈', 39
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghijlmnpqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 14:
        if item.value == 'a':
            return '∈', 40
        elif item.value == 'e':
            return '∈', 41
        elif item.value == 'l':
            return '∈', 42
        elif item.value == 'o':
            return '∈', 43
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZbcdfghijkmnpqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 15:
        if item.value == 'u':
            return '∈', 44
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 16:
        if item.value == 'e':
            return '∈', 45
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 17:
        if item.value == 'e':
            return '∈', 46
        elif item.value == 'i':
            return '∈', 47
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghjklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 18:
        if item.value == 'r':
            return '∈', 48
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 19:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'FOIS'
    elif current.value == 20:
        if item.value == 'é':
            return '∈', 49
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 21:
        if item.value == '1':
            return '∈', 50
        elif item.value in '023456789':
            return '∈', 3
        else:
            return '∉', 'VALUE'
    elif current.value == 22:
        if item.value == 'f':
            return '∈', 51
        else:
            return '∉', '!A_FAIT'
    elif current.value == 23:
        if item.value == 'c':
            return '∈', 52
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 24:
        if item.value == 'n':
            return '∈', 53
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 25:
        if item.value == 'o':
            return '∈', 54
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnpqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 26:
        if item.value == 'u':
            return '∈', 55
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 27:
        if item.value == 'l':
            return '∈', 56
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 28:
        if item.value == 'i':
            return '∈', 57
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 29:
        if item.value == 'u':
            return '∈', 58
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 30:
        if item.value == 'r':
            return '∈', 59
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 31:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'KW_ET'
    elif current.value == 32:
        if item.value == 'i':
            return '∈', 60
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 33:
        if item.value == 'r':
            return '∈', 61
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 34:
        if item.value == 'n':
            return '∈', 62
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 35:
        if item.value == 'l':
            return '∈', 63
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 36:
        if item.value == 'n':
            return '∈', 64
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 37:
        if item.value == 't':
            return '∈', 64
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrsuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 38:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'KW_OK'
    elif current.value == 39:
        if item.value == 'p':
            return '∈', 65
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnoqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 40:
        if item.value == 'r':
            return '∈', 66
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 41:
        if item.value == 'n':
            return '∈', 67
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 42:
        if item.value == 'u':
            return '∈', 68
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 43:
        if item.value == 'i':
            return '∈', 69
        elif item.value == 'u':
            return '∈', 70
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 44:
        if item.value == 'a':
            return '∈', 71
        elif item.value == 'i':
            return '∈', 72
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZbcdefghjklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 45:
        if item.value == 'f':
            return '∈', 73
        elif item.value == 's':
            return '∈', 74
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdeghijklmnopqrtuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 46:
        if item.value == 'c':
            return '∈', 75
        elif item.value in 'px':
            return '∈', 37
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghijklmnoqrstuvwyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 47:
        if item.value == 'm':
            return '∈', 76
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 48:
        if item.value == 'i':
            return '∈', 76
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 49:
        if item.value == 'r':
            return '∈', 77
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 50:
        if item.value in '0123456789':
            return '∈', 3
        else:
            return '∉', 'GAME'
    elif current.value == 51:
        if item.value == 'a':
            return '∈', 78
        else:
            return '∉', '!A_FAIT'
    elif current.value == 52:
        if item.value == 'o':
            return '∈', 79
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnpqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 53:
        if item.value == 'u':
            return '∈', 80
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 54:
        if item.value == 'u':
            return '∈', 81
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 55:
        if item.value == 'l':
            return '∈', 82
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 56:
        if item.value == 'l':
            return '∈', 83
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 57:
        if item.value == 'c':
            return '∈', 84
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 58:
        if item.value == 'b':
            return '∈', 85
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZacdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 59:
        if item.value == 'a':
            return '∈', 86
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZbcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 60:
        if item.value == 's':
            return '∈', 19
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrtuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 61:
        if item.value == 'q':
            return '∈', 87
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnoprstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 62:
        if item.value == 'u':
            return '∈', 88
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 63:
        if item.value == 'k':
            return '∈', 89
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijlmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 64:
        if item.value == 'u':
            return '∈', 76
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 65:
        if item.value == 's':
            return '∈', 90
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrtuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 66:
        if item.value == 'a':
            return '∈', 91
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZbcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 67:
        if item.value == 'd':
            return '∈', 92
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 68:
        if item.value == 's':
            return '∈', 93
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrtuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 69:
        if item.value == 'n':
            return '∈', 94
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 70:
        if item.value == 'r':
            return '∈', 95
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 71:
        if item.value == 'd':
            return '∈', 96
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 72:
        if item.value == 'n':
            return '∈', 37
        elif item.value == 't':
            return '∈', 97
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrsuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 73:
        if item.value == 'a':
            return '∈', 98
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZbcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 74:
        if item.value == 't':
            return '∈', 99
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrsuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 75:
        if item.value == 'o':
            return '∈', 100
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnpqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 76:
        if item.value == 'p':
            return '∈', 85
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnoqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 77:
        if item.value == 'o':
            return '∈', 101
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnpqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 78:
        if item.value == 'i':
            return '∈', 102
        else:
            return '∉', '!A_FAIT'
    elif current.value == 79:
        if item.value == 'o':
            return '∈', 103
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnpqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 80:
        if item.value == 'l':
            return '∈', 104
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 81:
        if item.value == 'n':
            return '∈', 105
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 82:
        if item.value == 'e':
            return '∈', 101
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 83:
        if item.value == 'e':
            return '∈', 101
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'VALUE'
    elif current.value == 84:
        if item.value == 'k':
            return '∈', 106
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijlmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 85:
        if item.value == 'l':
            return '∈', 107
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 86:
        if item.value == 'n':
            return '∈', 108
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 87:
        if item.value == 'u':
            return '∈', 109
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 88:
        if item.value == ' ':
            return '∈', 110
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 89:
        if item.value == 'k':
            return '∈', 111
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijlmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 90:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'ANNULER'
    elif current.value == 91:
        if item.value == 'm':
            return '∈', 112
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 92:
        if item.value == 'a':
            return '∈', 113
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZbcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 93:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'PLUS'
    elif current.value == 94:
        if item.value == 't':
            return '∈', 114
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrsuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 95:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'KW_POUR'
    elif current.value == 96:
        if item.value == 'r':
            return '∈', 64
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 97:
        if item.value == 't':
            return '∈', 115
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrsuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 98:
        if item.value == 'i':
            return '∈', 116
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 99:
        if item.value == 'a':
            return '∈', 117
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZbcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 100:
        if item.value == 'n':
            return '∈', 118
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 101:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'VALUE'
    elif current.value == 102:
        if item.value == 't':
            return '∈', 'A_FAIT'
        else:
            return '∉', '!A_FAIT'
    elif current.value == 103:
        if item.value == 'l':
            return '∈', 119
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 104:
        if item.value == 'e':
            return '∈', 120
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 105:
        if item.value == 'd':
            return '∈', 121
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 106:
        if item.value == 'e':
            return '∈', 122
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 107:
        if item.value == 'e':
            return '∈', 123
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 108:
        if item.value == 't':
            return '∈', 124
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrsuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 109:
        if item.value == 'e':
            return '∈', 125
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 110:
        if item.value == 'p':
            return '∈', 126
        else:
            return '∉', '!MENU_PRINCIPAL'
    elif current.value == 111:
        if item.value == 'y':
            return '∈', 127
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 112:
        if item.value == 'è':
            return '∈', 128
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 113:
        if item.value == 'n':
            return '∈', 129
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 114:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'POINT'
    elif current.value == 115:
        if item.value == 'e':
            return '∈', 130
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 116:
        if item.value == 'r':
            return '∈', 131
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 117:
        if item.value == 'u':
            return '∈', 132
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 118:
        if item.value == 'd':
            return '∈', 133
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 119:
        if item.value == 'i':
            return '∈', 134
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 120:
        if item.value == 'r':
            return '∈', 90
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 121:
        if item.value == ' ':
            return '∈', 135
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 122:
        if item.value == 't':
            return '∈', 127
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrsuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 123:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'FACTOR'
    elif current.value == 124:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'DURANT'
    elif current.value == 125:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'MARQUE'
    elif current.value == 126:
        if item.value == 'r':
            return '∈', 136
        else:
            return '∉', '!MENU_PRINCIPAL'
    elif current.value == 127:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'GAME'
    elif current.value == 128:
        if item.value == 't':
            return '∈', 137
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrsuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 129:
        if item.value == 't':
            return '∈', 138
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrsuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 130:
        if item.value == 'r':
            return '∈', 139
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 131:
        if item.value == 'e':
            return '∈', 140
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 132:
        if item.value == 'r':
            return '∈', 141
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 133:
        if item.value == 'e':
            return '∈', 142
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 134:
        if item.value == 'q':
            return '∈', 143
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnoprstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 135:
        if item.value == 't':
            return '∈', 144
        else:
            return '∉', '!GAME'
    elif current.value == 136:
        if item.value == 'i':
            return '∈', 145
        else:
            return '∉', '!MENU_PRINCIPAL'
    elif current.value == 137:
        if item.value == 'r':
            return '∈', 146
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 138:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'PENDANT'
    elif current.value == 139:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'QUITTER'
    elif current.value == 140:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'REFAIRE'
    elif current.value == 141:
        if item.value == 'e':
            return '∈', 147
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 142:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'SECONDE'
    elif current.value == 143:
        if item.value == 'u':
            return '∈', 148
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 144:
        if item.value == 'h':
            return '∈', 149
        else:
            return '∉', '!GAME'
    elif current.value == 145:
        if item.value == 'n':
            return '∈', 150
        else:
            return '∉', '!MENU_PRINCIPAL'
    elif current.value == 146:
        if item.value == 'e':
            return '∈', 151
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 147:
        if item.value == 'r':
            return '∈', 140
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 148:
        if item.value == 'e':
            return '∈', 127
        elif item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdfghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'NAME'
    elif current.value == 149:
        if item.value == 'e':
            return '∈', 152
        else:
            return '∉', '!GAME'
    elif current.value == 150:
        if item.value == 'c':
            return '∈', 153
        else:
            return '∉', '!MENU_PRINCIPAL'
    elif current.value == 151:
        if item.value in '-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÂÄÊËÎÏÔÖÛÜàâäèéêëîïôöûüÿ':
            return '∈', 2
        else:
            return '∉', 'PARAMETRES'
    elif current.value == 152:
        if item.value == ' ':
            return '∈', 154
        else:
            return '∉', '!GAME'
    elif current.value == 153:
        if item.value == 'i':
            return '∈', 155
        else:
            return '∉', '!MENU_PRINCIPAL'
    elif current.value == 154:
        if item.value == 'c':
            return '∈', 156
        else:
            return '∉', '!GAME'
    elif current.value == 155:
        if item.value == 'p':
            return '∈', 157
        else:
            return '∉', '!MENU_PRINCIPAL'
    elif current.value == 156:
        if item.value == 'l':
            return '∈', 158
        else:
            return '∉', '!GAME'
    elif current.value == 157:
        if item.value == 'a':
            return '∈', 159
        else:
            return '∉', '!MENU_PRINCIPAL'
    elif current.value == 158:
        if item.value == 'o':
            return '∈', 160
        else:
            return '∉', '!GAME'
    elif current.value == 159:
        if item.value == 'l':
            return '∈', 'MENU_PRINCIPAL'
        else:
            return '∉', '!MENU_PRINCIPAL'
    elif current.value == 160:
        if item.value == 'c':
            return '∈', 161
        else:
            return '∉', '!GAME'
    elif current.value == 161:
        if item.value == 'k':
            return '∈', 'GAME'
        else:
            return '∉', '!GAME'
    else:
        raise Exception(f'value = {current.value!r}')


def lexer(src: Iterator[Char]) -> Iterator[Token]:
    cur: Token = Token(at=0, to=0, value=0)
    pos: int = 0
    for old in src:
        while cur.to == old.at:
            new: Token = cur.develop(_lexer(cur, old), old)
            if not new.is_terminal:
                cur = new
                continue
            if new.is_valid:
                cur = Token(at=new.to, to=new.to, value=0)
                if new.value in ['WHITESPACE']:
                    continue
                else:
                    new = replace(new, at=pos, to=pos + 1)
                    pos += 1
                yield new
                continue
            if old.value == 'EOF':
                yield Token.EOF(pos)
                break
            raise SyntaxError((cur, old, new))
