from typing import Generator

from tools37.Typed import Typed, typedmethod
from .Vector import Vector, Real


class VectorBase(Typed):
    """Represent a basis of two vectors ex and ey."""

    def __init__(self, ex: Vector, ey: Vector = None):
        if ey is None:
            ey = ex.__orth__()

        assert ex ^ ey != 0
        self.ex: Vector = ex
        self.ey: Vector = ey

    def __iter__(self) -> Generator[Vector, None, None]:
        yield self.ex
        yield self.ey

    def __len__(self) -> int:
        return 2

    def __repr__(self):
        return f"{self.__class__.__name__}({self.ex!r}, {self.ey!r})"

    def __eq__(self, other):
        return type(self) is type(other) and self.ex == other.ex and self.ey == other.ey

    def __getitem__(self, index: int) -> Vector:
        if index == 0:
            return self.ex
        elif index == 1:
            return self.ey
        else:
            raise IndexError(index)

    def __setitem__(self, index: int, value: Vector) -> None:
        if index == 0:
            self.ex = value
        elif index == 1:
            self.ey = value
        else:
            raise IndexError(index)

    def __abs__(self) -> Real:
        return self.ex ^ self.ey

    @typedmethod(Vector)
    def __lshift__(self, vector: Vector) -> Vector:
        """Return the vector projected in the base."""
        return Vector(vector ^ self.ey, self.ex ^ vector) / abs(self)

    @typedmethod(Vector)
    def __mul__(self, vector: Vector) -> Vector:
        """Return the vector extracted from the base."""
        return vector.x * self.ex + vector.y * self.ey

    @typedmethod(Vector)
    def __rrshift__(self, other: Vector) -> Vector:
        return self << other

    @typedmethod(Vector)
    def __rmul__(self, other: Vector) -> Vector:
        return self * other
