from numbers import Real
from typing import List

from tools37.Typed import Typed, typedmethod
from tools37.geom import Vector
from .Circle import Circle
from .Collision import Collision
from .CollisionList import CollisionList
from .Line import Line
from .Object import Object
from .functions import circle_line_collision, circle_circle_collision


class System(Typed):
    def __init__(self, gravity: Vector, friction: Real, max_collision_check: int = 100):
        self.objects: List[Object] = []
        self.gravity: Vector = gravity
        self.friction: Real = friction
        self.objects_searching_for_collision: List[Object] = []
        self.max_collision_check: int = max_collision_check

    def forward(self, dt: float):
        for o in self.objects:
            o.forward(dt)

    def update(self, dt: float = 1.0, col_callback=None):
        for o in self.objects:
            o.apply_force(self.gravity)
            o.apply_friction(self.friction)

        checks = 0
        while dt > 0 and checks < self.max_collision_check:
            collisions = CollisionList(dt)
            done = []
            for origin in self.objects_searching_for_collision:
                done.append(origin)
                for target in self.objects:
                    if target not in done:
                        collision = self.calculate_collision(origin, target, dt)
                        collisions.add(collision)

            if not collisions:
                break

            self.forward(collisions.dt)
            collisions.apply(col_callback)
            dt -= collisions.dt

            checks += len(collisions)

        if checks >= self.max_collision_check:
            print("MAX COLLISION CHECK OVERLOAD")

        if 0 < dt:
            self.forward(dt)

    def calculate_collision(self, origin: Object, target: Object, dt: float):
        collision = Collision(origin, target, dt)
        for dt, v in self.calculate_collisions_between(origin, target):
            if 0 < dt:
                collision.add(dt, v)
        return collision

    @typedmethod(Circle, Circle)
    def calculate_collisions_between(self, origin: Circle, target: Circle):
        if abs(origin.position - target.position) - (origin.radius + target.radius) <= abs(origin.speed) + abs(target.speed):
            for t, v in circle_circle_collision(origin, target):
                yield t, v

    @typedmethod(Circle, Line)
    def calculate_collisions_between(self, origin: Circle, target: Line):
        for t, v in circle_line_collision(origin, target):
            yield t, v

    @typedmethod(Line, Circle)
    def calculate_collisions_between(self, origin: Line, target: Circle):
        for t, v in circle_line_collision(target, origin):
            yield t, -v

    @typedmethod(Object, Object)
    def calculate_collisions_between(self, origin, target):
        raise NotImplementedError(f"collision between {type(origin)!r} and {type(target)!r} is not handled yet !")

    @typedmethod(object, object)
    def calculate_collisions_between(self, origin, target):
        raise TypeError(type(origin), type(target))
