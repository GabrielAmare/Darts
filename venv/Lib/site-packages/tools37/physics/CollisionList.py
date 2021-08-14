from typing import List

from .Collision import Collision


class CollisionList:
    def __init__(self, dt: float):
        self.dt: float = dt
        self.collisions: List[Collision] = []

    def __iter__(self):
        return iter(self.collisions)

    def __len__(self):
        return len(self.collisions)

    def __bool__(self):
        return bool(self.collisions)

    def add(self, collision: Collision):
        if collision.dt < self.dt:
            self.dt = collision.dt
            self.collisions = [collision]
        elif collision.dt == self.dt:
            self.collisions.append(collision)

    def apply(self, col_callback=None):
        for collision in self.collisions:
            collision.apply(col_callback)
