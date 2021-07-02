from item_engine.textbase import *
from itertools import starmap
from operator import eq


class Value:
    def __init__(self, value: int):
        self.value: int = value
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.value!r})'
    
    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value


class Factor:
    def __init__(self, value: int):
        self.value: int = value
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.value!r})'
    
    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value


class Player:
    def __init__(self, name: str):
        self.name: str = name
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r})'
    
    def __str__(self):
        return str(self.name)
    
    def __eq__(self, other):
        return type(self) is type(other) and self.name == other.name


class Game:
    def __init__(self, name: str):
        self.name: str = name
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r})'
    
    def __str__(self):
        return str(self.name)
    
    def __eq__(self, other):
        return type(self) is type(other) and self.name == other.name


class AddPlayer:
    def __init__(self, c0):
        self.c0 = c0
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.c0!r})'
    
    def __str__(self):
        return f'{self.c0!s}'
    
    def __eq__(self, other):
        return type(self) is type(other) and self.c0 == other.c0


class AddScore:
    def __init__(self, c0, c1):
        self.c0 = c0
        self.c1 = c1
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.c0!r}, {self.c1!r})'
    
    def __str__(self):
        return f'{self.c0!s} pour {self.c1!s}'
    
    def __eq__(self, other):
        return type(self) is type(other) and self.c0 == other.c0 and self.c1 == other.c1


class StartParty:
    def __init__(self):
        pass
    
    def __repr__(self):
        return f'{self.__class__.__name__}()'
    
    def __str__(self):
        return f'ok'
    
    def __eq__(self, other):
        return type(self) is type(other)


class NewParty:
    def __init__(self, c0):
        self.c0 = c0
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.c0!r})'
    
    def __str__(self):
        return f'{self.c0!s}'
    
    def __eq__(self, other):
        return type(self) is type(other) and self.c0 == other.c0


class AddPlayers:
    def __init__(self, *cs):
        self.cs = cs
    
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(map(repr, self.cs))})"
    
    def __str__(self):
        return ' et '.join(map(str, self.cs))
    
    def __eq__(self, other):
        return type(self) is type(other) and all(starmap(eq, zip(self.cs, other.cs)))


def build(e: Element):
    if isinstance(e, Lemma):
        if e.value == '__ADDPLAYER__':
            return AddPlayer(build(e.data['c0']))
        elif e.value == '__ADDSCORE__':
            return AddScore(build(e.data['c0']), build(e.data['c1']))
        elif e.value == '__STARTPARTY__':
            return StartParty()
        elif e.value == '__NEWPARTY__':
            return NewParty(build(e.data['c0']))
        elif e.value == '__ADDPLAYERS__':
            return AddPlayers(*map(build, e.data['cs']))
        else:
            raise Exception(e.value)
    elif isinstance(e, Token):
        if e.value == 'VALUE':
            def parse(content):
                data = dict(zéro=0, bull=25, bulle=25, boule=25)
                if content in data:
                    return data[content]
                else:
                    return int(content)
            
            return Value(int(parse(e.content)))
        elif e.value == 'FACTOR':
            parse = lambda content: dict(simple=1, double=2, triple=3, quadruple=4, quintuple=5, sextuple=6, septuple=7, octuple=8, nonuple=9)[content]
            return Factor(int(parse(e.content)))
        elif e.value == 'NAME':
            return Player(str(e.content))
        elif e.value == 'GAME':
            return Game(str(e.content))
        else:
            raise Exception(e.value)
    else:
        raise Exception(e.value)
