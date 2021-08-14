from numbers import Real

from tools37.geom import Vector
from .Object import Object


class Circle(Object):
    def __init__(self, position: Vector, radius: Real, speed: Vector, mass: Real):
        super().__init__(position, speed, mass)
        self.radius: Real = radius

    def __repr__(self):
        return f"{self.__class__.__name__}({self.position!r}, {self.radius!r}, {self.speed!r}, {self.mass!r})"