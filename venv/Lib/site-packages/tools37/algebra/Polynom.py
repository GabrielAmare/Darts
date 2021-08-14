from functools import reduce
from itertools import repeat, zip_longest, starmap
from operator import add, sub, mul, truediv
from typing import List, Iterator, TypeVar, Generic

from tools37.Typed import Typed, TypedArg, typedmethod

C = TypeVar('C')


class Polynom(Generic[C], Typed):
    def __init__(self, *factors: C):
        self.factors: List[C] = list(factors) or [0]

        while len(self.factors) > 1 and self.factors[-1] == 0:
            self.factors.pop(-1)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(map(repr, self.factors))})"

    def __eq__(self, other):
        return type(self) is type(other) and self.factors == other.factors

    def __len__(self) -> int:
        return len(self.factors)

    def __iter__(self) -> Iterator[C]:
        return iter(self.factors)

    def __getitem__(self, index: int) -> C:
        return self.factors[index]

    def __setitem__(self, index: int, value: C) -> None:
        self.factors[index] = value

    def __call__(self, x):
        return sum(c * x ** p for p, c in enumerate(self.factors))

    @typedmethod(TypedArg.CLASS)
    def __add__(self, other):
        return Polynom(*starmap(add, zip_longest(self, other, fillvalue=0)))

    @typedmethod(TypedArg.CLASS)
    def __sub__(self, other):
        return Polynom(*starmap(sub, zip_longest(self, other, fillvalue=0)))

    @typedmethod(TypedArg.CLASS)
    def __mul__(self, other):
        factors = [0 for p in range(len(self) + len(other))]
        for p1, c1 in enumerate(self):
            for p2, c2 in enumerate(other):
                factors[p1 + p2] += c1 * c2

        return Polynom(*factors)

    @typedmethod(object)
    def __add__(self, other):
        factors = self.factors.copy()
        factors[0] = add(factors[0], other)
        return Polynom(*factors)

    @typedmethod(object)
    def __radd__(self, other):
        factors = self.factors.copy()
        factors[0] = add(other, factors[0])
        return Polynom(*factors)

    @typedmethod(object)
    def __sub__(self, other):
        factors = self.factors.copy()
        factors[0] = sub(factors[0], other)
        return Polynom(*factors)

    @typedmethod(object)
    def __rsub__(self, other):
        factors = self.factors.copy()
        factors[0] = sub(other, factors[0])
        return Polynom(*factors)

    @typedmethod(object)
    def __mul__(self, other):
        return Polynom(*map(mul, self, repeat(other, len(self))))

    @typedmethod(object)
    def __rmul__(self, other):
        return Polynom(*map(mul, repeat(other, len(self)), self))

    @typedmethod(object)
    def __truediv__(self, other):
        return Polynom(*map(truediv, self, repeat(other, len(self))))

    @typedmethod(int)
    def __pow__(self, other: int):
        if other < 0:
            return NotImplemented

        return reduce(mul, repeat(self, other))

    @typedmethod(object)
    def __pow__(self, other):
        return NotImplemented

    def _solve_1(self):
        if self[0] == 0:
            return []
        else:
            return []

    def _solve_2(self):
        return [-self[0] / self[1]]

    def _solve_3(self):
        delta = self[1] ** 2 - 4 * self[0] * self[2]
        if delta < 0:
            return []

        alpha = - self[1] / (2 * self[2])

        if delta == 0:
            return [alpha]

        beta = delta ** 0.5 / abs(2 * self[2])

        return [alpha - beta, alpha + beta]

    def solve(self):
        if len(self) == 1:
            return self._solve_1()
        elif len(self) == 2:
            return self._solve_2()
        elif len(self) == 3:
            return self._solve_3()
        else:
            raise ValueError(f"cannot solve polynoms of degree > 2 : {len(self) - 1}")
