from numbers import Real

from tools37.geom import Vector
from .Object import Object


class Line(Object):
    def __init__(self, origin: Vector, target: Vector, speed: Vector, mass: Real, friction: float = 0.0):
        center = (target + origin) / 2
        delta = (target - origin) / 2
        super().__init__(center, speed, mass, friction)
        self.delta: Vector = delta

    def __repr__(self):
        return f"{self.__class__.__name__}({self.origin!r}, {self.target!r}, {self.speed!r}, {self.mass!r})"

    @property
    def origin(self):
        return self.position - self.delta

    @property
    def target(self):
        return self.position + self.delta
