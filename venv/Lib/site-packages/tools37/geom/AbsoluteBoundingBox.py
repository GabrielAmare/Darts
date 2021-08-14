from numbers import Real

from .BoundingBox import BoundingBox


class AbsoluteBoundingBox(BoundingBox):
    def __init__(self, xi: Real, yi: Real, xf: Real, yf: Real):
        assert xi < xf
        assert yi < yf
        self.xi: Real = xi
        self.yi: Real = yi
        self.xf: Real = xf
        self.yf: Real = yf

    def __repr__(self):
        return f"{self.__class__.__name__}({self.xi!r}, {self.yi!r}, {self.xf!r}, {self.yf!r})"

    @property
    def x(self) -> Real:
        return (self.xi + self.xf) / 2

    @x.setter
    def x(self, value: Real):
        dx = self.dx
        self.xi, self.xf = value - dx, value + dx

    @property
    def y(self) -> Real:
        return (self.yi + self.yf) / 2

    @y.setter
    def y(self, value: Real):
        dy = self.dy
        self.yi, self.yf = value - dy, value + dy

    @property
    def dx(self) -> Real:
        return (self.xf - self.xi) / 2

    @dx.setter
    def dx(self, value: Real):
        x = self.x
        self.xi, self.xf = x - value, x + value

    @property
    def dy(self) -> Real:
        return (self.yf - self.yi) / 2

    @dy.setter
    def dy(self, value: Real):
        y = self.y
        self.yi, self.yf = y - value, y + value
