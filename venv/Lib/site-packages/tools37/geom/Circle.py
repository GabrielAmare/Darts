from numbers import Real

from tools37.Typed import Typed, typedmethod
from .Coords import Coords


class Circle(Typed):
    def __init__(self, x: Real, y: Real, r: Real):
        assert float(r) > 0
        self.x: Real = x
        self.y: Real = y
        self.r: Real = r

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x!r}, {self.y!r}, {self.r!r})"

    def __eq__(self, other):
        return type(self) is type(other) and self.x == other.x and self.y == other.y and self.r == other.r

    @typedmethod(Coords)
    def __contains__(self, other: Coords) -> bool:
        center = Coords(self.x, self.y)
        return abs(other - center) <= self.r

    @typedmethod(Coords)
    def __lshift__(self, other: Coords) -> Coords:
        """Return the projection of other on the border of self."""
        center = Coords(self.x, self.y)
        return center + self.r * (other - center).__unit__()

    @typedmethod(Coords)
    def __rrshift__(self, other: Coords) -> Coords:
        return self << other
