from tools37.geom import Vector
from numbers import Real


class Object:
    """Object with mass."""

    def __init__(self, position: Vector, speed: Vector, mass: Real, friction: float = 0.0):
        self.position: Vector = position
        self.speed: Vector = speed
        self.mass: Real = mass
        self.friction: float = friction

    def apply_friction(self, friction: Real):
        assert 0 <= float(friction) <= 1
        self.speed *= 1 - friction

    def apply_force(self, force: Vector):
        if self.mass < float('inf'):
            self.speed += force

    def apply_pacman(self, xi: Real, yi: Real, xf: Real, yf: Real):
        dx, dy = xf - xi, yf - yi
        if dx == 0:
            self.position.x = xi
        else:
            self.position.x %= dx
        if dy == 0:
            self.position.y = yi
        else:
            self.position.y %= yi

    def forward(self, dt: Real = 1.0):
        self.position += dt * self.speed
