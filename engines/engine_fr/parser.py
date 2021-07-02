from item_engine import ACTION, STATE
from item_engine.textbase.elements import Lemma, Token
from typing import Dict, Iterator, List, Tuple, Union


__all__ = ['parser']


def _parser(current: Lemma, item: Token) -> Iterator[Tuple[ACTION, STATE]]:
    if current.value == 0:
        if item.value == 'GAME':
            yield 'as:c0', '__NEWPARTY__'
        elif item.value == 'KW_OK':
            yield '∈', '__STARTPARTY__'
        elif item.value == 'NAME':
            yield 'in:cs', 1
        elif item.value == 'VALUE':
            yield 'as:c0', 2
        else:
            yield '∉', '!__ADDPLAYERS__|__ADDPLAYER__|__ADDSCORE__|__NEWPARTY__|__STARTPARTY__'
    elif current.value == 1:
        if item.value == 'KW_ET':
            yield '∈', 3
        elif item.value == 'NAME':
            yield 'in:cs', 4
        else:
            yield '∉', '!__ADDPLAYERS__'
    elif current.value == 2:
        if item.value == 'KW_POUR':
            yield '∈', 5
        else:
            yield '∉', '!__ADDSCORE__'
    elif current.value == 3:
        if item.value == 'NAME':
            yield 'in:cs', 6
        else:
            yield '∉', '!__ADDPLAYERS__'
    elif current.value == 4:
        if item.value == 'KW_ET':
            yield '∈', 7
        elif item.value == 'NAME':
            yield 'in:cs', 4
        else:
            yield '∉', '!__ADDPLAYERS__'
    elif current.value == 5:
        if item.value == 'PLAYER':
            yield 'as:c1', '__ADDSCORE__'
        else:
            yield '∉', '!__ADDSCORE__'
    elif current.value == 6:
        if item.value == 'KW_ET':
            yield '∈', 3
        else:
            yield '∉', '__ADDPLAYERS__'
    elif current.value == 7:
        if item.value == 'NAME':
            yield 'in:cs', '__ADDPLAYERS__'
        else:
            yield '∉', '!__ADDPLAYERS__'
    else:
        raise Exception(f'value = {current.value!r}')


def parser(src: Iterator[Token]) -> Iterator[Lemma]:
    curs: Dict[int, List[Lemma]] = {}
    def add_cur(cur: Lemma):
        to = cur.to
        if to not in curs:
            curs[to] = [cur]
        elif cur not in curs[to]:
            curs[to].append(cur)
    
    add_cur(Lemma(at=0, to=0, value=0))
    stack: List[Union[Token, Lemma]] = []
    j: int = 0
    for old in src:
        stack.append(old)
        while j < len(stack):
            oldr: Lemma = stack[j]
            j += 1
            if oldr.at in curs:
                queue = curs[oldr.at]
                add_cur(Lemma(at=oldr.at, to=oldr.at, value=0))
                i = 0
                while i < len(queue):
                    cur: Lemma = queue[i]
                    i += 1
                    for new in (cur.develop(res, oldr) for res in _parser(cur, oldr)):
                        if not new.is_terminal:
                            add_cur(new)
                            continue
                        if new.is_valid:
                            if new not in stack:
                                stack.insert(j, new)
                            add_cur(Lemma(at=new.to, to=new.to, value=0))
                            yield new
                            continue
                continue
        if old.value == 'EOF':
            yield Lemma.EOF(old.to)
            break
