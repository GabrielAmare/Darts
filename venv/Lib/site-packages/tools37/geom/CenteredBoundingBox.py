from numbers import Real

from .BoundingBox import BoundingBox


class CenteredBoundingBox(BoundingBox):
    def __init__(self, x: Real, y: Real, dx: Real, dy: Real):
        assert float(dx) > 0
        assert float(dy) > 0
        self.x: Real = x
        self.y: Real = y
        self.dx: Real = dx
        self.dy: Real = dy

    @property
    def xi(self):
        return self.x - self.dx

    @xi.setter
    def xi(self, value):
        self.x = value + self.dx

    @property
    def xf(self):
        return self.x + self.dx

    @xf.setter
    def xf(self, value):
        self.x = value - self.dx

    @property
    def yi(self):
        return self.y - self.dy

    @yi.setter
    def yi(self, value):
        self.y = value + self.dy

    @property
    def yf(self):
        return self.y + self.dy

    @yf.setter
    def yf(self, value):
        self.y = value - self.dy
