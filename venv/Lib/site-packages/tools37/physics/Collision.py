from tools37.geom import Vector, VectorBase
from .Object import Object
from .functions import elastic_collision


class Collision:
    def __init__(self, origin: Object, target: Object, dt: float):
        self.origin: Object = origin
        self.target: Object = target
        self.dt: float = dt
        self.v: Vector = Vector(0, 0)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.origin!r}, {self.target!r}, {self.dt!r}, {self.v!r})"

    def add(self, dt: float, v: Vector):
        if dt < self.dt:
            self.dt = dt
            self.v = v
        elif dt == self.dt:
            self.v += v

    def apply(self, col_callback=None):
        if abs(self.v):
            friction = (1 - self.origin.friction) * (1 - self.target.friction)

            ex = self.v.__unit__()

            base = VectorBase(ex, ex.__orth__())

            v1n, v1t = base << self.origin.speed
            v2n, v2t = base << self.target.speed

            v1n, v2n = elastic_collision(v1n, self.origin.mass, v2n, self.target.mass)

            self.origin.speed = Vector(friction * v1n, v1t) * base
            self.target.speed = Vector(friction * v2n, v2t) * base

            col_callback(self.origin)
            col_callback(self.target)
